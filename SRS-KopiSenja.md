# SRS Mini — Sistem Informasi Pemesanan dan Persediaan “Kopi Senja”

> Dokumen ini adalah ringkasan SRS dari jawaban UTS Rekayasa Perangkat Lunak (Soal 2). Seluruh nama dan data fiktif.

## 1. Tujuan dan ruang lingkup

Sistem web untuk pemesanan (Pelanggan dan Kasir), pembayaran (tunai dan QRIS simulasi), pengurangan stok otomatis berdasarkan resep, peringatan stok minimum, antrean untuk Barista, serta laporan penjualan harian/bulanan per cabang (3 cabang).

**Di luar lingkup:** pembayaran QRIS sungguhan, pengiriman, pembelian ke pemasok, penggajian, aplikasi mobile native.

## 2. Aktor

| Aktor | Peran |
|---|---|
| Pelanggan | Memesan, membayar QRIS, memantau status |
| Kasir | Menginput pesanan, promo, menerima pembayaran |
| Barista | Melihat antrean, memperbarui status |
| Manajer Cabang | Menu/resep/promo, stok, laporan cabang |
| Pemilik | Laporan seluruh cabang; Product Owner |
| Layanan QRIS (eksternal) | Membuat dan memverifikasi kode QRIS (simulasi) |

## 3. Asumsi dan batasan

- Jam operasional 07.00–22.00; resep sama di tiga cabang; Kasir bertugas di satu cabang.
- Aplikasi web + MySQL; QRIS hanya simulasi.
- Kepatuhan UU PDP 27/2022: minimasi data dan audit akses (NFR-05).

## 4. Kebutuhan fungsional

| Kode | Kebutuhan | Prioritas | Sumber |
|---|---|---|---|
| FR-01 | Sistem harus dapat mengautentikasi pengguna (login/logout) dan membatasi fitur berdasarkan peran: Pelanggan, Kasir, Barista, Manajer Cabang, Pemilik. | Tinggi | Semua pemangku kepentingan |
| FR-02 | Sistem harus dapat menampilkan daftar menu beserta harga dan ketersediaannya per cabang. | Tinggi | Pelanggan, Kasir |
| FR-03 | Sistem harus dapat membuat pesanan, baik oleh Kasir di kedai maupun oleh Pelanggan secara online, berisi menu, jumlah, dan catatan. | Tinggi | Pelanggan, Kasir |
| FR-04 | Sistem harus dapat menghitung subtotal, potongan promo, dan total pesanan secara otomatis. | Tinggi | Kasir |
| FR-05 | Sistem harus dapat memproses pembayaran tunai dan QRIS simulasi serta mencatat metode dan status pembayaran. | Tinggi | Kasir, Pelanggan |
| FR-06 | Sistem harus dapat mengurangi stok bahan baku secara otomatis berdasarkan resep menu setelah pembayaran berhasil. | Tinggi | Manajer Cabang, Pemilik |
| FR-07 | Sistem harus dapat menampilkan peringatan bahan yang stoknya sama dengan atau di bawah batas minimum kepada Manajer Cabang. | Tinggi | Manajer Cabang |
| FR-08 | Sistem harus dapat menampilkan antrean pesanan berurutan waktu kepada Barista dan memungkinkan Barista memperbarui status (Diproses, Siap). | Tinggi | Barista, Kasir |
| FR-09 | Sistem harus dapat menampilkan status pesanan kepada Pelanggan dan mengirim notifikasi ketika pesanan berstatus Siap. | Sedang | Pelanggan, Barista |
| FR-10 | Sistem harus dapat mengelola data menu, resep (takaran bahan per menu), dan promo oleh Manajer Cabang. | Sedang | Manajer Cabang, Pemilik, Kasir |
| FR-11 | Sistem harus dapat mencatat penerimaan bahan dan penyesuaian stok (stock opname) per cabang. | Sedang | Manajer Cabang |
| FR-12 | Sistem harus dapat menghasilkan laporan penjualan harian dan bulanan per cabang. | Tinggi | Manajer Cabang, Pemilik |
| FR-13 | Sistem harus dapat menampilkan ringkasan penjualan seluruh cabang kepada Pemilik kapan saja. | Tinggi | Pemilik |
| FR-14 | Sistem harus dapat menerbitkan nota/struk digital untuk setiap pesanan yang telah dibayar. | Sedang | Kasir, Pelanggan |

