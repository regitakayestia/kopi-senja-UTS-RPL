'use strict';
/** Lapisan HTTP: POST /api/pesanan/:noPesanan/bayar (hak akses: KASIR, PELANGGAN). */
class PembayaranController {
  constructor(pembayaranService) { this.service = pembayaranService; }
  async bayar(req, res) {
    // TODO: validasi input, panggil service.bayar(...), kembalikan struk
    res.status(501).json({ pesan: 'Belum diimplementasikan' });
  }
}
module.exports = PembayaranController;
