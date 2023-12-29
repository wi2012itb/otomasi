from argparse import FileType
import json
import pandas as pd

from enum import Enum
from datetime import datetime, timedelta

from otomasi.utilities.files import DfOutFormat, write_df


class Days(Enum):
    Senin = 0
    Selasa = 1
    Rabu = 2
    Kamis = 3
    Jumat = 4
    Sabtu = 5
    Minggu = 6


def generate_schedule(
    start_date: datetime, week_count: int, class_schedule: dict[str, int]
) -> pd.DataFrame:
    seed = {
        "minggu": [i for i in range(1, week_count + 1)],
        "week_start": [
            (start_date + timedelta(days=(7 * i))) for i in range(week_count)
        ],
    }
    schedule = pd.DataFrame(seed)
    # Create each class date schedule
    for class_name, class_day in class_schedule.items():
        day_diff = timedelta(days=Days[class_day].value)
        schedule[class_name] = schedule.apply(lambda x: x.week_start + day_diff, axis=1)

    schedule.drop("week_start", axis=1, inplace=True)
    return schedule


def format_list_in_csv(list):
    return f"{",".join(list)}"


def filter_holidays(
    schedule: pd.DataFrame, holidays: pd.DataFrame, class_cols: list[str]
) -> pd.DataFrame:
    for col in class_cols:
        schedule[f"{col}_holiday"] = schedule[col].apply(
            lambda x: format_list_in_csv(
                holidays.loc[
                    (holidays["start"] <= x) & (holidays["end"] >= x), "detail"
                ].values
            )
        )

    return schedule


def format_result(schedule: pd.DataFrame, include_date: bool, class_cols: list[str]):
    if include_date:
        schedule[class_cols] = schedule[class_cols].apply(lambda x: x.dt.date)
    else:
        schedule.drop(columns=class_cols, inplace=True)
    return schedule


def main(
    seed_file: FileType,
    holiday_file: FileType,
    output_path: str,
    output_format: DfOutFormat,
    drop_dates: bool,
):
    seed = json.load(seed_file)
    class_names: list[str] = list(seed["class_schedule"].keys())

    # Generate schedule based on descriptor
    schedule = generate_schedule(
        datetime.fromisoformat(seed["start_date"]),
        int(seed["week_count"]),
        seed["class_schedule"],
    )

    # Load the holidays list
    holiday_list = pd.read_csv(holiday_file)
    holiday_list["start"] = pd.to_datetime(holiday_list["start"])
    holiday_list["end"] = pd.to_datetime(holiday_list["end"])

    # Join the schedule with the holidays list
    filtered_schedule = filter_holidays(schedule, holiday_list, class_names)

    # Additional formatting to clean the results
    filtered_schedule = format_result(filtered_schedule, not drop_dates, class_names)

    # Pretty-print output file name
    if "." not in output_path:
        output_path = f"{output_path}.{output_format.value}"

    write_df(filtered_schedule, output_path, output_format, index=False)