## 5. Kebutuhan non-fungsional (terukur)

| Kode | Aspek | Kebutuhan | Cara uji |
|---|---|---|---|
| NFR-01 | Kinerja | Halaman daftar menu dan antrean pesanan tampil ≤ 3 detik (persentil ke-95) untuk 50 pengguna bersamaan per cabang; penyimpanan pesanan selesai ≤ 2 detik. | Uji beban (k6/JMeter) pada staging |
| NFR-02 | Keamanan | Seluruh akses memakai HTTPS (TLS ≥ 1.2); kata sandi disimpan dengan hash Argon2id/bcrypt + salt unik; akses dibatasi peran (RBAC) dengan 100% kasus uji hak akses lulus (mis. Kasir tidak dapat membuka laporan seluruh cabang); akun terkunci 15 menit setelah 5 kali gagal login. | Uji hak akses, pemindaian TLS, uji penetrasi dasar |
| NFR-03 | Usability | Kasir baru dapat menyelesaikan pesanan 3 item sampai pembayaran ≤ 2 menit setelah pelatihan 15 menit; skor SUS ≥ 70 pada UAT dengan minimal 5 pengguna (Kasir/Barista). | UAT dengan lembar observasi dan kuesioner SUS |
| NFR-04 | Ketersediaan | Sistem tersedia ≥ 99% per bulan pada jam operasional kedai (asumsi 07.00–22.00, toleransi henti ≈ 4,5 jam/bulan); backup database harian dengan RPO ≤ 24 jam dan RTO ≤ 4 jam. | Pemantauan uptime; uji pemulihan backup tiap kuartal |
| NFR-05 | Privasi (UU PDP) | Data pelanggan yang dikumpulkan hanya nama dan nomor HP (Pasal 16); setiap akses staf ke data pelanggan tercatat di audit log aplikasi (100% akses tercatat); pelanggan dapat meminta penghapusan akun dan diproses ≤ 3×24 jam; bila terjadi kebocoran data, pemberitahuan ke pelanggan terdampak dikirim ≤ 72 jam (Pasal 46). | Tinjauan skema DB, uji skenario hapus akun, simulasi insiden (tabletop) |

## 6. Matriks kebutuhan–pemangku kepentingan

● utama, ○ terkait

| Kebutuhan | Pelanggan | Kasir | Barista | Manajer Cabang | Pemilik |
|---|:-:|:-:|:-:|:-:|:-:|
| FR-01 | ● | ● | ● | ● | ● |
| FR-02 | ● | ● |  |  |  |
| FR-03 | ● | ● |  |  |  |
| FR-04 |  | ● |  |  |  |
| FR-05 | ○ | ● |  |  |  |
| FR-06 |  |  |  | ● | ○ |
| FR-07 |  |  |  | ● |  |
| FR-08 |  | ○ | ● |  |  |
| FR-09 | ● | ○ |  |  |  |
| FR-10 |  | ○ |  | ● | ○ |
| FR-11 |  |  |  | ● |  |
| FR-12 |  |  |  | ● | ● |
| FR-13 |  |  |  |  | ● |
| FR-14 | ● | ○ |  |  |  |
| NFR-01 | ○ | ● | ● |  |  |
| NFR-02 | ○ |  |  | ● | ● |
| NFR-03 |  | ● | ● |  |  |
| NFR-04 |  | ○ |  | ○ | ● |
| NFR-05 | ● |  |  |  | ● |

## 7. Kebutuhan ambigu

1. **“Bahan yang hampir habis”** — batas belum ditentukan. Klarifikasi: wawancara Manajer + analisis catatan stok; usulan *stok minimum = pemakaian rata-rata 2 hari + cadangan*; persetujuan tertulis.
2. **“Promo”** — jenis, syarat, periode, dan kombinasi belum jelas. Klarifikasi: kumpulkan contoh promo, wawancara Pemilik, observasi Kasir; versi awal: PERSEN dan NOMINAL, satu promo per pesanan.
