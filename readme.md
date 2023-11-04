# Instruksi
### Normal Usage
Untuk menjalankan program ini, pada `main.py` sudah disediakan contoh penggunaan. Untuk menjalankan program, cukup jalankan `main.py` dengan python3.6 atau lebih tinggi.

```python
from UnitTest import UnitTest

# Membuat objek UnitTest
# Parameter 1: Nama folder yang akan dijadikan sebagai test-case
# Parameter 2: Nama file yang akan dijadikan sebagai program yang akan diujiS
```
```bash

### Input dan Output
Untuk bagian pengisian input dan output harap mengikuti ketentuan dibawah ini supaya file dapat dijalankan dengan baik.
```python
# Input
# Karena keterbatasan cara input, maka input diisi dalam bentuk list, 
# dan tiap elemen list dipisahkan dengan spasi untuk per test-case
inputTest = ["1 2 3 4 5"]
inputTest = ["1 2 3 4 5", "6 7 8 9 10"]

# Output
# Pembacaan output oleh Popen.communicate() akan menghasilkan byte,
# maka dari itu output diisi dalam bentuk string, dan tanpa spasi
outputTest = ["15"]
outputTest = ["15", "40"]
outputTest = ["Contohoutput1", "Contohoutput2"]
```
Program dapat dikostumisasi dengan membuat single file checker atau folder-based

# Things to add
- [x] Unit Test
- [x] Single File Checker
- [x] Folder-based Checker
- [ ] GUI
- [ ] Documentation
- [ ] Checking using regex
- [ ] Checking using tolerance
- [ ] Auto degrade, ketika salah kode aslab
- [ ] Auto 0, ketika terindikasi plagiarisme
- [ ] Scrapping website untuk cek plagiarisme