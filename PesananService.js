'use strict';
/** Aturan bisnis pemesanan: validasi menu aktif & tersedia, promo, penomoran pesanan. */
class PesananService {
  constructor({ pesananRepo }) { this.pesananRepo = pesananRepo; }
  async buatPesanan(data) { /* TODO */ throw new Error('Belum diimplementasikan'); }
}
module.exports = PesananService;
