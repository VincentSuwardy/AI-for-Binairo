# AIF234001/AIF234002 Tugas Akhir 

### [LNV5903] AI for Binairo

**Dibuat oleh:** Vincent Emmanuel Suwardy / 6182201067

**Dosen pembimbing:** Lionov Ph.D

## Deskripsi

[**Binairo**](https://www.puzzle-binairo.com/) also known as **Takuzu** is a logic puzzle with simple rules and challenging solutions.

**The rules** are _simple_. Binairo is played on a rectangular grid with no standard size. Some cells start out filled with black or white circles. The rest of the cells are empty. The goal is to place circles in all cells in such a way that:
1. Each row and each column must contain an equal number of white and black circles.
2. More than two circles of the same color can't be adjacent.
3. Each row and column is unique.

## Struktur

- **Main.py**:
- **WebIterator.py**:
- **Constraint.py**:

## Cara Menjalankan

1. Pastikan sudah melakukan install untuk library `selenium`
   Jika belum, lakukan instalasi menggunakan **Command Prompt (CMD)** dengan cara berikut:

   ```bash
   pip install selenium
   ```

   Jika `python` yang digunakan adalah versi 3.x:

   ```bash
   python -m pip install selenium
   ``` 

2. Jalankan program dengan cara:

    ```bash
    python Main.py
    ```

3. Hasil retreive puzzle akan disimpan pada folder (`./Data/{size}{difficulty}/{id}.txt`) dan hasil jawaban solver akan disimpan pada folder (`./Asnwer/{size}{difficulty}/{id}.txt`)
   Jika folder tidak tersedia, program akan secara otomatis membuatkan folder untuk menyimpan `.txt`