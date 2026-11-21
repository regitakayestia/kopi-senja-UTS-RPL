-- =====================================================================
-- Laporan penjualan HARIAN per cabang (Soal 6b)
-- Hanya pesanan yang sudah dibayar. Total dihitung dari detail_pesanan
-- (qty x harga_satuan) dikurangi potongan promo.
-- =====================================================================
USE kopi_senja;

WITH total_pesanan AS (
  SELECT p.no_pesanan,
         p.id_cabang,
         DATE(p.waktu_pesan)                  AS tanggal,
         SUM(d.qty * d.harga_satuan) - p.potongan AS total_bersih
  FROM pesanan p
  JOIN detail_pesanan d ON d.no_pesanan = p.no_pesanan
  WHERE p.status IN ('DIBAYAR','DIPROSES','SIAP','SELESAI')
  GROUP BY p.no_pesanan, p.id_cabang, DATE(p.waktu_pesan), p.potongan
)
SELECT c.nama_cabang,
       t.tanggal,
       COUNT(*)            AS jumlah_pesanan,
       SUM(t.total_bersih) AS total_penjualan
FROM total_pesanan t
JOIN cabang c ON c.id_cabang = t.id_cabang
GROUP BY c.nama_cabang, t.tanggal
ORDER BY t.tanggal, c.nama_cabang;

-- Varian BULANAN: ganti kolom tanggal dengan DATE_FORMAT(p.waktu_pesan, '%Y-%m')
-- pada CTE dan pada SELECT/GROUP BY di atas.

-- =====================================================================
-- Peringatan stok minimum (dipakai Manajer Cabang sebelum kedai buka)
-- =====================================================================
SELECT c.nama_cabang, b.nama_bahan, s.jumlah_stok, s.stok_minimum, b.satuan
FROM stok_cabang s
JOIN cabang c ON c.id_cabang = s.id_cabang
JOIN bahan  b ON b.id_bahan  = s.id_bahan
WHERE s.jumlah_stok <= s.stok_minimum
ORDER BY c.nama_cabang, b.nama_bahan;
