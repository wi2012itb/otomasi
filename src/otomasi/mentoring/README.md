# Mentoring administration scripts
This repository contains script and configuration to manage Mentoring related administration tasks.

## [Group Assignment](assign_groups.py)
Use the script to group class participants into groups of specified size.

To use, supply class participants data in CSV format with the following columns:

`NIM, NAMA, FAKULTAS, PRODI, KELAS, KELOMPOK`

Where `KELOMPOK` uses the Gender of class participant for grouping.
To run the script, use the command:

`python assign_groups.py {input_file_1} {input_file_2} ... [--out {output_filename}]`

example: `python assign_groups.py K1-2.csv K3.csv k4.csv k5.csv --out mentoring`

The input file is the CSV file to be supplied, and class being the mentoring class (Ganesha, Jatinangor, Cirebon).
The class will only be used for the file name, and serve no other purpose in processing (for now)

## [Generate list prodi](list_prodi_gen.py)
Obtain list from Fakultas dan Prodi from attendance sheet and Akademik ITB.

1. Use OneCommander or Notepad to paste the raw copy text from Akademik ITB
1. Modify the variable names of the files
1. run the program

To-do:

- automation of obtaining and concat of Fakultas and Prodi to a single csv from DPK raw csv