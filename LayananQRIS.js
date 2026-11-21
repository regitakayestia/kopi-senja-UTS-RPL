'use strict';
/** Pembungkus layanan pembayaran eksternal (simulasi/sandbox). */
class LayananQRIS {
  buatKodeQris(total) { /* TODO: panggil API sandbox */ throw new Error('Belum diimplementasikan'); }
  verifikasi(kodeQris) { /* TODO: cek status pembayaran */ throw new Error('Belum diimplementasikan'); }
}
module.exports = LayananQRIS;
