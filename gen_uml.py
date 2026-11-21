"""Pembangkit SVG untuk Use Case Diagram (03a) dan Activity Diagram (03c) Kopi Senja."""
import math, html
F = "font-family:Inter,DejaVu Sans,sans-serif"
def esc(t): return html.escape(t)

class Svg:
    def __init__(s, w, h):
        s.w, s.h, s.o = w, h, []
    def add(s, x): s.o.append(x)
    def text(s, x, y, t, size=13, anchor="middle", weight="normal", fill="#1c1917", style=""):
        lines = t.split("\n"); y0 = y - (len(lines)-1)*size*0.6 + size*0.35
        for i, l in enumerate(lines):
            s.add(f'<text x="{x}" y="{y0+i*size*1.2:.1f}" text-anchor="{anchor}" style="{F};font-size:{size}px;font-weight:{weight};{style}" fill="{fill}">{esc(l)}</text>')
    def tlabel(s, x, y, t, size=11):  # label dengan latar putih
        w = max(len(l) for l in t.split("\n"))*size*0.58+8; h = (t.count("\n")+1)*size*1.25+4
        s.add(f'<rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" fill="white" opacity="0.92"/>')
        s.text(x, y, t, size, style="font-style:italic")
    def save(s, path):
        defs = '''<defs>
<marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#292524"/></marker>
<marker id="op" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M1,1 L9,5 L1,9" fill="none" stroke="#292524" stroke-width="1.4"/></marker>
</defs>'''
        open(path, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s.w} {s.h}" width="{s.w}" height="{s.h}"><rect width="100%" height="100%" fill="white"/>{defs}{"".join(s.o)}</svg>')

