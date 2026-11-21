'use strict';
/** Kelas Pembayaran — padanan tabel `pembayaran`. */
class Pembayaran {
  constructor({ idPembayaran, noPesanan, metode, total = 0, jumlahBayar = 0 }) {
    this.idPembayaran = idPembayaran;
    this.noPesanan = noPesanan;
    this.metode = metode;            // 'TUNAI' | 'QRIS'
    this.total = total;               // total tagihan pesanan
    this.jumlahBayar = jumlahBayar;
    this.status = 'GAGAL';           // menjadi 'BERHASIL' setelah proses() sukses
  }

  /**
   * Memproses pembayaran (Sequence Diagram pesan 3: proses).
   * @returns {string} 'BERHASIL' | 'GAGAL'
   */
  proses(noPesanan, metode, jumlah) {
    // TODO: metode QRIS -> LayananQRIS.buatKodeQris() lalu verifikasi();
    //       metode TUNAI -> hitungKembalian()
    throw new Error('Belum diimplementasikan');
  }

  /** Kembalian untuk pembayaran tunai (Sequence Diagram pesan 8). */
  hitungKembalian(jumlah) {
    return Math.max(jumlah - this.total, 0);
  }
}
module.exports = Pembayaran;
