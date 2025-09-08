from typing import Tuple
import pandas as pd


def find_anchor(df: pd.DataFrame, anchor: str) -> Tuple[int, int]:
    anchor_loc = df[df.eq(anchor)].dropna(axis=1, how="all").dropna(how="all")
    return (anchor_loc.index.item(), df.columns.get_loc(anchor_loc.columns.item()))  # type: ignore


def extract_table(
    df: pd.DataFrame,
    headers: list | None = None,
    start_row: int = 0,
    start_col: int = 0,
) -> pd.DataFrame:
    """
    Extract a structured Dataframe with headers from an unstructured Dataframe

    Parameters
    ----------
    df:
        The unstructured Dataframe to be processed
    headers: default None
        If headers is supplied, the function will assume that the start_row and start_col denotes the start of the data in the table.
        Otherwise, the function will assume that the first row is a one row header, and proceed to extract
    """
    if headers is None:
        headers = df.iloc[start_row : start_row + 1, start_col:].astype("string").ffill(axis=1).fillna("").values.tolist()[0]  # type: ignore
        assert headers is not None
        max_col_length = len(df.iloc[start_row:, start_col:].columns)
        headers = headers[0:max_col_length]
        # Increment starting row since first row is used for headers
        start_row = start_row + 1
    return df.iloc[start_row:, start_col:].set_axis(headers, axis=1)
