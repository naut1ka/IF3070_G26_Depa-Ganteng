# IF3070_G26_Depa-Ganteng

Ini merupakan repositori untuk Tugas Besar 1 IF3070 Dasar Inteligensi Artifisial group 26

Program pada repositori ini dibuat untuk mencari susunan kendaraan pada kapal menggunakan Genetic Algorithm, Simulated Annealing, dan beberapa varian Hill Climbing. Program menampilkan state awal dan akhir, nilai objective, serta plot hasil pencarian.

## Setup dan Cara Menjalankan Program

Pastikan Python 3.10 atau lebih baru dan Matplotlib sudah terpasang.

Pilih algoritma melalui menu terminal. Untuk Genetic Algorithm, masukkan jumlah populasi dan banyak iterasi saat diminta. Setiap hasil eksekusi disimpan sebagai `result.json` dan `plot.png` di folder dalam `output/`.

## Pembagian Tugas

Pembagian berikut merangkum area kontribusi utama berdasarkan implementasi dan riwayat repository:

| Anggota (handle repository) | Tanggung jawab utama |
|---|---|
| 18224077 - Naufalziyadh Alif Bintang S. (`ItsOxiris`) | Kerangka repo (struktur folder MVC, .gitignore, main.py). entities.py (representasi data, effective_size, occupied_cells). neighbor.py (rotate, move, swap). initial.py (initial_state). simulated_annealing.py (Simulated Annealing), generate.py (data generator).  |
| 18224099 - Muhammad Afif Habiburrahman (`naut1ka`) | Mengimplementasikan dan ideasi genetic.py, main.py, Folder view. |
| 18224111 - Raditya Nanda Dhevara (`rndheva`) | Implementasi validation.py, objective.py, Steepest Ascent (hc_steepest.py), Sideways Move (hc_sideways.py), dan Random Restart Hill Climbing (hc_random.py). |
