from flask import Flask,render_template
import sqlite3


app = Flask(__name__)

@app.route("/")
@app.route("/home")
def homepage():
    connection = sqlite3.connect("DENEME.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT pc_id,pc_ad,fiyat,puan,site_ad,pc_imglink,pc_link FROM bilgisayar GROUP BY model_no""")
    rows = cursor.fetchall()

    cursor.execute("""SELECT DISTINCT marka FROM bilgisayar""")
    pc_names = cursor.fetchall()

    cursor.execute("""SELECT DISTINCT islemci_tipi FROM bilgisayar""")
    islemci_tipleri = cursor.fetchall()

    cursor.execute("""SELECT DISTINCT ram FROM bilgisayar""")
    ram_boyutlari = cursor.fetchall()


    return render_template("home.html", rows=rows, pc_names=pc_names,islemci_tipleri=islemci_tipleri,ram_boyutlari=ram_boyutlari)

@app.route("/view")
def kayitGoster():
    connection = sqlite3.connect("DENEME.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT pc_ad,fiyat,puan,site_ad,pc_link FROM bilgisayar""")
    rows = cursor.fetchall()

    return render_template("view.html",rows=rows)

@app.route("/fiyatArtan")
def fiyatArtan():
    connection = sqlite3.connect("DENEME.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT pc_id,pc_ad,fiyat,puan,site_ad,pc_imglink,pc_link FROM bilgisayar ORDER BY fiyat asc""")
    rows = cursor.fetchall()

    cursor.execute("""SELECT DISTINCT marka FROM bilgisayar""")
    pc_names = cursor.fetchall()


    return render_template("fiyat_artan.html",rows=rows,pc_names=pc_names)

@app.route("/fiyatAzalan")
def fiyatAzalan():
    connection = sqlite3.connect("DENEME.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT pc_id,pc_ad,fiyat,puan,site_ad,pc_imglink,pc_link FROM bilgisayar ORDER BY fiyat desc""")
    rows = cursor.fetchall()

    cursor.execute("""SELECT DISTINCT marka FROM bilgisayar""")
    pc_names = cursor.fetchall()


    return render_template("fiyat_azalan.html",rows=rows,pc_names=pc_names)

@app.route("/puanArtan")
def puanArtan():
    connection = sqlite3.connect("DENEME.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT pc_id,pc_ad,fiyat,puan,site_ad,pc_imglink,pc_link FROM bilgisayar ORDER BY puan asc""")
    rows = cursor.fetchall()

    cursor.execute("""SELECT DISTINCT marka FROM bilgisayar""")
    pc_names = cursor.fetchall()

    return render_template("puan_artan.html",rows=rows,pc_names=pc_names)

@app.route("/puanAzalan")
def puanAzalan():
    connection = sqlite3.connect("DENEME.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT pc_id,pc_ad,fiyat,puan,site_ad,pc_imglink,pc_link FROM bilgisayar ORDER BY puan desc""")
    rows = cursor.fetchall()

    cursor.execute("""SELECT DISTINCT marka FROM bilgisayar""")
    pc_names = cursor.fetchall()

    return render_template("puan_azalan.html",rows=rows,pc_names=pc_names)

@app.route("/pcDetails/id=<id>")
def bilgisayarSayfasi(id):
    connection = sqlite3.connect("DENEME.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""SELECT pc_id,pc_ad,fiyat,puan,pc_imglink,isletim_sistemi,islemci_tipi,islemci_nesli,ram,disk_boyut,disk_tur,ekran_boyut FROM bilgisayar WHERE pc_id={}""".format(id))
    rows = cursor.fetchall()


    return render_template("pc_ayrinti.html", rows=rows)

