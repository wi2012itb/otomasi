import glob
import itertools
import re
import pandas as pd

from otomasi.utilities.files import read_df, write_df
from otomasi.utilities.xlsx import extract_table, find_anchor

KELAS_RE = re.compile(r"No Kelas: (\d{2})")


def extract_data(df: pd.DataFrame, anchor: str):
    (row, col) = find_anchor(df, anchor)
    df_extracted = extract_table(df, start_row=row, start_col=col)
    match = KELAS_RE.search(str(df.iloc[3, 0]))
    if match:
        kelas = match.group(1)
        df_extracted["KELAS"] = f"K{kelas}"
        return df_extracted


def main(
    globs: list[str],
    out: str,
):
    # extract globs and flatten into path list
    paths_lists = [glob.glob(_glob, recursive=True) for _glob in globs]
    paths = list(itertools.chain(*paths_lists))

    # read dataframes
    df_inputs = [read_df(path) for path in paths]

    df_processed = [extract_data(df, "NO") for df in df_inputs]
    df_concat = pd.concat(df_processed)

    write_df(df_concat, out, index=False)
