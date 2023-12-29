# Cek Hari Libur
Generator filter pertemuan-pertemuan kuliah yang membutuhkan kelas pengganti akibat hari libur

## Usage
1. Siapkan seed jadwal kuliah dengan format JSON, ikuti template [schedule_template.json](../../../config/calendar/schedule_template.json)
2. Siapkan list tanggal libur nasional dalam format CSV, ikuti template [holiday_template.csv](../../../config/calendar/holiday_template.csv)
3. Jalankan script, masukkan file seed dan list hari libur yang telah disiapkan sebagai parameter
```
py holiday_summary.py {file seed JSON} {file list libur CSV} [-o {lokasi file output}] [--out-format {csv,md,xlsx}] [--drop-dates]
```
4. Jalankan `py holiday_summary.py -h` untuk melihat daftar perintah yang dapat digunakan
