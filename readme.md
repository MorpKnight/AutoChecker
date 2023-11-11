# Instruksi
### Normal Usage
Untuk menjalankan program ini, pada `main.py` sudah disediakan contoh penggunaan. Untuk menjalankan program, cukup jalankan `main.py` dengan python3.6 atau lebih tinggi.

```python
from UnitTest import UnitTest

# Membuat objek UnitTest
# Parameter 1: Nama folder yang akan dijadikan sebagai test-case
inputTest = []
outputTest = []

# Runs a unit test using the `UnitTest` class with specified input and output tests.
# 
# Parameters:
# - `folderName`: the name of the folder containing the test files
# - `input_test`: the input test file name
# - `output_test`: the output test file name
#
# Returns:
# - Check generated result.txt and result.csv
checker = UnitTest("folderName", input_test=inputTest, output_test=outputTest)
checker.run()
```

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
- [x] Checking using regex
- [x] Auto degrade, ketika salah kode aslab
- [x] Auto 0, ketika terindikasi plagiarisme
- [x] Scrapping website untuk cek plagiarisme
- [ ] GUI
- [ ] Documentation
- [ ] Checking using tolerance
- [ ] Fix bug occurs when check plagiaisme about naming that doesn't match to plagiaism check