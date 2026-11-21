'use strict';
/** Lapisan HTTP: POST /api/pesanan (KASIR, PELANGGAN); GET /api/antrean (BARISTA). */
class PesananController {
  constructor(pesananService) { this.service = pesananService; }
  async buat(req, res)    { res.status(501).json({ pesan: 'Belum diimplementasikan' }); }
  async antrean(req, res) { res.status(501).json({ pesan: 'Belum diimplementasikan' }); }
}
module.exports = PesananController;
