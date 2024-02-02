import argparse
import os

from config import NIM_SIX_COL, NIM_TARGET_COL

if __name__ == "__main__":
    arg_in = argparse.ArgumentParser()
    arg_in.add_argument("filename", type=str)
    arg_in.add_argument("--o", type=str, help="output filename", default="difference.csv")

    args = arg_in.parse_args()
    
    FILENAME = args.filename
    OUTPUT_FILENAME = args.o

    CWD = os.getcwd()

    # read data
    filepath = os.path.join(CWD, FILENAME)
    if not(os.path.exists(filepath)):
        print("file not found.")
        exit(-1)

    six_set = set()
    target_set = set()
    target_double = dict()
    
    with open(filepath, "r", encoding='UTF-8') as data_file:
        data_file.readline()
        for row in data_file:
            # print(row)
            tmp_row = row.split(sep=';')
            nim_six = tmp_row[NIM_SIX_COL]
            nim_target = tmp_row[NIM_TARGET_COL]
            if nim_six == '':
                pass
            else:
                six_set.add(nim_six)

            if nim_target == '':
                pass
            else:
                if (nim_target in target_set):
                    try:
                        target_double[nim_target] += 1
                    except KeyError:
                        target_double[nim_target] = 1
                else:
                    target_set.add(nim_target)

    # create difference file
    with open (OUTPUT_FILENAME, "w+") as out_file:
        out_file.write('')
    
    with open (OUTPUT_FILENAME, "a", encoding='UTF-8') as out_file:
            # write invalid NIM (found in NIM_target, but not in NIM_SIX)
            out_file.write("NIM_target_Invalid\n")
            invalid_set = target_set.difference(six_set)
            for nim in invalid_set:
                out_file.write(f"{nim}\n")

            # write missing NIM in SIX (which is not found in NIM_target)
            out_file.write("\nNIM_SIX_Missing\n")
            invalid_set = six_set.difference(target_set)
            for nim in invalid_set:
                out_file.write(f"{nim}\n")

            # write duplicate NIM in NIM_target
            out_file.write("\nNim_target_duplicate;Duplicate_count\n")
            for nim, count in target_double.items():
                out_file.write(f"{nim};{count}\n")
