import glob
from enum import Enum
import csv
import pandas as pd

QUOTE_STRINGS = getattr(csv, "QUOTE_STRINGS", csv.QUOTE_NONNUMERIC)


class DfInFormat(Enum):
    CSV = "csv"
    JSON = "json"
    Excel = "xlsx"
    EMPTY = ""

    def __str__(self):
        return self.value


class DfOutFormat(Enum):
    CSV = "csv"
    JSON = "json"
    Excel = "xlsx"
    Markdown = "md"
    EMPTY = ""

    def __str__(self):
        return self.value


def get_extension(file_path: str) -> str:
    parts = file_path.rpartition(".")
    # no separator with the dot "." for extension, return empty
    if parts[0] == "":
        return ""
    return parts[-1]


def read_glob_df(glob_str: str, recursive: bool = False):
    paths = glob.glob(glob_str, recursive=recursive)
    return [read_df(_path) for _path in paths]


def read_df(file_path: str, file_format: DfInFormat | None = None, dtype: dict = {}, **kwargs):
    if file_format is None:
        file_format = DfInFormat(get_extension(file_path))
    match file_format:
        case DfInFormat.CSV:
            try:
                df = pd.read_csv(file_path, dtype=dtype, **kwargs)
            except UnicodeDecodeError:
                last_exc = None
                for enc in ("utf-8", "cp1252", "latin-1"):
                    try:
                        df = pd.read_csv(file_path, dtype=dtype, encoding=enc, **kwargs)
                        break
                    except UnicodeDecodeError as e:
                        last_exc = e
                else:
                    # re-raise the last UnicodeDecodeError if none worked
                    raise last_exc
        case DfInFormat.JSON:
            df = pd.read_json(file_path, dtype=dtype)
        case DfInFormat.Excel:
            df = pd.read_excel(file_path, dtype=dtype)
        case _:
            raise TypeError("file format not supported")
    return df


def write_df(
    df: pd.DataFrame,
    output_path: str,
    file_format: DfOutFormat | None = None,
    index: bool = True,
    **kwargs,
):
    if file_format is None:
        file_format = DfOutFormat(get_extension(output_path))
    match file_format:
        case DfOutFormat.CSV:
            df.to_csv(output_path, index=index, quoting=QUOTE_STRINGS, **kwargs)
        case DfOutFormat.JSON:
            df.to_json(output_path, index=index, **kwargs)
        case DfOutFormat.Excel:
            df.to_excel(output_path, index=index, **kwargs)
        case DfOutFormat.Markdown:
            df.to_markdown(output_path, index=index)
        case _:
            df.to_csv(
                f"{output_path}.csv", index=index, quoting=QUOTE_STRINGS, **kwargs
            )
