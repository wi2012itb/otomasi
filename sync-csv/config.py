# Configuration for updating a CSV file's columns from
# another CSV file's columns based on its key column

FILE_ENCODING = 'UTF-8'

FILE_DELIMITER = ','

'''
USES 0 INDEXING FOR COLUMNS
'''

# No,NIM,Nama,Kelas SIX,Kuliah,Lokasi UTS
# the key column to match both file's row
DATA_KEY_COL = 1
# the columns that are to be updated with values from new target
UPDATE_TARGET_COLS = [4]

# No.,NIM,Nama,SIX,Kuliah,STATUS
# the key column to match both file's row
UPDATE_KEY_COL = 1
# the columns that are to be used to update the target values of the columns
UPDATE_SOURCE_COLS = [4]