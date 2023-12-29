import json
from argparse import FileType
import pandas as pd

from otomasi.utilities.files import read_df, write_df


def enforce_grade(
    data: pd.Series, upper_thresh: dict[str, int], score_col: str, index_col: str
):
    if pd.isna(data[score_col]) or pd.isna(data[index_col]):
        return pd.NA
    else:
        if data[score_col] < upper_thresh[data[index_col]]:
            # If original score is in range of the index, return as is
            return data[score_col]
        else:
            # Reduce score to -2 of the upper threshold
            enforced = upper_thresh[data[index_col]] - 2
            return enforced


def main(
    score_file: str,
    grade_config: FileType,
    score_col: str,
    index_col: str,
    output_path: str,
):
    grade_df = read_df(score_file)
    upper_thresh: dict[str, int] = json.load(grade_config)

    INDEX_SET = {"A", "AB", "B", "BC", "C", "D", "E"}
    if INDEX_SET != upper_thresh.keys():
        raise ValueError(f"Index must only contain {INDEX_SET}")

    grade_df["SCORE_ADJUSTED"] = grade_df.apply(
        lambda x: enforce_grade(x, upper_thresh, score_col, index_col), axis=1
    )

    write_df(grade_df, output_path, index=False)
