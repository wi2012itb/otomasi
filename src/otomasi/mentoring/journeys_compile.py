import glob
import itertools
import pandas as pd

from otomasi.utilities.files import read_df, write_df
from otomasi.utilities.xlsx import extract_table, find_anchor


def _extract_data(df: pd.DataFrame, anchor_header: str) -> pd.DataFrame:
    (row, col) = find_anchor(df, anchor_header)
    _df = df.iloc[row:, col:]
    # Extract headers
    main_headers = (
        _df.iloc[:1].astype("string").ffill(axis=1).fillna("").values.tolist()[0]
    )
    # and sub_headers
    sub_headers = (
        _df.iloc[1:2].astype("string").ffill(axis=1).fillna("").values.tolist()[0]
    )
    # Then combine them into a flat -single dimensional- header
    final_headers = [
        f"{header}_{sub}" if sub != "" else header
        for header, sub in zip(main_headers, sub_headers)
    ]

    data = extract_table(_df, final_headers, start_row=2)
    data.dropna(subset=anchor_header, inplace=True)
    return data


def filter_valid_df(
    df: pd.DataFrame, path: str, raise_error: bool = False
) -> pd.DataFrame | None:
    if not df.loc[:, df.columns.duplicated()].empty:
        msg = f"duplicate headers found in file: {path}"
        if raise_error:
            raise ValueError(msg)
        else:
            print(msg)
            return
    # All ok, return the dataframe
    return df


def main(globs: list[str], header: str, out: str):
    # extract globs and flatten into path list
    paths_lists = [glob.glob(_glob, recursive=True) for _glob in globs]
    paths = list(itertools.chain(*paths_lists))

    # read dataframes
    mentor_grades = [(read_df(path), path) for path in paths]
    extracted_dfs = [(_extract_data(df, header), path) for df, path in mentor_grades]

    valid_dfs = [filter_valid_df(df, _path) for df, _path in extracted_dfs]

    compiled_grades = pd.concat(valid_dfs, join="outer", ignore_index=True)
    write_df(compiled_grades, out, index=False)
