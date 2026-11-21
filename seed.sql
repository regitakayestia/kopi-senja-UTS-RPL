-- Data contoh (fiktif) dari soal UTS: nota N-0012 cabang Dago.
USE kopi_senja;

INSERT INTO cabang VALUES ('C01','Dago','Jl. Dago (fiktif)'),('C02','Braga','Jl. Braga (fiktif)'),('C03','Buah Batu','Jl. Buah Batu (fiktif)');
INSERT INTO staf VALUES
 ('S01','C01','Sari','sari@kopisenja.example','$argon2id$contoh','KASIR'),
 ('S02','C01','Rudi','rudi@kopisenja.example','$argon2id$contoh','BARISTA'),
 ('S03','C01','Maya','maya@kopisenja.example','$argon2id$contoh','MANAJER'),
 ('S04',NULL ,'Pak Hadi','pemilik@kopisenja.example','$argon2id$contoh','PEMILIK');
INSERT INTO pelanggan VALUES ('P01','Budi','0812xxxx',NULL),('P02','Dewi','0813xxxx',NULL);
INSERT INTO menu VALUES ('M01','Es Kopi Susu','Minuman',22000,TRUE),('M07','Croissant','Makanan',22000,TRUE);
INSERT INTO bahan VALUES ('B01','Biji kopi','gram'),('B02','Susu','ml'),('B03','Es batu','gram'),('B04','Croissant beku','pcs');
INSERT INTO resep VALUES ('M01','B01',18),('M01','B02',120),('M01','B03',100),('M07','B04',1);
INSERT INTO stok_cabang VALUES
 ('C01','B01',2000,500),('C01','B02',10000,2000),('C01','B03',8000,1500),('C01','B04',30,10);

INSERT INTO pesanan (no_pesanan,waktu_pesan,id_cabang,id_staf,id_pelanggan,saluran,status) VALUES
 ('N-0012','2026-11-03 09:15:00','C01','S01','P01','KASIR','SELESAI'),
 ('N-0013','2026-11-03 10:05:00','C01','S01','P02','KASIR','SELESAI');
INSERT INTO detail_pesanan VALUES
 ('N-0012','M01',2,22000,NULL),('N-0012','M07',1,22000,NULL),
 ('N-0013','M01',1,22000,NULL);
INSERT INTO pembayaran VALUES
 ('B-0012','N-0012','QRIS',66000,'BERHASIL','2026-11-03 09:16:00','QRIS-SIM-0012'),
 ('B-0013','N-0013','TUNAI',22000,'BERHASIL','2026-11-03 10:06:00',NULL);
