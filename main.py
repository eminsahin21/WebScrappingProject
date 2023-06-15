import requests
from bs4 import BeautifulSoup
import random
import string
import sqlite3 as sql


def tekrarlari_sil():
    connection = sql.connect("DENEME.db")
    cursor = connection.cursor()
    cursor.execute("""DELETE FROM bilgisayar WHERE model_no="" """)

    i=0
    while i<2:
        cursor.execute("""DELETE FROM bilgisayar where pc_id in ( 
                Select MAX(pc_id) as id
                From bilgisayar 
                Group By model_no 
                Having Count (model_no) > 1
                
                )""")
        i+=1

    connection.commit()
    connection.close()


def veritabani(kayitlistesi):
    _marka = str(kayitlistesi[0]).strip()
    _modelad = str(kayitlistesi[1]).strip()
    _modelno = str(kayitlistesi[2]).strip()
    _isletimsistemi = str(kayitlistesi[3]).strip()
    _islemcitipi = str(kayitlistesi[4]).strip()
    _islemcinesli = str(kayitlistesi[5]).strip()
    _ram = str(kayitlistesi[6]).strip()
    _diskboyut = str(kayitlistesi[7]).strip()
    _disktur = str(kayitlistesi[8]).strip()
    _ekranboyut = str(kayitlistesi[9]).strip()
    _puan = str(kayitlistesi[10]).strip()
    _fiyat = int(kayitlistesi[11])
    _sitead = str(kayitlistesi[12]).strip()
    _pctamad = str(kayitlistesi[13]).strip()
    _linkpc = str(kayitlistesi[14]).strip()
    _linkresim = str(kayitlistesi[15]).strip()

    connection = sql.connect("DENEME.db")
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS bilgisayar(
            pc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            marka TEXT,
            model_ad  TEXT,
            model_no  TEXT,
            isletim_sistemi  TEXT,
            islemci_tipi  TEXT,
            islemci_nesli  TEXT,
            ram  TEXT, 
            disk_boyut  TEXT,
            disk_tur  TEXT,
            ekran_boyut  TEXT,
            puan TEXT,
            fiyat  INTEGER,
            site_ad TEXT,
            pc_ad TEXT,
            pc_link TEXT,
            pc_imglink TEXT)""")

    ekle = """INSERT INTO bilgisayar 
    (marka,model_ad,model_no,isletim_sistemi,islemci_tipi,islemci_nesli,ram,disk_boyut,disk_tur,ekran_boyut,puan,fiyat,site_ad,pc_ad,pc_link,pc_imglink) 
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
    cursor.execute(ekle, (
        _marka, _modelad, _modelno, _isletimsistemi, _islemcitipi, _islemcinesli, _ram, _diskboyut, _disktur,
        _ekranboyut,
        _puan, _fiyat, _sitead, _pctamad, _linkpc, _linkresim))

    connection.commit()
    connection.close()

    return 1