@app.route("/filterBrand/<markalarlistesi>")
def filtreSayfasi(markalarlistesi):

    connection = sqlite3.connect("DENEME.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    markalarlistesi = str(markalarlistesi).split(",")
    print(markalarlistesi)
    topluliste = []

    i=0
    while i<len(markalarlistesi):
        cursor.execute("""SELECT pc_id,pc_ad,fiyat,puan,site_ad,pc_imglink,pc_link FROM bilgisayar WHERE marka='{}'""".format(markalarlistesi[i]))
        rows = list(cursor.fetchall())


        i+=1

    cursor.execute("""SELECT DISTINCT marka FROM bilgisayar""")
    pc_names = cursor.fetchall()

    cursor.execute("""SELECT DISTINCT islemci_tipi FROM bilgisayar""")
    islemci_tipleri = cursor.fetchall()

    cursor.execute("""SELECT DISTINCT ram FROM bilgisayar""")
    ram_tipleri = cursor.fetchall()

    return render_template("filtre_marka.html", rows=rows, pc_names=pc_names, islemci_tipleri=islemci_tipleri,ram_tipleri=ram_tipleri)

@app.route("/filterIslemci/<islemcilistesi>")
def filtreSayfasi_islemci(islemcilistesi):

    connection = sqlite3.connect("DENEME.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    islemcilistesi = str(islemcilistesi).split(",")

    topluliste = []

    i=0
    while i<len(islemcilistesi):
        cursor.execute("""SELECT pc_id,pc_ad,fiyat,puan,site_ad,pc_imglink,pc_link FROM bilgisayar WHERE islemci_tipi='{}'""".format(islemcilistesi[i]))
        rows = list(cursor.fetchall())
        i+=1

    cursor.execute("""SELECT DISTINCT marka FROM bilgisayar""")
    pc_names = cursor.fetchall()

    cursor.execute("""SELECT DISTINCT islemci_tipi FROM bilgisayar""")
    islemci_tipleri = cursor.fetchall()

    cursor.execute("""SELECT DISTINCT ram FROM bilgisayar""")
    ram_tipleri = cursor.fetchall()

    return render_template("filtre_islemci.html", rows=rows, pc_names=pc_names, islemci_tipleri=islemci_tipleri, ram_tipleri=ram_tipleri)

@app.route("/filterram/<ramlistesi>")
def filtreSayfasi_ram(ramlistesi):

    connection = sqlite3.connect("DENEME.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    ramlistesi = str(ramlistesi).split(",")

    topluliste = []

    i=0
    while i<len(ramlistesi):
        cursor.execute("""SELECT pc_id,pc_ad,fiyat,puan,site_ad,pc_imglink,pc_link FROM bilgisayar WHERE ram='{}'""".format(ramlistesi[i]))
        rows = list(cursor.fetchall())
        i+=1


    cursor.execute("""SELECT DISTINCT marka FROM bilgisayar""")
    pc_names = cursor.fetchall()

    cursor.execute("""SELECT DISTINCT islemci_tipi FROM bilgisayar""")
    islemci_tipleri = cursor.fetchall()

    cursor.execute("""SELECT DISTINCT ram FROM bilgisayar""")
    ram_tipleri = cursor.fetchall()

    return render_template("filterram.html",rows=rows,pc_names=pc_names,islemci_tipleri=islemci_tipleri,ram_tipleri=ram_tipleri)






@app.route("/admin")
def adminSayfasi():
    connection = sqlite3.connect("DENEME.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT pc_id,marka,model_no,fiyat,puan,site_ad FROM bilgisayar""")
    rows = cursor.fetchall()

    return render_template("admin.html",rows=rows)

@app.route("/urunsil/<id_silme>")
def urunsilSayfasi(id_silme):
    connection = sqlite3.connect("DENEME.db")
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM bilgisayar WHERE pc_id={}""".format(id_silme))
    connection.commit()
    connection.close()


    connection = sqlite3.connect("DENEME.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT pc_id,marka,model_no,fiyat,puan,site_ad FROM bilgisayar""")
    rows = cursor.fetchall()


    return render_template("urunsil.html",rows=rows)

@app.route("/urunguncelle/<id_guncelleme>")
def guncellemeSayfasi(id_guncelleme):

    connection = sqlite3.connect("DENEME.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""SELECT marka,model_ad,model_no,isletim_sistemi,islemci_tipi,islemci_nesli,ram,disk_boyut,disk_tur,fiyat,puan FROM bilgisayar WHERE pc_id={}""".format(id_guncelleme))
    rows = cursor.fetchall()

    return render_template("urunguncelle.html",rows=rows)




if __name__ == '__main__':
    app.run(debug=True)

