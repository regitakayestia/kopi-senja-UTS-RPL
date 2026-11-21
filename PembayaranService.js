'use strict';
/**
 * Menyatukan alur Sequence Diagram "pesanan dibayar hingga stok bahan berkurang".
 * Seluruh langkah (tandai lunas + kurangi stok) harus berada dalam SATU transaksi
 * database agar stok tidak berubah bila pembayaran gagal.
 */
class PembayaranService {
  constructor({ pesananRepo, stokRepo, layananQris }) {
    Object.assign(this, { pesananRepo, stokRepo, layananQris });
  }
  /** @returns {Promise<{status:string}>} */
  async bayar(noPesanan, metode, jumlah) {
    // TODO: 1) hitung total  2) proses pembayaran  3) bila berhasil: tandaiLunas + kurangi stok
    throw new Error('Belum diimplementasikan');
  }
}
module.exports = PembayaranService;