def n11_tumislemler():
    # linke git fonksiyonu her pc nin ayrıntılı ekranına gidip özellik çeker
    # link pc her pc nin adresini(url) tutar
    def linke_git_n11(pc_link, fiyat, foto_url, link_pc):

        isletim_sistemi = ""
        islemci_tipi = ""
        islemci_nesli = ""
        ram_boyut = ""
        disk_turu = ""
        disk_boyut = ""
        ekran_boyut = ""
        model_no = ""

        site_ad = "n11"
        pc_model = pc_model_alma

        pc_url = pc_link
        r = requests.get(pc_url)
        soup2 = BeautifulSoup(r.text, "html.parser")
        rating = soup2.find("div", {"class": "ratingCont"}).strong.text
        rating = str(rating).replace(",", ".")
        urun_ozellik = soup2.find_all("li", {"class": "unf-prop-list-item"})

        for ozellik in urun_ozellik:
            ozellik_isim = ozellik.find("p", {"class": "unf-prop-list-title"}).text
            ozellik_cevap = ozellik.find("p", {"class": "unf-prop-list-prop"}).text
            ozellik_isim = str(ozellik_isim)
            ozellik_cevap = str(ozellik_cevap)

            if ozellik_isim == "İşletim Sistemi":
                isletim_sistemi = ozellik_cevap
            elif ozellik_isim == "İşlemci":
                islemci_tipi = ozellik_cevap
            elif ozellik_isim == "İşlemci Modeli":
                islemci_nesli = ozellik_cevap
            elif ozellik_isim == "Bellek Kapasitesi":
                ram_boyut = ozellik_cevap
            elif ozellik_isim == "Disk Türü":
                disk_turu = ozellik_cevap
            elif (ozellik_isim == "Disk Kapasitesi"):
                disk_boyut = ozellik_cevap
            elif ozellik_isim == "Ekran Boyutu":
                ekran_boyut = ozellik_cevap
                ekran_boyut = ekran_boyut.split("\"")[0]
            elif ozellik_isim == "Model":
                model_no = ozellik_cevap

            # print("{} = {}".format(ozellik_isim,ozellik_cevap))

            # print("Derece:{}".format(rating))

            toplu_liste_n11 = [pc_marka_alma.strip().capitalize(), pc_model, model_no, isletim_sistemi, islemci_tipi,
                               islemci_nesli, ram_boyut, disk_boyut, disk_turu, ekran_boyut]
            toplu_liste_n11.append(rating)
            toplu_liste_n11.append(sonfiyat_n11)
            toplu_liste_n11.append(site_ad)
            toplu_liste_n11.append(pc_tamad_n11)
            toplu_liste_n11.append(link_pc)
            toplu_liste_n11.append(foto_url)
            print(toplu_liste_n11)
            veritabani(toplu_liste_n11)

    # fonksiyon bitiyo burda karıştırma

    x = 1
    i = 0
    # while da yazdığım sayfa adedince pc bulur.2 ise 2 sayfanın verilerini çeker
    while x <= 5:
        url = "https://www.n11.com/bilgisayar/dizustu-bilgisayar?pg={}".format(x)
        print(url)
        response = requests.get(url)
        soup_n11 = BeautifulSoup(response.text, "html.parser")
        analink_n11 = soup_n11.find_all("li", {"class": "column"})

        x += 1
        for aramalinki_n11 in analink_n11:
            i += 1
            # pc tam adları
            pc_tamad_n11 = aramalinki_n11.find("h3", {"class": "productName"}).text
            pc_tamad_n11 = str(pc_tamad_n11)
            pc_model_alma = list(pc_tamad_n11.split())[1]
            pc_marka_alma = list(pc_tamad_n11.split())[0]
            # print(pc_tamad_n11)

            # fiyat bilgisi
            pc_fiyat_n11 = aramalinki_n11.find("div", {"class": "priceContainer"}).ins.text
            pc_fiyat_n11 = str(pc_fiyat_n11).split(",")[0]
            fiyat1 = pc_fiyat_n11.split(".")[0]
            fiyat2 = pc_fiyat_n11.split(".")[1]
            sonfiyat_n11 = fiyat1 + fiyat2
            # print("Fiyat:{}".format(pc_fiyat_n11))

            pc_foto_link = aramalinki_n11.find("img", {"class": "lazy cardImage"}).get("data-src")
            # print(pc_foto_link)

            # pc linkleri
            pc_link_n11 = aramalinki_n11.find("div", {"class": "pro"}).a.get("href")
            # print(linkler3)
            linke_git_n11(pc_link_n11, pc_fiyat_n11, pc_foto_link, pc_link_n11)

            print(
                "--------------------------------------------------------------------------------------------------------------")

    print("Toplam Kayıt(n11):{}".format(i))


