# AIF234001/AIF234002 Tugas Akhir 

### [LNV5903ACS] AI for Binairo

**Dibuat oleh:** Vincent Emmanuel Suwardy / 6182201067  
**Dosen pembimbing:** Lionov, S.Kom., M.Sc., Ph.D.

## Deskripsi

[**Binairo**](https://www.puzzle-binairo.com/), juga dikenal **Takuzu**, adalah puzzle logika dengan aturan sederhana namun menantang untuk diselesaikan.

**Aturan**  
Binairo dimainkan pada papan berbentuk persegi panjang dengan ukuran yang bervariasi. Beberapa sel sudah diisi dengan lingkaran hitam atau putih, sementara sisanya kosong. Tujuan permainan adalah mengisi semua sel sehingga:
1. Setiap baris dan kolom memiliki jumlah lingkaran putih dan hitam yang sama.
2. Tidak ada lebih dari dua lingkaran dengan warna yang sama yang berdampingan.
3. Setiap baris dan kolom bersifat unik.

## Struktur Program

- **Main.py**: file utama yang dijalankan untuk memulai proses pengambilan puzzle dari website, menerapkan _preprocessing_ dengan pola yang sudah didefinisikan, dan menjalankan solver untuk menyelesaikan puzzle.
- **WebIterator.py**: perangkat lunak yang sebelumnya telah dikembangkan oleh _Edo Farrell Haryanto_, dengan sedikit penyesuaian agar bisa digunakan untuk website Binairo.
- **Constraint.py**: berisi pola-pola (_patterns_) yang akan digunakan untuk _pre-filling_ atau _preprocessing_ puzzle sebelum diselesaikan oleh solver.

## Cara Menjalankan

1. Pastikan library `selenium` sudah terinstal.
   Jika belum, lakukan instalasi melalui **Command Prompt (CMD)** dengan perintah:

   ```bash
   pip install selenium
   ```

   Atau jika `python` versi 3.x:

   ```bash
   python -m pip install selenium
   ``` 

2. Pada `Main.py`, sesuaikan nilai variabel `PUZZLE_SIZE` dan `PUZZLE_DIFF` sesuai ukuran dan tingkat kesulitan puzzle yang ingin dijalankan.

3. Jalankan program dengan perintah:

    ```bash
    python Main.py
    ```

4. Hasil pengambilan puzzle akan disimpan pada folder (`./Data/{size}{difficulty}/{id}.txt`), sedangkan hasil jawaban solver akan disimpan pada folder (`./Answer/{size}{difficulty}/{id}.txt`), dimana 
   - `{size}` adalah ukuran puzzle, 
   - `{difficulty}` adalah tingkat kesulitan puzzle, dan 
   - `{id}` adalah id puzzle.   
Jika folder belum tersedia, program akan membuatnya secara otomatis.