import pandas as pd

# generate list hadir di WI2012 dan di Akademik ITB
csv_hadir = "2025-03-05 22-46-15.csv"
csv_itb = "2025-03-05 22-51-43.csv"

hadir_raw = pd.read_csv(csv_hadir, sep="\t")
itb_raw = pd.read_csv(csv_itb, header=None)

prodi_hadir = hadir_raw.drop_duplicates(subset="PRODI")

prodi_itb = pd.DataFrame(columns=["FAKULTAS", "PRODI"])

for item in itb_raw[0]:
    if "Fakultas" in item or "Sekolah" in item:
        fak = item.split(" ")[-1].replace("(", "").replace(")", "")
    else:
        prodi = item.split("(")[0][:-1]
        new_row = pd.DataFrame({"FAKULTAS": [fak], "PRODI": [prodi]})
        prodi_itb = pd.concat([prodi_itb, new_row], ignore_index=True)

prodi_hadir.to_csv("prodi_hadir.csv", index=False)
prodi_itb.to_csv("prodi_itb.csv", index=False)