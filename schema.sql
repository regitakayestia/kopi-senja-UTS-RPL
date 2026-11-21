-- =====================================================================
-- Kopi Senja — Skema Database (MySQL 8)
-- Sumber: ERD final (docs/diagrams/05-erd.png), hasil normalisasi 3NF.
-- Konvensi: nama tabel & kolom huruf kecil snake_case, bahasa Indonesia;
--           PK = id_* / kode_* / no_*; FK memakai nama kolom yang sama
--           dengan PK yang dirujuk.
-- =====================================================================
CREATE DATABASE IF NOT EXISTS kopi_senja
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE kopi_senja;

-- ---------- Master ----------
CREATE TABLE cabang (
  id_cabang    VARCHAR(10)  NOT NULL,
  nama_cabang  VARCHAR(50)  NOT NULL,
  alamat       VARCHAR(150) NULL,
  PRIMARY KEY (id_cabang)
) ENGINE=InnoDB;

-- Staf = Kasir, Barista, Manajer Cabang, Pemilik (generalisasi pada Class Diagram).
-- id_cabang boleh NULL karena Pemilik tidak terikat satu cabang.
CREATE TABLE staf (
  id_staf          VARCHAR(10)  NOT NULL,
  id_cabang        VARCHAR(10)  NULL,
  nama_staf        VARCHAR(80)  NOT NULL,
  email            VARCHAR(100) NOT NULL,
  kata_sandi_hash  VARCHAR(255) NOT NULL,           -- hash Argon2id/bcrypt, bukan teks asli
  peran            ENUM('KASIR','BARISTA','MANAJER','PEMILIK') NOT NULL,
  PRIMARY KEY (id_staf),
  UNIQUE KEY uq_staf_email (email),
  CONSTRAINT fk_staf_cabang FOREIGN KEY (id_cabang) REFERENCES cabang (id_cabang)
) ENGINE=InnoDB;

-- Data pelanggan dipisah dari transaksi (minimasi & pemisahan data, UU PDP).
CREATE TABLE pelanggan (
  id_pelanggan     VARCHAR(10)  NOT NULL,
  nama_pelanggan   VARCHAR(80)  NOT NULL,
  no_hp            VARCHAR(20)  NOT NULL,
  kata_sandi_hash  VARCHAR(255) NULL,
  PRIMARY KEY (id_pelanggan),
  UNIQUE KEY uq_pelanggan_no_hp (no_hp)
) ENGINE=InnoDB;

CREATE TABLE menu (
  kode_menu  VARCHAR(10)   NOT NULL,
  nama_menu  VARCHAR(80)   NOT NULL,
  kategori   VARCHAR(30)   NULL,
  harga      DECIMAL(10,2) NOT NULL CHECK (harga >= 0),
  aktif      BOOLEAN       NOT NULL DEFAULT TRUE,
  PRIMARY KEY (kode_menu)
) ENGINE=InnoDB;

CREATE TABLE promo (
  id_promo       VARCHAR(10)   NOT NULL,
  nama_promo     VARCHAR(80)   NOT NULL,
  jenis_diskon   ENUM('PERSEN','NOMINAL') NOT NULL,
  nilai_diskon   DECIMAL(10,2) NOT NULL CHECK (nilai_diskon >= 0),
  tgl_mulai      DATE NOT NULL,
  tgl_selesai    DATE NOT NULL,
  PRIMARY KEY (id_promo)
) ENGINE=InnoDB;

CREATE TABLE bahan (
  id_bahan    VARCHAR(10) NOT NULL,
  nama_bahan  VARCHAR(80) NOT NULL,
  satuan      VARCHAR(15) NOT NULL,                  -- gram, ml, pcs
  PRIMARY KEY (id_bahan)
) ENGINE=InnoDB;

