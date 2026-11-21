'use strict';
/** Kelas StokBahan — padanan tabel `stok_cabang` (stok bahan per cabang). */
class StokBahan {
  constructor({ idCabang, idBahan, jumlahStok, stokMinimum }) {
    this.idCabang = idCabang;
    this.idBahan = idBahan;
    this.jumlahStok = jumlahStok;
    this.stokMinimum = stokMinimum;
  }

  /** Mengurangi stok dan mengembalikan stok baru (Sequence Diagram pesan 12). */
  kurangiStok(idBahan, jumlah) {
    if (jumlah > this.jumlahStok) throw new Error('Stok tidak cukup');
    this.jumlahStok -= jumlah;
    return this.jumlahStok;
  }

  tambahStok(idBahan, jumlah) { this.jumlahStok += jumlah; }

  /** true bila stok sudah di bawah/sama dengan batas minimum -> kirim peringatan. */
  cekStokMinimum() { return this.jumlahStok <= this.stokMinimum; }
}
module.exports = StokBahan;
