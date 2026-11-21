'use strict';
/** Akses data tabel `stok_cabang` dan `resep`. */
class StokRepository {
  constructor(db) { this.db = db; }
  async cariStok(idCabang, idBahan) { /* TODO */ }
  async simpanStok(stok)            { /* TODO: UPDATE stok_cabang SET jumlah_stok = ? */ }
  async bahanDiBawahMinimum(idCabang){ /* TODO: lihat database/query_laporan_penjualan.sql */ }
}
module.exports = StokRepository;