def hepsiburada_tumislemler():
    def linke_git_hepsiburada(pc_link):
        isletim_sistemi = ""
        islemci_tipi = ""
        islemci_nesli = ""
        ram_boyut = ""
        disk_turu = ""
        disk_boyut = ""
        ekran_boyut = ""
        site_ad = "Hepsiburada"
        model_no = []

        pc_url = pc_link
        headers2 = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
        r = requests.get(pc_url, headers=headers2)
        soup2 = BeautifulSoup(r.text, "html.parser")
        rasgele = random.randint(1000, 9999)
        harf1 = random.choice(string.ascii_letters)
        harf2 = random.choice(string.ascii_letters)
        harf1 = str(harf1)
        harf2 = str(harf2)

        metin = str(rasgele) + harf1.upper() + harf2.upper()

        try:
            rating1 = soup2.find("span", {"class": "rating-star"}).text
        except AttributeError:
            rating1 = "0"

        rating1 = rating1.replace(",", ".")

        liste_model_no = soup2.find("h1", {"itemprop": "name"}).text
        liste_model_no = list(liste_model_no.split())

        if (liste_model_no[0] == "Monster") or (liste_model_no[0] == "MSI"):
            model_no = liste_model_no[3]
        elif (liste_model_no[0] == "Asus"):
            model_no = pc_url.split("-")
            model_no = model_no[len(model_no) - 1]
        elif (liste_model_no[0] == "Casper") or (liste_model_no[0] == "Huawei"):
            model_no = liste_model_no[2]
        else:
            model_no = liste_model_no[len(liste_model_no) - 1]
            if (model_no == "Bilgisayar") or (model_no == "Yıl") or (model_no == "Dos") or (model_no == "Notebook"):
                model_no = metin

        # print(model_no)
        rating1 = rating1.split("\r")[0]

        satimKontrol = soup2.find("div", {"class": "product-detail-box"}).get("style").strip()
        flag = 0
        if satimKontrol == "display: none":
            flag = 1  # pc nin dbase e kayıt edilip edilmiyeceği kontrolü için
            urun_ozellik1 = soup2.find("table", {"class": "data-list tech-spec"})
            urun_ozellik2 = urun_ozellik1.find_all("tr")
            for ozellik in urun_ozellik2:
                ozellik_isim = ozellik.th.text
                ozellik_cevap = ozellik.td.text
                ozellik_cevap = str(ozellik_cevap).strip()
                ozellik_isim = str(ozellik_isim).strip()

                if ozellik_isim == "İşletim Sistemi":
                    isletim_sistemi = ozellik_cevap
                elif ozellik_isim == "İşlemci Tipi":
                    islemci_tipi = ozellik_cevap
                elif ozellik_isim == "İşlemci Nesli":
                    islemci_nesli = ozellik_cevap
                elif ozellik_isim == "Ram (Sistem Belleği)":
                    ram_boyut = ozellik_cevap
                elif ozellik_isim == "Harddisk Kapasitesi":
                    disk_turu = "HDD"
                    disk_boyut = ozellik_cevap
                elif (ozellik_isim == "SSD Kapasitesi") and (ozellik_cevap != "Yok"):
                    disk_turu = "SSD"
                    disk_boyut = ozellik_cevap
                elif ozellik_isim == "Ekran Boyutu":
                    ekran_boyut = ozellik_cevap
                    ekran_boyut = ekran_boyut.split()[0].replace(",", ".")

                # print("{}==={}".format(ozellik_isim,ozellik_cevap))
        else:
            flag = 0
            print("Bu bilgisayar şuan satışta değil")

        if flag == 1:
            kayit_listesi = [str(hepsbrda_urun_model[0]).capitalize(), hepsbrda_urun_model[1], model_no,
                             isletim_sistemi, islemci_tipi, islemci_nesli, ram_boyut, disk_boyut, disk_turu,
                             ekran_boyut]
            kayit_listesi.append(rating1)
            kayit_listesi.append(sonfiyat_hepsiburada)
            kayit_listesi.append(site_ad)
            kayit_listesi.append(hepsbrda_urun_tamad)
            kayit_listesi.append(hepsbrda_pc_link)
            kayit_listesi.append(hepsbrda_urun_foto)
            print(kayit_listesi)
            veritabani(kayit_listesi)

        return 1

    # fonksiyon bitiyo burda karıştırma

    x = 1
    i = 0
    # while da yazdığım(x) sayfa adedince pc bulur.2 ise 2 sayfanın verilerini çeker
    while x <= 15:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
        url = "https://www.hepsiburada.com/ara?q=laptop&kategori=2147483646_3000500_98&sayfa={}".format(x)
        print("SAYFA BAŞI URLSİ:{}".format(url))
        print("-" * 180)
        response = requests.get(url, headers=headers)
        soup_hepsiburada = BeautifulSoup(response.text, "html.parser")
        analink_hepsiburada = soup_hepsiburada.find_all("li", {"class": "productListContent-zAP0Y5msy8OHn5z7T_K_"})

        x += 1
        for link_hpsbrda in analink_hepsiburada:
            i += 1

            # urun marka model tam ad
            hepsbrda_urun_model = link_hpsbrda.find("h3", {"data-test-id": "product-card-name"}).text
            hepsbrda_urun_tamad = hepsbrda_urun_model
            hepsbrda_urun_model = list(hepsbrda_urun_model.split())
            # print(hepsbrda_urun_model[0])

            # fiyat bilgisi okay
            hepsbrda_urun_fiyat = link_hpsbrda.find("div", {"data-test-id": "price-current-price"}).text
            hepsbrda_urun_fiyat = str(hepsbrda_urun_fiyat).split(",")[0]
            fiyat1 = hepsbrda_urun_fiyat.split(".")[0]
            fiyat2 = hepsbrda_urun_fiyat.split(".")[1]
            sonfiyat_hepsiburada = fiyat1 + fiyat2
            # print(hepsbrda_urun_fiyat)

            # foto
            hepsbrda_urun_foto = link_hpsbrda.find("div", {"data-test-id": "product-image-image"}).img.get("src")
            # print(hepsbrda_urun_foto)

            # pc linkleri okay
            hepsbrda_pc_link = link_hpsbrda.a.get("href")
            if hepsbrda_pc_link.startswith("https"):
                hepsbrda_pc_link = hepsbrda_pc_link
            else:
                hepsbrda_pc_link = str(hepsbrda_pc_link)
                hepsbrda_pc_link = "https://www.hepsiburada.com" + hepsbrda_pc_link

            # print(hepsbrda_pc_link)
            linke_git_hepsiburada(hepsbrda_pc_link)

            print(
                "--------------------------------------------------------------------------------------------------------------")

    print("Toplam Kayıt:{}".format(i))

    return 0


