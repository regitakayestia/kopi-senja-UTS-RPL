# Kopi Senja — Sistem Informasi Pemesanan dan Persediaan

Proyek UTS **Rekayasa Perangkat Lunak** · S1 Sistem Informasi · Semester Ganjil 2026/2027.
Disusun oleh: Regita Kayestia
## Tujuan

Sistem ini menggantikan pencatatan kertas dan hitung stok manual dengan aplikasi web untuk:

- pemesanan oleh Pelanggan (dari rumah) dan Kasir (di kedai);
- pembayaran tunai dan QRIS (simulasi);
- pengurangan stok bahan otomatis berdasarkan resep menu;
- peringatan stok minimum sebelum kedai buka;
- antrean pesanan untuk Barista;
- laporan penjualan harian dan bulanan per cabang.

## Aktor

| Aktor | Peran singkat |
|---|---|
| Pelanggan | Memesan, membayar, memantau status pesanan |
| Kasir | Menginput pesanan, menerapkan promo, menerima pembayaran |
| Barista | Melihat antrean dan memperbarui status pesanan |
| Manajer Cabang | Mengelola menu/resep/promo, memantau stok, laporan cabang |
| Pemilik | Melihat laporan seluruh cabang |
| Layanan QRIS (eksternal) | Pembayaran QRIS simulasi |

## Struktur folder

```
kopi-senja/
├─ docs/
│  ├─ srs/SRS-KopiSenja.md        SRS mini (kebutuhan FR/NFR, matriks, ambiguitas)
│  └─ diagrams/                   diagram (PNG/SVG) + sumber di diagrams/src
│     ├─ 03a-usecase · 03c-activity
│     ├─ 04-class · 06-sequence-pembayaran-stok
│     └─ 05-erd · 05-arsitektur
├─ src/
│  ├─ models/        kelas domain (Pesanan, Pembayaran, StokBahan, Resep, ...)
│  ├─ controllers/   lapisan HTTP (stub)
│  ├─ services/      aturan bisnis (stub)
│  └─ repositories/  akses data (stub)
├─ database/
│  ├─ schema.sql                      11 tabel MySQL dari ERD final
│  ├─ seed.sql                        data contoh (nota N-0012 dan N-0013)
│  └─ query_laporan_penjualan.sql     laporan penjualan per cabang + stok minimum
├─ test/smoke.js                      uji asap logika dasar
├─ .env.example · .gitignore · package.json
└─ README.md
```

## Cara menjalankan

Prasyarat: **MySQL 8** dan **Node.js 18+**.

```bash
# 1. Buat database, tabel, dan data contoh
mysql -u root -p < database/schema.sql
mysql -u root -p < database/seed.sql

# 2. Jalankan query laporan penjualan per cabang
mysql -u root -p < database/query_laporan_penjualan.sql
# Hasil contoh: Dago | 2026-11-03 | 2 pesanan | 88000

# 3. Uji asap logika model (tanpa database)
npm test
```

Salin `.env.example` menjadi `.env` untuk konfigurasi koneksi; berkas `.env` tidak di-commit.

## Status

Implementasi awal (UTS): skema database lengkap, model domain dengan logika dasar, dan kerangka (stub) controller/service/repository. Logika penuh dan antarmuka web dikerjakan pada sprint berikutnya (lihat Product Backlog pada dokumen jawaban UTS).

## Konvensi

- Penamaan tabel/kolom: `snake_case` bahasa Indonesia; kelas: `PascalCase`; metode: `camelCase`.
- Pesan commit: `jenis(cakupan): ringkasan` — contoh `feat(database): ...`, `docs: ...`.
- Kata sandi hanya disimpan sebagai hash; rahasia konfigurasi tidak pernah di-commit.
