import pandas as pd
import unicodedata
from otomasi.utilities.files import read_df
from collections import deque


class GroupDistributor:
    def __init__(self, group_size, min_group_size=-1) -> None:
        self.group_size = group_size
        self.min_group_size = min_group_size
        # List of groups where ith elements are groups with i members
        # i.e. group_queues[0] has 0 member, group_queues[1] has 1 member, ...,
        # group_queues[group_size] has group_size members
        self.group_queues: list[deque[list[pd.DataFrame]]] = [
            deque() for _ in range(group_size)
        ]
        self.complete_groups: list[pd.DataFrame] = []

    def enqueue_group(self, group: pd.DataFrame):
        group_len = len(group)
        # check if deque is not empty (there exist a group requiring group_len more members
        if self.group_queues[-group_len]:
            new_group = self.group_queues[-group_len].pop()
            new_group.append(group)
            self.complete_groups.append(pd.concat(new_group))
        else:  # deque is empty, insert the group as the group requiring group_size - group_len more members
            self.group_queues[group_len].append([group])

    def combine_remainders(self):
        # group the remaining incomplete groups
        if self.min_group_size == -1:
            self.dump_remainders()
        elif self.min_group_size == 0:
            for group_deque in self.group_queues:
                while group_deque:
                    group = group_deque.pop()
                    self.complete_groups.append(pd.concat(group))
        else:
            count = 0
            temp_groups: list[pd.DataFrame] = []
            for i, group_deque in reversed(list(enumerate(self.group_queues))):
                curr_group_size = i
                while group_deque:
                    # add up the current group until it is maximized
                    while count + curr_group_size < self.group_size and group_deque:
                        count += curr_group_size
                        temp_groups.extend(group_deque.pop())
                    # add the remaining groups
                    remaining = self.group_size - count
                    while (count + remaining <= self.group_size) and (0 < remaining):
                        remaining_deque = self.group_queues[remaining]
                        if remaining_deque:
                            count += remaining
                            temp_groups.extend(remaining_deque.pop())
                        else:
                            remaining -= 1
                    # if the group meet the minimum group size, sum up, then restart
                    if count >= self.min_group_size or group_deque:
                        new_group = pd.concat(temp_groups)
                        self.complete_groups.append(new_group)
                        count = 0
                        temp_groups = []
            # finished iterating all groups, dump the remaining unallocated groups
            if temp_groups:
                unallocated_group = pd.concat(temp_groups)
                self.enqueue_group(unallocated_group)
            self.dump_remainders()

        return self.complete_groups

    def dump_remainders(self):
        temp_groups: list[pd.DataFrame] = []
        for group_deque in self.group_queues:
            while group_deque:
                temp_groups.extend(group_deque.pop())
        if temp_groups:
            self.complete_groups.append(pd.concat(temp_groups))


def distribute_groups(dataset: pd.DataFrame, group_size, min_group_size):
    if "RUMPUN" in dataset.columns:
        dataset = dataset.sort_values("RUMPUN")
    else:
        dataset = dataset.sort_values("PRODI")
    grouped = dataset.groupby("FAKULTAS")
    groups: list[pd.DataFrame] = []

    group_distributor = GroupDistributor(group_size, min_group_size)
    for _, group in grouped:
        cur_group = group
        group_len = len(group)
        # if group is larger than the target size, split the group
        if group_len > group_size:
            cur_group = cur_group.reset_index(drop=True)
            n_groups = group_len // group_size
            for i in range(n_groups):
                start = i * group_size
                groups.append(cur_group.iloc[start : start + group_size, :])

            # process the remainder group
            remainder_size = group_len % group_size
            if remainder_size != 0:
                last_slice = n_groups * group_size
                # swap the remainder into group and group_len
                # to use the same logic as small groups
                cur_group = cur_group.iloc[last_slice:, :]
                group_len = remainder_size
            else:  # no remainder remaining, continue to the next groups
                continue
        if group_len >= min_group_size:
            groups.append(cur_group)
        else:  # group_len < group_size
            group_distributor.enqueue_group(cur_group)
    remaining_groups = group_distributor.combine_remainders()
    groups.extend(remaining_groups)
    return groups


