'use strict';
/** Akses data tabel `pesanan` & `detail_pesanan`. Hanya berisi SQL, tanpa aturan bisnis. */
class PesananRepository {
  constructor(db) { this.db = db; }
  async simpan(pesanan)        { /* TODO: INSERT pesanan + detail dalam satu transaksi */ }
  async cariByNo(noPesanan)    { /* TODO: SELECT ... WHERE no_pesanan = ? */ }
  async antreanCabang(idCabang){ /* TODO: SELECT pesanan berstatus DIBAYAR/DIPROSES */ }
}
module.exports = PesananRepository;
