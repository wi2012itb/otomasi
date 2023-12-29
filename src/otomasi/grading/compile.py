from enum import Enum
import pandas as pd

from otomasi.utilities.files import read_df, write_df


class JoinMethod(Enum):
    LEFT = "left"
    RIGHT = "right"
    OUTER = "outer"
    INNER = "inner"

    def __str__(self):
        return self.value


def combine_dataframes(
    master: pd.DataFrame,
    inputs: list[pd.DataFrame],
    join_key: str,
    how: JoinMethod,
    concat: bool,
) -> pd.DataFrame:
    _master = master.set_index(join_key)
    _inputs = [input.set_index(join_key) for input in inputs]

    if concat:
        _inputs = pd.concat(_inputs)

    return _master.join(_inputs, how=how.value)


def main(
    master: str,
    inputs: list[str],
    out: str,
    join_key: str,
    how: JoinMethod = JoinMethod.LEFT,
    concat: bool = False,
):
    cast_dtype = {join_key: "string"}
    master_df = read_df(master, dtype=cast_dtype)
    inputs_df = [read_df(input, dtype=cast_dtype) for input in inputs]

    compiled_df = combine_dataframes(master_df, inputs_df, join_key, how, concat)

    index_counts = compiled_df.index.value_counts()
    duplicate_counts = index_counts[index_counts > 1]
    if duplicate_counts.count() > 0:
        print("warning: duplicates found. ignore this if this is expected")
        print(duplicate_counts.to_string())

    write_df(compiled_df, out)