def trendyol_tumislemler():
    # trendyoldan veri çeker

    # linke git fonksiyonu her pc nin ayrıntılı ekranına gidip özellik çeker
    def linke_git(pc_link):

        pc_marka = ""
        isletim_sistemi = ""
        islemci_tipi = ""
        islemci_nesli = ""
        ram_boyut = ""
        disk_turu = ""
        disk_boyut = ""
        ekran_boyut = ""

        pc_url = pc_link
        r = requests.get(pc_url)
        soup2 = BeautifulSoup(r.text, "html.parser")
        sitead = "Trendyol"

        urun_full_ad = str(urun_marka_trendyol) + " " + str(urun_model_trendyol)
        # print(urun_full_ad)

        # pclerin foto linkleri
        foto = soup2.find_all("img")
        img_pc = []
        for urunfoto in foto:
            img_pc.append(urunfoto.get("src"))

        foto_link = img_pc[1]

        # urun model nosunu çekmek için
        urun_model_arama = soup2.find("h1", {"class": "pr-new-br"}).span.text
        urun_tamad_liste = list(str(urun_model_arama).split())

        # print(urun_tamad_liste)
        if (urun_marka_trendyol == "Monster"):
            model_no = urun_tamad_liste[2]
        elif (urun_marka_trendyol == "Casper"):
            model_no = urun_tamad_liste[1]
        elif (urun_marka_trendyol == "MSI"):
            model_no = urun_tamad_liste[3]
        else:
            model_no = urun_tamad_liste[len(urun_tamad_liste) - 1]
            if (model_no == "Yıl") or (model_no == "Bilgisayar"):
                model_no = "-"

        # urun model adı
        urun_model_ad = urun_tamad_liste[0]

        # pc ozellikleri
        urun_ozellik = soup2.find_all("li", {"class": "detail-attr-item"})
        for ozellik in urun_ozellik:
            ozellik_isim = ozellik.find("span").text
            ozellik_cevap = ozellik.find("b").text
            # print("{}-{}".format(ozellik_isim,ozellik_cevap))

            if ozellik_isim == "İşletim Sistemi":
                isletim_sistemi = ozellik_cevap
            elif ozellik_isim == "İşlemci Tipi":
                islemci_tipi = ozellik_cevap
            elif (ozellik_isim == "İşlemci Nesli") or (ozellik_isim == "İslemci Nesli"):
                islemci_nesli = ozellik_cevap
            elif ozellik_isim == "Ram (Sistem Belleği)":
                ram_boyut = ozellik_cevap
            elif (ozellik_isim == "Harddisk Kapasitesi") and (ozellik_cevap != "Yok"):
                disk_turu = "HDD"
                disk_boyut = ozellik_cevap
            elif (ozellik_isim == "SSD Kapasitesi") and (ozellik_cevap != "Yok"):
                disk_turu = "SSD"
                disk_boyut = ozellik_cevap
            elif (ozellik_isim == "Kapasite"):
                disk_turu = "SSD"
                disk_boyut = ozellik_cevap
            elif ozellik_isim == "Ekran Boyutu":
                ekran_boyut = ozellik_cevap
                ekran_boyut = str(ekran_boyut).split()[0].replace(",", ".")

        trendyol_db_liste = [urun_marka_trendyol.capitalize(), urun_model_ad, model_no, isletim_sistemi, islemci_tipi,
                             islemci_nesli, ram_boyut, disk_boyut, disk_turu, ekran_boyut]
        trendyol_db_liste.append(yildiz_puani)
        trendyol_db_liste.append(sonfiyat)
        trendyol_db_liste.append(sitead)
        trendyol_db_liste.append(urun_full_ad)
        trendyol_db_liste.append(trend_pc_link)
        trendyol_db_liste.append(foto_link)
        print(trendyol_db_liste)
        veritabani(trendyol_db_liste)

        return 1

    # fonksiyon bitiyo burda karıştırma

    x = 1
    i = 0
    # while da yazdığım(x) sayfa adedince pc bulur.2 ise 2 sayfanın verilerini çeker
    while x <= 5:
        url = "https://www.trendyol.com/laptop-x-c103108?pi={}".format(x)
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        analink_trendyol = soup.find_all("div", {"class": "p-card-wrppr with-campaign-view"})

        x += 1
        for link_trendyol in analink_trendyol:
            i += 1

            # urun markaları
            urun_marka_trendyol = link_trendyol.find("span", {"class": "prdct-desc-cntnr-ttl"}).text
            urun_marka_trendyol = str(urun_marka_trendyol).capitalize()

            # urun model tam ad
            urun_model_trendyol = link_trendyol.find("span", {"class": "prdct-desc-cntnr-name"}).text

            # fiyat bilgisi
            urun_fiyat_trendyol = link_trendyol.find("div", {"class": "prc-box-dscntd"}).text
            urun_fiyat_trendyol = str(urun_fiyat_trendyol).split()[0].split(",")[0]
            fiyat1 = urun_fiyat_trendyol.split(".")[0]
            fiyat2 = urun_fiyat_trendyol.split(".")[1]
            sonfiyat = fiyat1 + fiyat2

            # ratingler
            yildiz_puani = 0
            try:
                rating1 = link_trendyol.find("div", {"class": "ratings"})
                rating2 = rating1.find_all("div", {"class": "star-w"})
                for rtng in rating2:
                    rating3 = rtng.find_all("div", {"class": "full"})
                    # rating3 = str(rating3)
                    for n in rating3:
                        rating4 = n.get("style")
                        rating4 = str(rating4).split(";")[0].split(":")[1].split("%")[0]
                        puan_tutucu = int(rating4)
                        yildiz_puani += (puan_tutucu / 100)
                # print(yildiz_puani)
            except AttributeError:
                yildiz_puani = 0

            # pc linkleri
            trend_pc_link = link_trendyol.find("div", {"class": "p-card-chldrn-cntnr card-border"}).a.get("href")
            trend_pc_link = "https://www.trendyol.com" + trend_pc_link
            # print(trend_pc_link)
            linke_git(trend_pc_link)
            yildiz_puani = 0
            print(
                "--------------------------------------------------------------------------------------------------------------")

    print("Toplam Kayıt:{}".format(i))

    return 0