# ---------------------------------------------------------------- USE CASE
def usecase():
    W, H = 1240, 1000
    g = Svg(W, H)
    BX, BY, BW, BH = 190, 40, 860, 930
    g.add(f'<rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" fill="#fffdf8" stroke="#44403c" stroke-width="2"/>')
    g.text(BX+BW/2, BY+22, "Sistem Informasi Pemesanan dan Persediaan “Kopi Senja”", 15, weight="bold")
    g.text(BX+BW/2, BY+42, "(batas sistem)", 11, fill="#78716c")
    UC = {  # kunci: (x, y, teks)
     "menu":   (330, 150, "Melihat Menu"),
     "pesan":  (330, 290, "Memesan Menu"),
     "status": (330, 560, "Melihat Status\nPesanan"),
     "antre":  (330, 640, "Melihat Antrean\nPesanan"),
     "ubah":   (330, 770, "Memperbarui\nStatus Pesanan"),
     "promo":  (610, 190, "Menerapkan Promo"),
     "total":  (610, 320, "Menghitung Total\nPesanan"),
     "bayar":  (610, 470, "Melakukan\nPembayaran"),
     "qris":   (860, 360, "Membayar\ndengan QRIS"),
     "kurangi":(610, 610, "Mengurangi Stok\nOtomatis"),
     "notif":  (610, 770, "Mengirim Notifikasi\nPesanan Siap"),
     "kmenu":  (860, 480, "Mengelola Menu,\nResep, dan Promo"),
     "pantau": (860, 580, "Memantau\nStok Bahan"),
     "alert":  (860, 680, "Menerima Peringatan\nStok Minimum"),
     "catat":  (860, 780, "Mencatat Penerimaan/\nPenyesuaian Stok"),
     "lapor":  (860, 880, "Melihat Laporan\nPenjualan"),
    }
    RX, RY = 88, 27
    def ell(k):
        x,y,t = UC[k]
        g.add(f'<ellipse cx="{x}" cy="{y}" rx="{RX}" ry="{RY}" fill="#fff7ed" stroke="#9a3412" stroke-width="1.6"/>')
        g.text(x, y, t, 12.5)
    def edge_pt(a, b):  # titik pada tepi elips a menuju b
        ax,ay,_=UC[a]; bx,by,_=UC[b]; dx,dy=bx-ax,by-ay; d=math.hypot(dx,dy) or 1
        k=1/math.sqrt((dx/d/RX)**2+(dy/d/RY)**2); return ax+dx/d*k, ay+dy/d*k
    # aktor
    ACT = {"Pelanggan":(80,430,"L"), "Kasir":(80,290,"L"), "Barista":(80,730,"L"),
           "Layanan QRIS\n(sistem eksternal)":(1140,260,"R"), "Manajer Cabang":(1140,640,"R"), "Pemilik":(1140,900,"R")}
    def actor(x,y,label,ext=False):
        c="#44403c"
        g.add(f'<g stroke="{c}" stroke-width="2" fill="none"><circle cx="{x}" cy="{y-30}" r="10" fill="white"/><line x1="{x}" y1="{y-20}" x2="{x}" y2="{y+14}"/><line x1="{x-18}" y1="{y-8}" x2="{x+18}" y2="{y-8}"/><line x1="{x}" y1="{y+14}" x2="{x-15}" y2="{y+38}"/><line x1="{x}" y1="{y+14}" x2="{x+15}" y2="{y+38}"/></g>')
        if ext: g.text(x, y-52, "«actor»", 10, fill="#78716c")
        g.text(x, y+56, label, 12.5, weight="bold")
    for n,(x,y,_) in ACT.items(): actor(x,y,n,ext=n.startswith("Layanan"))
    # asosiasi
    def assoc(actor_name, uc):
        ax,ay,side = ACT[actor_name]; ux,uy,_ = UC[uc]
        p0=(ax+(20 if side=="L" else -20), ay)
        # titik tepi elips menuju aktor
        dx,dy=p0[0]-ux,p0[1]-uy; d=math.hypot(dx,dy); k=1/math.sqrt((dx/d/RX)**2+(dy/d/RY)**2)
        p1=(ux+dx/d*k, uy+dy/d*k)
        g.add(f'<line x1="{p0[0]}" y1="{p0[1]}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" stroke="#44403c" stroke-width="1.4"/>')
    # elips digambar setelah garis agar menimpa ujung
    for a,u in [("Pelanggan","menu"),("Pelanggan","pesan"),("Pelanggan","status"),("Pelanggan","bayar"),
                ("Kasir","menu"),("Kasir","pesan"),("Kasir","bayar"),
                ("Barista","antre"),("Barista","ubah"),
                ("Layanan QRIS\n(sistem eksternal)","qris"),
                ("Manajer Cabang","kmenu"),("Manajer Cabang","pantau"),("Manajer Cabang","alert"),("Manajer Cabang","catat"),("Manajer Cabang","lapor"),
                ("Pemilik","lapor")]:
        assoc(a,u)
    # include / extend
    def rel(a, b, label, lx=0, ly=0):
        p0=edge_pt(a,b); p1=edge_pt(b,a)
        g.add(f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" stroke="#292524" stroke-width="1.3" stroke-dasharray="6 4" marker-end="url(#op)"/>')
        g.tlabel((p0[0]+p1[0])/2+lx, (p0[1]+p1[1])/2+ly, label)
    rel("pesan","total","«include»", 10, 0)
    rel("promo","pesan","«extend»", 0, -4)
    rel("bayar","kurangi","«include»", 28, 0)
    rel("qris","bayar","«extend»", 14, -2)
    rel("notif","ubah","«extend»", 0, -12)
    rel("alert","pantau","«extend»", 30, 0)
    rel("kurangi","alert","«extend»", 0, 0) if False else None
    for k in UC: ell(k)
    # catatan syarat extend
    g.text(840, 650, "[stok ≤ stok minimum]", 10.5, anchor="end", fill="#78716c", style="font-style:italic")
    g.text(470, 796, "[status = Siap]", 10.5, fill="#78716c", style="font-style:italic")
    g.text(860, 402, "[metode = QRIS]", 10.5, fill="#78716c", style="font-style:italic")
    g.text(520, 268, "[ada promo berlaku]", 10.5, fill="#78716c", style="font-style:italic")
    g.save("../03a-usecase.svg")

# ---------------------------------------------------------------- ACTIVITY (versi sederhana)
def activity():
    LX = {"Pelanggan":145, "Kasir":425, "Barista":705}
    LW, TOP = 280, 44
    W, H = 850, 990
    g = Svg(W, H)
    for i,(n,x) in enumerate(LX.items()):
        g.add(f'<rect x="{x-LW/2}" y="{TOP}" width="{LW}" height="{H-TOP-10}" fill="{"#fffaf2" if i%2==0 else "#faf8f5"}" stroke="#78716c" stroke-width="1.2"/>')
        g.add(f'<rect x="{x-LW/2}" y="{TOP-34}" width="{LW}" height="34" fill="#9a3412"/>')
        g.text(x, TOP-17, n, 15, weight="bold", fill="white")
    P,K,B = LX["Pelanggan"], LX["Kasir"], LX["Barista"]
    def act(x, y, t, w=200, h=50):
        g.add(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="14" fill="#fff7ed" stroke="#9a3412" stroke-width="1.5"/>'); g.text(x,y,t,13)
    def dec(x, y, t, w=130, h=70):
        g.add(f'<polygon points="{x},{y-h/2} {x+w/2},{y} {x},{y+h/2} {x-w/2},{y}" fill="#fef3c7" stroke="#92400e" stroke-width="1.5"/>'); g.text(x,y,t,12)
    def bar(x1,x2,y): g.add(f'<rect x="{x1}" y="{y-4}" width="{x2-x1}" height="8" fill="#1c1917"/>')
    def line(pts, label=None, lp=None):
        d="M"+" L".join(f"{x},{y}" for x,y in pts)
        g.add(f'<path d="{d}" fill="none" stroke="#292524" stroke-width="1.6" marker-end="url(#ar)"/>')
        if label: g.tlabel(*lp, label, 12)
    g.add(f'<circle cx="{P}" cy="{TOP+28}" r="11" fill="#1c1917"/>')
    act(P,150,"Memesan menu\ndan jumlah")
    act(K,240,"Mencatat pesanan")
    dec(K,340,"menu\ntersedia?")
    act(P,340,"Memilih menu lain")
    act(K,450,"Menerima pembayaran\n(tunai / QRIS)")
    act(K,620,"Memberikan struk")
    act(B,620,"Membuat pesanan")
    act(B,780,"Menandai pesanan\nsiap")
    act(P,870,"Mengambil pesanan")
    bar(K-40,B+40,530); bar(K-40,B+40,700)
    g.text(K-50,530,"fork",11,anchor="end",fill="#78716c",style="font-style:italic")
    g.text(K-50,700,"join",11,anchor="end",fill="#78716c",style="font-style:italic")
    line([(P,TOP+39),(P,125)])
    line([(P+100,150),(K,150),(K,215)])
    line([(K,265),(K,305)])
    line([(K-65,340),(P+100,340)],"[tidak]",(K-105,326))
    line([(P,315),(P,240),(K-100,240)])
    line([(K,375),(K,425)],"[ya]",(K+26,400))
    line([(K,475),(K,526)])
    line([(K,534),(K,595)]); line([(B,534),(B,595)])
    line([(K,645),(K,696)]); line([(B,645),(B,696)])
    line([(B+20,704),(B+20,755)])
    line([(B-100,780),(P,780),(P,845)])
    g.add(f'<circle cx="{P}" cy="945" r="13" fill="white" stroke="#1c1917" stroke-width="2"/><circle cx="{P}" cy="945" r="8" fill="#1c1917"/>')
    line([(P,895),(P,932)])
    g.save("../03c-activity.svg")

usecase(); activity()
