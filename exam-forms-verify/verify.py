import argparse
import os

from config import *

class ExamDetail:
    def __init__(self, name: str, score: str) -> None:
        # self.nim = nim
        self.name = name
        self.score = score

if __name__ == "__main__":
    arg_in = argparse.ArgumentParser()
    arg_in.add_argument("filename", type=str)
    arg_in.add_argument("validate_filename", type=str)
    arg_in.add_argument("--o", type=str, help="output filename", default="difference.csv")

    args = arg_in.parse_args()
    
    FILENAME = args.filename
    VALIDATE_FILENAME = args.validate_filename
    OUTPUT_FILENAME = args.o

    CWD = os.getcwd()

    # read data
    filepath = os.path.join(CWD, FILENAME)
    if not(os.path.exists(filepath)):
        print("file not found.")
        exit(-1)

    match_data: dict[str, (ExamDetail, bool)] = dict()
    with open(filepath, "r", encoding=FILE_ENCODING) as data_file:
        data_file.readline()
        for read_row in data_file:
            # print(row)
            row = read_row.split(sep=';')
            
            nim = row[MATCH_NIM_COL]
            name = row[MATCH_NAME_COL]
            score = row[MATCH_SCORE_COL].strip()

            detail = ExamDetail(name, score)
            match_data[nim] = [detail, False]

    # read validate data
    validate_filepath = os.path.join(CWD, VALIDATE_FILENAME)
    if not(os.path.exists(validate_filepath)):
        print("validation file not found.")
        exit(-1)

    # create difference file
    with open (OUTPUT_FILENAME, "w+") as out_file:
        out_file.write("NIM;name;current score;original score\n")
    
    with open(validate_filepath, "r", encoding=FILE_ENCODING) as validate_file:
        with open (OUTPUT_FILENAME, "a", encoding=FILE_ENCODING) as out_file:
                validate_file.readline()
                for row in validate_file:
                    tmp_row = row.split(sep=';')
                    
                    val_nim = tmp_row[VALIDATE_NIM_COL]
                    val_name = tmp_row[VALIDATE_NAME_COL]
                    val_score = tmp_row[VALIDATE_SCORE_COL].strip()
                    try:
                        detail = match_data[val_nim][0]
                        if (str(detail.score) != str(val_score)):
                            # print(nim, name)
                            # Check if NIM has multiple entry
                            if match_data[val_nim][1]:
                                print(f"{val_nim} {val_name} has multiple entry in data!\n")
                                out_file.write(f"{val_nim};{val_name};NULL;NULL\n")
                            else:
                                out_file.write(f"{val_nim};{val_name};{detail.score};{val_score}\n")
                        match_data[val_nim][1] = True
                    except KeyError:
                        print(f"{val_nim} not found")
                        out_file.write(f"{val_nim};{val_name};NULL;{val_score}\n")

    # without assuming an entry that has score but doesn't have score in validate is inputted manually
    with open (OUTPUT_FILENAME, "a", encoding=FILE_ENCODING) as out_file:
        out_file.write("\n")
        for nim, row in match_data.items():
            if not row[1]:
                detail = row[0]
                name = detail.name
                score = detail.score
                out_file.write(f"{nim};{name};{score};NULL\n")