def vatan_tumislemler():
    def linke_git(pc_link):

        pc_url = pc_link
        r = requests.get(pc_url)
        soup2 = BeautifulSoup(r.text, "html.parser")

        sitead = "Vatan"
        pc_marka = ""
        isletim_sistemi = ""
        islemci_tipi = ""
        islemci_nesli = ""
        ram_boyut = ""
        disk_turu = ""
        disk_boyut = ""
        ekran_boyut = ""

        rating1 = soup2.find("span", {"class": "score"}).get("style").split(":")
        rating2 = rating1[1].split("%")
        rating3 = int(rating2[0])
        sonrating = rating3 / 20

        urun_ozellik = soup2.find_all("table", {"class": "product-table"})
        for ozellik in urun_ozellik:
            ozellik1 = ozellik.find_all("tr", {"data-count": "0"})

            for son_ozellik in ozellik1:
                ozellik_isim = son_ozellik.td.text
                ozellik_cevap = son_ozellik.find("p").text
                # print("{}-{}".format(ozellik_isim,ozellik_cevap))

                if ozellik_isim == "İşletim Sistemi":
                    isletim_sistemi = ozellik_cevap
                elif ozellik_isim == "İşlemci Teknolojisi":
                    islemci_tipi = ozellik_cevap
                elif ozellik_isim == "İşlemci Nesli":
                    islemci_nesli = ozellik_cevap
                elif ozellik_isim == "Ram (Sistem Belleği)":
                    ram_boyut = ozellik_cevap
                elif ozellik_isim == "Disk Türü":
                    disk_turu = ozellik_cevap
                elif (ozellik_isim == "Disk Kapasitesi"):
                    disk_boyut = ozellik_cevap
                elif ozellik_isim == "Ekran Boyutu":
                    ekran_boyut = ozellik_cevap
                    ekran_boyut = ekran_boyut.split()[0]

        toplu_liste_vatan = [vatan_urunmarka.capitalize(), vatan_urunmodel, vatan_urun_modelno, isletim_sistemi,
                             islemci_tipi, islemci_nesli, ram_boyut, disk_boyut, disk_turu, ekran_boyut]
        toplu_liste_vatan.append(sonrating)
        toplu_liste_vatan.append(sonfiyat_vatan)
        toplu_liste_vatan.append(sitead)
        toplu_liste_vatan.append(vatan_urun_model_tamad)
        toplu_liste_vatan.append(vatan_pc_link)
        toplu_liste_vatan.append(urun_foto)
        print(toplu_liste_vatan)
        veritabani(toplu_liste_vatan)

        return 1

    # fonksiyon bitiyo burda karıştırma

    x = 1
    i = 0
    # while da yazdığım(x) sayfa adedince pc bulur.2 ise 2 sayfanın verilerini çeker
    while x <= 15:
        url = "https://www.vatanbilgisayar.com/notebook/?page={}".format(x)
        print(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        linkler1 = soup.find_all("div", {"class": "product-list product-list--list-page"})

        x += 1
        for link in linkler1:
            i += 1

            # urun marka model tam ad
            vatan_urun_model_tamad = link.find("div", {"class": "product-list__product-name"}).h3.text
            # print(vatan_urun_model_tamad)
            vatan_urunmarka = str(vatan_urun_model_tamad).split()[0].capitalize()
            vatan_urunmodel = str(vatan_urun_model_tamad).split()[1]
            # print(vatan_urunmarka)
            # print(vatan_urunmodel)

            # urun modelno
            vatan_urun_modelno = link.find("div", {"class": "product-list__product-code"}).text
            vatan_urun_modelno = str(vatan_urun_modelno).strip()
            # print(vatan_urun_modelno)

            # fiyat bilgisi okay
            vatan_urun_fiyat = link.find("span", {"class": "product-list__price"}).text
            fiyat1 = vatan_urun_fiyat.split(".")[0]
            fiyat2 = vatan_urun_fiyat.split(".")[1]
            sonfiyat_vatan = fiyat1 + fiyat2
            # print(vatan_urun_fiyat)

            # foto
            urun_foto = link.find("img", {"class": "owl-lazy"}).get("data-src")
            # print(urun_foto)

            # pc linkleri okay
            vatan_pc_link = link.find("div", {"class": "product-list__image-safe"}).a.get("href")
            vatan_pc_link = str(vatan_pc_link)
            vatan_pc_link = "https://www.vatanbilgisayar.com" + vatan_pc_link
            linke_git(vatan_pc_link)
            # print(vatan_pc_link)

            print(
                "--------------------------------------------------------------------------------------------------------------")

    print("Toplam Kayıt:{}".format(i))


if __name__ == "__main__":
    hepsiburada_tumislemler()
    trendyol_tumislemler()
    vatan_tumislemler()
    n11_tumislemler()
    tekrarlari_sil()
