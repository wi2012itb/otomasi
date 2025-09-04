import re
from typing import Iterable

import pandas as pd

from otomasi.utilities.files import read_df, write_df

SPLIT_DELIMS = ["_", "-", " "]
SPLIT_DELIM_RE = "|".join(map(re.escape, SPLIT_DELIMS))
NIM_RE = re.compile(r"\d{8}")
SIT_IN_RE = re.compile(r"(?i)sit(_|-|\s)in")

NAME_COLUMN = "Name (original name)"
DURATION_COLUMNS = {"Duration (minutes)", "Total duration (minutes)"}


def get_duration_column(cols: Iterable[str]):
    for col in cols:
        if col in DURATION_COLUMNS:
            return col


def extract_NIM(x: str):
    match = NIM_RE.search(x)
    if match:
        return match.group()
    else:
        return x


def is_sit_in(x: str):
    match = SIT_IN_RE.search(x)
    if match:
        return match.group()
    else:
        return None


def main(filename: str, out: str, threshold: int = 80):
    df: pd.DataFrame = read_df(filename)
    # Filter column based on the type of file exported from Zoom report
    duration_col_name = get_duration_column(df.columns)

    # Aggregate total duration of user in the meeting
    df["Identifier"] = df[NAME_COLUMN].apply(extract_NIM)
    if duration_col_name is None:
        raise ValueError(
            f"No duration column detected, check if sheet contains one of the following: {DURATION_COLUMNS}"
        )

    groups = df.groupby(["Identifier"])
    df_grouped = groups[duration_col_name].sum().reset_index()
    df_grouped = pd.merge(
        df_grouped, groups.head(1)[["Identifier", NAME_COLUMN]], on="Identifier"
    )

    # Check if sit in
    df_grouped["Sit in"] = df_grouped[NAME_COLUMN].apply(is_sit_in)

    # Evaluate the attendance status based on minimum duration required for attendance
    new_thresh = (
        df_grouped[duration_col_name].average() if threshold == -1 else threshold
    )
    df_grouped["Attendance"] = df_grouped[duration_col_name].apply(
        lambda x: "H" if x >= new_thresh else None
    )

    write_df(df_grouped, out, index=False)
