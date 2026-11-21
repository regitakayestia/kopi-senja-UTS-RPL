'use strict';
/** Kelas Resep — padanan tabel `resep` (menu <-> bahan, takaran per porsi). */
class Resep {
  constructor({ kodeMenu, idBahan, takaran }) {
    this.kodeMenu = kodeMenu;
    this.idBahan = idBahan;
    this.takaran = takaran;
  }

  /** Kebutuhan bahan untuk `qty` porsi menu (Sequence Diagram pesan 10). */
  ambilKebutuhanBahan(kodeMenu, qty) {
    // TODO: ResepRepository.cariByMenu(kodeMenu) lalu kalikan takaran x qty
    throw new Error('Belum diimplementasikan');
  }
}
module.exports = Resep;
