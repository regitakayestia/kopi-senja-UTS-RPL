"""Membuat 05-erd.dot (notasi crow's foot) dari definisi tabel; sumber kebenaran = database/schema.sql."""
T = {
 "cabang":[("id_cabang","PK"),("nama_cabang",""),("alamat","")],
 "staf":[("id_staf","PK"),("id_cabang","FK"),("nama_staf",""),("email",""),("kata_sandi_hash",""),("peran","")],
 "pelanggan":[("id_pelanggan","PK"),("nama_pelanggan",""),("no_hp",""),("kata_sandi_hash","")],
 "menu":[("kode_menu","PK"),("nama_menu",""),("kategori",""),("harga",""),("aktif","")],
 "promo":[("id_promo","PK"),("nama_promo",""),("jenis_diskon",""),("nilai_diskon",""),("tgl_mulai",""),("tgl_selesai","")],
 "pesanan":[("no_pesanan","PK"),("waktu_pesan",""),("id_cabang","FK"),("id_staf","FK"),("id_pelanggan","FK"),("id_promo","FK"),("saluran",""),("status",""),("potongan","")],
 "detail_pesanan":[("no_pesanan","PK,FK"),("kode_menu","PK,FK"),("qty",""),("harga_satuan",""),("catatan","")],
 "pembayaran":[("id_pembayaran","PK"),("no_pesanan","FK"),("metode",""),("jumlah_bayar",""),("status",""),("waktu_bayar",""),("ref_qris","")],
 "bahan":[("id_bahan","PK"),("nama_bahan",""),("satuan","")],
 "stok_cabang":[("id_cabang","PK,FK"),("id_bahan","PK,FK"),("jumlah_stok",""),("stok_minimum","")],
 "resep":[("kode_menu","PK,FK"),("id_bahan","PK,FK"),("takaran","")],
}
# (induk, anak, kardinalitas sisi induk, sisi anak, label)  — "1"=tepat satu, "01"=nol/satu, "0N"=nol/banyak, "1N"=satu/banyak
R = [("cabang","staf","1","0N","mempekerjakan"),("cabang","pesanan","1","0N","menerima"),("cabang","stok_cabang","1","0N","menyimpan"),
     ("bahan","stok_cabang","1","0N","tercatat di"),("bahan","resep","1","0N","dipakai di"),("menu","resep","1","0N","memiliki"),
     ("menu","detail_pesanan","1","0N","dipesan di"),("pesanan","detail_pesanan","1","1N","terdiri dari"),("pesanan","pembayaran","1","01","dibayar lewat"),
     ("pelanggan","pesanan","01","0N","membuat"),("staf","pesanan","01","0N","melayani"),("promo","pesanan","01","0N","dipakai pada")]
HEAD={"1":"teetee","01":"teeodot","0N":"crowodot","1N":"crowtee"}
out=['digraph ERD {','graph [rankdir=LR, nodesep=0.35, ranksep=1.1, fontname="Inter", splines=true, pad=0.3, bgcolor=white];',
 'node [shape=plaintext, fontname="Inter", fontsize=11]; edge [fontname="Inter", fontsize=9.5, color="#44403c", arrowsize=0.9, labeldistance=1];']
for n,cols in T.items():
    rows="".join(f'<tr><td align="left" port="{c}"><font color="{"#9a3412" if "PK" in k else "#1c1917"}">{"<b>" if "PK" in k else ""}{c}{"</b>" if "PK" in k else ""}</font></td><td align="left">{('<font color="#78716c">'+k+'</font>') if k else "&nbsp;"}</td></tr>' for c,k in cols)
    out.append(f'{n} [label=<<table border="1" cellborder="0" cellspacing="0" cellpadding="3" color="#9a3412"><tr><td colspan="2" bgcolor="#9a3412"><font color="white"><b>{n}</b></font></td></tr>{rows}</table>>];')
for p,c,hp,hc,l in R:
    out.append(f'{p} -> {c} [dir=both, arrowtail="{HEAD[hp]}", arrowhead="{HEAD[hc]}", label=" {l}"];')
out.append("}")
open("05-erd.dot","w").write("\n".join(out))
