# Admin Panel Finder

Admin Panel Finder adalah sebuah tool Python untuk menemukan halaman login admin pada sebuah website dengan menjelajahi seluruh tautan yang ada di dalamnya. Tool ini berguna untuk pengujian keamanan dan analisis struktur website.

## 🚀 Fitur
- Menjelajahi seluruh halaman website untuk mencari halaman login.
- Menggunakan multi-threading untuk efisiensi pencarian.
- Memeriksa form login berdasarkan kata kunci umum seperti "admin", "dashboard", "username", dan "password".
- Menghindari domain eksternal untuk fokus hanya pada target yang ditentukan.
- Menggunakan berbagai User-Agent secara acak untuk menghindari deteksi firewall.

## 🛠 Instalasi
Pastikan Anda memiliki Python 3.x terinstal di sistem Anda. Kemudian, install dependensi yang diperlukan dengan perintah berikut:

```sh
pip install requests beautifulsoup4
```

## 🔥 Cara Penggunaan
Jalankan skrip dengan perintah berikut:

```sh
python main.py
```

Kemudian masukkan URL target (contoh: `http://example.com`), dan tool akan mulai menjelajahi website tersebut untuk mencari halaman login admin.

## 📌 Contoh Output
```
➜ python main.py
Masukkan URL target (contoh: http://example.com): https://situscontoh.com/
[!] Menjelajahi https://situscontoh.com/ untuk mencari halaman login...
[+] Halaman login ditemukan: https://situscontoh.com/admin/login.php
[+] Halaman login ditemukan: https://situscontoh.com/dashboard/
[!] Pencarian selesai.
```

## ⚠️ Catatan
- Tool ini hanya untuk tujuan edukasi dan pengujian keamanan yang sah.
- Gunakan dengan izin dari pemilik website.
- Tidak diperbolehkan digunakan untuk aktivitas ilegal atau peretasan tanpa izin.

## 📜 Lisensi
Proyek ini berlisensi di bawah [MIT License](LICENSE).

---

✨ **Dibuat dengan Python dan semangat eksplorasi!** 🚀