def create_groups(dataset: pd.DataFrame, group_size=8, min_group_size=6):
    # split male/female students into primary groups
    l_dataset = dataset[dataset["KELOMPOK"].values == "L"]
    p_dataset = dataset[dataset["KELOMPOK"].values == "P"]

    l_datasets = distribute_groups(l_dataset, group_size, min_group_size)
    p_datasets = distribute_groups(p_dataset, group_size, min_group_size)
    return l_datasets, p_datasets
    # TODO: try custom sorting https://stackoverflow.com/questions/23482668/sorting-by-a-custom-list-in-pandas
    # group into faculties
    # might need to iterate group https://pandas.pydata.org/docs/user_guide/groupby.html#iterating-through-groups


def write_to_excel(
    datasets: list[pd.DataFrame],
    out: str,
    category: str,
    overwrite: bool = False,
    check_min=0,
):
    # https://www.geeksforgeeks.org/how-to-write-pandas-dataframes-to-multiple-excel-sheets/
    write_mode = "w" if overwrite else "a"
    with pd.ExcelWriter(f"{out}.xlsx", engine="openpyxl", mode=write_mode) as writer:
        for idx, group in enumerate(datasets, start=1):
            group_size = len(group)
            if group_size == 0 or group_size < check_min:
                print(
                    f"Warning: group {category}{idx} does not meet minimum group size!"
                )
            group.to_excel(writer, sheet_name=f"{category}{idx}", index=False)


def main(input_file: list[str], out: str, group_size: int, min_size: int):
    assert (
        group_size >= min_size
    ), "Group size must be greater or equal to the minimum size!"

    l_groups: list[pd.DataFrame] = []
    p_groups: list[pd.DataFrame] = []
    for file in input_file:
        # use read_df to get encoding fallbacks and consistent file handling
        dataset = read_df(file)
        # Normalize header names and ensure required columns exist
        dataset = _standardize_columns(dataset)
        _validate_required_columns(dataset)
        l_datasets, p_datasets = create_groups(dataset, group_size, min_size)
        l_groups.extend(l_datasets)
        p_groups.extend(p_datasets)

    write_to_excel(l_groups, out, "L", overwrite=True, check_min=min_size)
    write_to_excel(p_groups, out, "P", overwrite=False, check_min=min_size)


def _clean_header(name: str) -> str:
    # Normalize unicode and remove non-breaking spaces, trim and uppercase
    s = unicodedata.normalize("NFKC", str(name)).replace("\u00A0", " ")
    return s.strip().upper()


def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Map potential header variants to the expected canonical names
    synonyms = {
        "KELOMPOK": "KELOMPOK",
        "KEL": "KELOMPOK",
        "JK": "KELOMPOK",
        "GENDER": "KELOMPOK",
        "JENIS KELAMIN": "KELOMPOK",
        "FAKULTAS": "FAKULTAS",
        "FAK": "FAKULTAS",
        "PRODI": "PRODI",
        "PROGRAM STUDI": "PRODI",
        "PROGDI": "PRODI",
        "RUMPUN": "RUMPUN",
    }

    rename_map: dict[str, str] = {}
    for c in df.columns:
        key = _clean_header(c)
        if key in synonyms:
            rename_map[c] = synonyms[key]
        else:
            # keep cleaned name for other columns (e.g., NO, NIM, NAMA)
            rename_map[c] = _clean_header(c)

    df = df.rename(columns=rename_map)
    return df


def _validate_required_columns(df: pd.DataFrame):
    missing = [c for c in ("KELOMPOK", "FAKULTAS", "PRODI") if c not in df.columns]
    if missing:
        raise ValueError(
            "Input file is missing required columns: "
            + ", ".join(missing)
            + f". Found columns: {list(df.columns)}"
        )