-- ---------- Transaksi ----------
-- pesanan = Nota Penjualan pada dokumen lama (No_Nota -> no_pesanan).
-- Total tidak disimpan: atribut turunan, dihitung dari detail_pesanan (3NF).
CREATE TABLE pesanan (
  no_pesanan    VARCHAR(20)   NOT NULL,
  waktu_pesan   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  id_cabang     VARCHAR(10)   NOT NULL,
  id_staf       VARCHAR(10)   NULL,                  -- kasir; NULL bila pesanan online
  id_pelanggan  VARCHAR(10)   NULL,                  -- NULL bila pelanggan tanpa akun
  id_promo      VARCHAR(10)   NULL,
  saluran       ENUM('KASIR','ONLINE') NOT NULL,
  status        ENUM('MENUNGGU_BAYAR','DIBAYAR','DIPROSES','SIAP','SELESAI','DIBATALKAN')
                NOT NULL DEFAULT 'MENUNGGU_BAYAR',
  potongan      DECIMAL(10,2) NOT NULL DEFAULT 0,
  PRIMARY KEY (no_pesanan),
  KEY idx_pesanan_cabang_waktu (id_cabang, waktu_pesan),
  CONSTRAINT fk_pesanan_cabang    FOREIGN KEY (id_cabang)    REFERENCES cabang (id_cabang),
  CONSTRAINT fk_pesanan_staf      FOREIGN KEY (id_staf)      REFERENCES staf (id_staf),
  CONSTRAINT fk_pesanan_pelanggan FOREIGN KEY (id_pelanggan) REFERENCES pelanggan (id_pelanggan),
  CONSTRAINT fk_pesanan_promo     FOREIGN KEY (id_promo)     REFERENCES promo (id_promo)
) ENGINE=InnoDB;

-- harga_satuan = harga saat transaksi (snapshot) agar riwayat tidak berubah
-- ketika harga menu diubah.
CREATE TABLE detail_pesanan (
  no_pesanan    VARCHAR(20)   NOT NULL,
  kode_menu     VARCHAR(10)   NOT NULL,
  qty           INT           NOT NULL CHECK (qty > 0),
  harga_satuan  DECIMAL(10,2) NOT NULL,
  catatan       VARCHAR(150)  NULL,
  PRIMARY KEY (no_pesanan, kode_menu),
  CONSTRAINT fk_detail_pesanan FOREIGN KEY (no_pesanan) REFERENCES pesanan (no_pesanan) ON DELETE CASCADE,
  CONSTRAINT fk_detail_menu    FOREIGN KEY (kode_menu)  REFERENCES menu (kode_menu)
) ENGINE=InnoDB;

CREATE TABLE pembayaran (
  id_pembayaran  VARCHAR(20)   NOT NULL,
  no_pesanan     VARCHAR(20)   NOT NULL,
  metode         ENUM('TUNAI','QRIS') NOT NULL,
  jumlah_bayar   DECIMAL(10,2) NOT NULL,
  status         ENUM('BERHASIL','GAGAL') NOT NULL,
  waktu_bayar    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  ref_qris       VARCHAR(60)   NULL,
  PRIMARY KEY (id_pembayaran),
  UNIQUE KEY uq_pembayaran_pesanan (no_pesanan),     -- relasi 1 : 0..1
  CONSTRAINT fk_pembayaran_pesanan FOREIGN KEY (no_pesanan) REFERENCES pesanan (no_pesanan)
) ENGINE=InnoDB;

-- ---------- Persediaan ----------
-- stok per cabang; stok_minimum dipakai untuk peringatan sebelum kedai buka.
CREATE TABLE stok_cabang (
  id_cabang     VARCHAR(10)   NOT NULL,
  id_bahan      VARCHAR(10)   NOT NULL,
  jumlah_stok   DECIMAL(12,2) NOT NULL DEFAULT 0 CHECK (jumlah_stok >= 0),
  stok_minimum  DECIMAL(12,2) NOT NULL DEFAULT 0,
  PRIMARY KEY (id_cabang, id_bahan),
  CONSTRAINT fk_stok_cabang FOREIGN KEY (id_cabang) REFERENCES cabang (id_cabang),
  CONSTRAINT fk_stok_bahan  FOREIGN KEY (id_bahan)  REFERENCES bahan (id_bahan)
) ENGINE=InnoDB;

-- resep = penghubung M:N antara menu dan bahan.
CREATE TABLE resep (
  kode_menu  VARCHAR(10)   NOT NULL,
  id_bahan   VARCHAR(10)   NOT NULL,
  takaran    DECIMAL(10,2) NOT NULL CHECK (takaran > 0),
  PRIMARY KEY (kode_menu, id_bahan),
  CONSTRAINT fk_resep_menu  FOREIGN KEY (kode_menu) REFERENCES menu (kode_menu),
  CONSTRAINT fk_resep_bahan FOREIGN KEY (id_bahan)  REFERENCES bahan (id_bahan)
) ENGINE=InnoDB;
