import argparse
import os

from config import *

if __name__ == "__main__":
    arg_in = argparse.ArgumentParser()
    arg_in.add_argument("source_filename", type=str)
    arg_in.add_argument("update_filename", type=str)
    arg_in.add_argument("--o", type=str, help="output filename", default="updated_data.csv")

    args = arg_in.parse_args()
    
    SOURCE_FILENAME = args.source_filename
    UPDATE_FILENAME = args.update_filename
    OUTPUT_FILENAME = args.o

    CWD = os.getcwd()

    # read data
    filepath = os.path.join(CWD, SOURCE_FILENAME)
    if not(os.path.exists(filepath)):
        print("file not found.")
        exit(-1)

    match_data: dict[str, list] = dict()
    with open(filepath, "r", encoding=FILE_ENCODING) as data_file:
        data_file.readline()
        for read_row in data_file:
            # print(row)
            row = read_row.split(sep=FILE_DELIMITER)
            
            key = row[DATA_KEY_COL]
            match_data[key] = row

    # read validate data
    validate_filepath = os.path.join(CWD, UPDATE_FILENAME)
    if not(os.path.exists(validate_filepath)):
        print("validation file not found.")
        exit(-1)

    # create difference file
    with open (OUTPUT_FILENAME, "w+") as out_file:
        out_file.write("No,NIM,Nama,Kelas SIX,Kuliah,Lokasi UTS\n")
    
    with open(validate_filepath, "r", encoding=FILE_ENCODING) as validate_file:
        with open (OUTPUT_FILENAME, "a", encoding=FILE_ENCODING) as out_file:
                validate_file.readline()
                for row in validate_file:
                    tmp_row = row.split(sep=FILE_DELIMITER)

                    key = tmp_row[UPDATE_KEY_COL]
                    
                    try:
                        for i in range(len(UPDATE_TARGET_COLS)):
                            match_data[key][UPDATE_TARGET_COLS[i]] = tmp_row[UPDATE_SOURCE_COLS[i]]
                    except KeyError:
                        print(f"{key} not found")
                        # out_file.write(f"{val_nim};{val_name};NULL;{val_score}\n")

    with open (OUTPUT_FILENAME, "a", encoding=FILE_ENCODING) as out_file:
        for key, row in match_data.items():
            out_row = FILE_DELIMITER.join(row)
            out_file.write(f"{out_row}")