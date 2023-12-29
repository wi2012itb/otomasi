import argparse
import re
import pandas as pd

SPLIT_DELIMS = ["_", "-", " "]
SPLIT_DELIM_RE = "|".join(map(re.escape, SPLIT_DELIMS))
NIM_RE = re.compile(r"^\d{8}$")

NAME_COLUMN = "Name (original name)"
DURATION_COLUMNS = {"Duration (minutes)", "Total duration (minutes)"}


def get_duration_column(cols: list[str]):
    for col in cols:
        if col in DURATION_COLUMNS:
            return col


def extract_NIM(x: str):
    try:
        _NIM_position = re.split(SPLIT_DELIM_RE, x)[1]
        match = NIM_RE.match(_NIM_position)
        if match:
            return _NIM_position
        else:
            return x
    except:
        return x


def main(filename: str, out: str, threshold: int = 80):
    df: pd.DataFrame = pd.read_csv(filename)
    # Filter column based on the type of file exported from Zoom report
    DURATION_COLUMN = get_duration_column(df.columns)

    # Aggregate total duration of user in the meeting
    df["Identifier"] = df[NAME_COLUMN].apply(extract_NIM)
    df = df.groupby(["Identifier"])[DURATION_COLUMN].sum().reset_index()

    # Evaluate the attendance status based on minimum duration required for attendance
    new_thresh = df[DURATION_COLUMN].average() if threshold == -1 else threshold
    df["Attendance"] = df[DURATION_COLUMN].apply(
        lambda x: "H" if x >= new_thresh else None
    )

    df.to_csv(out, index=False)
