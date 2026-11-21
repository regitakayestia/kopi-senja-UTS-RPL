'use strict';
/** Kelas ManajerCabang (turunan Staf). */
class ManajerCabang {
  /** Menerima peringatan stok minimum (Sequence Diagram pesan 14). */
  terimaPeringatanStok(namaBahan, sisa) {
    // TODO: simpan ke daftar peringatan agar tampil di dashboard sebelum kedai buka
    console.warn(`[PERINGATAN] Stok ${namaBahan} tinggal ${sisa}`);
  }
}
module.exports = ManajerCabang;
