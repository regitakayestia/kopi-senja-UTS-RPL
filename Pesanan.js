'use strict';
/**
 * Kelas Pesanan — padanan tabel `pesanan` (Nota Penjualan).
 * Operasi mengikuti Class Diagram dan Sequence Diagram (hitungTotal, tandaiLunas).
 */
class Pesanan {
  /** @param {{noPesanan:string, idCabang:string, saluran:'KASIR'|'ONLINE'}} data */
  constructor({ noPesanan, idCabang, saluran, potongan = 0 }) {
    this.noPesanan = noPesanan;
    this.idCabang = idCabang;
    this.saluran = saluran;
    this.status = 'MENUNGGU_BAYAR';
    this.potongan = potongan;
    /** @type {Array<{kodeMenu:string, qty:number, hargaSatuan:number}>} */
    this.detail = [];
  }

  /** Menambah item menu ke pesanan. */
  tambahItem(kodeMenu, qty, hargaSatuan) {
    if (qty <= 0) throw new Error('qty harus lebih dari 0');
    this.detail.push({ kodeMenu, qty, hargaSatuan });
  }

  /** Total bersih = jumlah subtotal item dikurangi potongan promo. */
  hitungTotal() {
    const subtotal = this.detail.reduce((t, d) => t + d.qty * d.hargaSatuan, 0);
    return Math.max(subtotal - this.potongan, 0);
  }

  /** Dipanggil Pembayaran setelah pembayaran berhasil (Sequence Diagram pesan 9). */
  tandaiLunas() {
    this.status = 'DIBAYAR';
    // TODO: panggil StokService.kurangiStokPesanan(this) di dalam satu transaksi
  }

  /** Mengubah status: DIPROSES -> SIAP -> SELESAI (dipakai Barista). */
  ubahStatus(statusBaru) {
    // TODO: validasi urutan status yang diperbolehkan
    this.status = statusBaru;
  }
}
module.exports = Pesanan;
