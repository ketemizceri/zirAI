from flask import Flask, request, render_template
import numpy as np
import pickle
import pandas as pd

# Modeli yükleme
model = pickle.load(open('model.pkl', 'rb'))
sc = pickle.load(open('standscaler.pkl', 'rb'))
ms = pickle.load(open('minmaxscaler.pkl', 'rb'))

# Veri setini okuma
data = pd.read_csv('OneriVerisetiENG.csv')  # Örnek: dataset.csv dosyasından N, P, K, pH bilgilerini okuyacağız.

# Flask uygulaması başlatma
app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hasat.html')
def hasat():
    return render_template('hasat.html')

@app.route('/oneri.html', methods=['GET', 'POST'])
def index():
    return render_template("oneri.html")


@app.route("/predict", methods=['POST'])
def predict():
    try:
        # Kullanıcıdan alınan değerler
        bolge_text = request.form['Bolge'].strip().lower()  # Kullanıcıdan alınan bölge küçük harfe çevrildi
        sehir_text = request.form['Sehir'].strip().lower()  # Kullanıcıdan alınan şehir küçük harfe çevrildi

        # Bölge ve şehir isimlerini normalize etmek için bir sözlük oluşturun
        bolge_dict = {
            "karadeniz": "Karadeniz Bolgesi",
            "karadeniz bolgesi": "Karadeniz Bolgesi",
            "karadeniz bölgesi": "Karadeniz Bolgesi",
            "marmara": "Marmara Bolgesi",
            "marmara bolgesi": "Marmara Bolgesi",
            "marmara bölgesi": "Marmara Bolgesi",
            "ege": "Ege Bolgesi",
            "ege bolgesi": "Ege Bolgesi",
            "ege bölgesi": "Ege Bolgesi",
            "akdeniz": "Akdeniz Bolgesi",
            "akdeniz bolgesi": "Akdeniz Bolgesi",
            "akdeniz bölgesi": "Akdeniz Bolgesi",
            "dogu anadolu": "Dogu Anadolu Bolgesi",
            "doguanadolu bolgesi": "Dogu Anadolu Bolgesi",
            "doğu anadolu": "Dogu Anadolu Bolgesi",
            "doğu anadolu bölgesi": "Dogu Anadolu Bolgesi",
            "guneydogu anadolu bolgesi":"Guneydogu Anadolu Bolgesi",
            "guneydogu": "Guneydogu Anadolu Bolgesi",
            "guneydoğu bolgesi": "Guneydogu Anadolu Bolgesi",
            "guneydogu bolgesi": "Guneydogu Anadolu Bolgesi",
            "güneydoğu": "Guneydogu Anadolu Bolgesi",
            "güneydoğu bölgesi": "Guneydogu Anadolu Bolgesi",
            "iç anadolu" : "Ic Anadolu Bolgesi",
            "iç anadolu bölgesi": "Ic Anadolu Bolgesi",
            "ic anadolu bölgesi": "Ic Anadolu Bolgesi",
            "ıc anadolu bolgesi": "Ic Anadolu Bolgesi",
            "ıc anadolu": "Ic Anadolu Bolgesi",
            "İç anadolu": "Ic Anadolu Bolgesi"
        }

        # Kullanıcı girişini normalize edin (bölge ve şehir eşleştiriliyor)
        if bolge_text in bolge_dict:
            bolge_normalized = bolge_dict[bolge_text]
        else:
            return "Girilen bölge veri setinde bulunamadı!"  # Hata kontrolü
        # Kullanıcıdan alınan diğer değerler
        Sicaklik = int(request.form['Sicaklik'])
        Nem = int(request.form['Nem'])
        YagmurOrani = int(request.form['YagmurOrani'])

        # Veri setinden bölge ve şehir ID değerleri alınıyor
        bolge_row = data[data['Bolge'] == bolge_normalized]  # Normalized bölgeyi seçiyoruz
        if bolge_row.empty:
            return "Girilen bölge veri setinde bulunamadı!"  # Hata kontrolü

        BolgeId = bolge_row['BolgeId'].values[0]  # Bölgenin ID'si

        # Şehir adı aynı şekilde normalize edilebilir
        sehir_row = data[
            (data['Sehir'].str.lower().str.strip() == sehir_text) & (data['BolgeId'] == BolgeId)
            ]  # Küçük harfe göre karşılaştırma
        if sehir_row.empty:
            return "Girilen şehir, bu bölgede bulunamadı!"  # Hata kontrolü

        Id = sehir_row['Id'].values[0]  # Şehrin ID'si

        # N, P, K, pH değerlerini alma
        N = sehir_row['N'].values[0]
        P = sehir_row['P'].values[0]
        K = sehir_row['K'].values[0]
        pH = sehir_row['pH'].values[0]

        # MinMaxScaler ve model için tam özellik listesi oluşturuluyor (9 değer)
        feature_list = [Id, BolgeId, N, P, K, pH, Sicaklik, Nem, YagmurOrani]

        # Model giriş verisini uygun şekilde düzenleme
        single_pred = np.array(feature_list).reshape(1, -1)

        # Özellikleri ölçeklendirme
        scaled_features = ms.transform(single_pred)  # Min-Max ölçeklendirme
        final_features = sc.transform(scaled_features)  # Standard Scaler işleme

        # Tahmini alma
        prediction = model.predict(final_features)

        # Ürün isimlerini eşleştiren sözlük
        dt_urun_dict = {
            1: "Armut",
            2: "Arpa",
            3: "Aycicegi",
            4: "Balkabagi",
            5: "Bamya",
            6: "Bezelye",
            7: "Biber",
            8: "Borulce",
            9: "Bugday",
            10: "Cavdar",
            11: "Cay",
            12: "Ceviz",
            13: "Cilek",
            14: "Domates",
            15: "Elma",
            16: "Erik",
            17: "Fasulye",
            18: "Findik",
            19: "Fistik",
            20: "Gul",
            21: "Hashas",
            22: "Incir",
            23: "Karpuz",
            24: "Kavun",
            25: "Kayisi",
            26: "Kestane",
            27: "Kiraz",
            28: "Kivi",
            29: "Lahana",
            30: "Limon",
            31: "Marul",
            32: "Mercimek",
            33: "Misir",
            34: "Muz",
            35: "Nar",
            36: "Narenciye",
            37: "Nohut",
            38: "Pamuk",
            39: "Pancar",
            40: "Patates",
            41: "Patlican",
            42: "Pazi",
            43: "Pirinc",
            44: "Salatalik",
            45: "Sarimsak",
            46: "Seftali",
            47: "Sogan",
            48: "Tutun",
            49: "Uzum",
            50: "Yonca",
            51: "Yulaf",
            52: "Zeytin",
            53: "Antepfistigi"
        }

        dt_urun_images = {
            1: "images/armut.jpeg",  # Armut
            2: "images/arpa.jpeg",  # Arpa
            3: "images/aycicegi.jpg",  # Aycicegi
            4: "images/balkabagi.jpg",  # Balkabagi
            5: "images/bamya.jpeg",  # Bamya
            6: "images/bezelye.jpg",  # Bezelye
            7: "images/biber.jpg",  # Biber
            8: "images/borulce.jpg",  # Borulce
            9: "images/bugday.jpeg",  # Bugday
            10: "images/cavdar.jpg",  # Cavdar
            11: "images/cay.jpg",  # Cay
            12: "images/ceviz.jpg",  # Ceviz
            13: "images/cilek",  # Cilek
            14: "images/domates.jpg",  # Domates
            15: "images/elma.jpg",  # Elma
            16: "images/erik.jpg",  # Erik
            17: "images/fasulye.jpg",  # Fasulye
            18: "images/findik.jpg",  # Findik
            19: "images/fistik.jpg",  # Fistik
            20: "images/gul.jpg",  # Gul
            21: "images/hashas.jpg", # Hashas
            22: "images/incir.jpg",  # Incir
            23: "images/karpuz.jpg",  # Karpuz
            24: "images/kavun.jpeg",  # Kavun
            25: "kayisi.jpg",  # Kayisi
            26: "images/kestane.jpg",  # Kestane
            27: "images/kiraz.pg",  # Kiraz
            28: "images/kivi.jpg",  # Kivi
            29: "images/lahana.jpg",  # Lahana
            30: "images/limon.jpg",  # Limon
            31: "images/marul.jpg",  # Marul
            32: "images/mercimek.jpg",  # Mercimek
            33: "images/misir.jpg",  # Misir
            34: "images/muz.jpg",  # Muz
            35: "images/nar.jpg",  # Nar
            36: "images/narenciye.jpg",  # Narenciye
            37: "images/nohut.jpg",  # Nohut
            38: "images/pamuk.jpg",  # Pamuk
            39: "images/pancar.jpg",  # Pancar
            40: "images/patates.jpg",  # Patates
            41: "images/patlican.jpg",  # Patlican
            42: "images/pazi.jpg",  # Pazi
            43: "images/pirinc.jpg",  # Pirinc
            44: "images/salatalik.jpeg",  # Salatalik
            45: "images/sarimsak.jpg",  # Sarimsak
            46: "images/seftali.jpg",  # Seftali
            47: "images/sogan.jpg",  # Sogan
            48: "images/tutun.jpg",  # Tutun
            49: "images/uzum.jpg",  # Uzum
            50: "images/yonca.jpg",  # Yonca
            51: "images/yulaf.jpg",  # Yulaf
            52: "images/zeytin.jpg",  # Zeytin
            53: "images/antepfistigi.jpg",  # Antepfistigi
        }

        # Tahmini değerlendiriyoruz
        if prediction[0] in dt_urun_dict:
            crop = dt_urun_dict[prediction[0]]
            image = dt_urun_images[prediction[0]]
            result = "{}".format(crop)
            return render_template('oneri.html', result=result, image=image)
        else:
            result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
            return render_template('oneri.html', result=result, image=None)
        # Sonucu döndür

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
    from flask import Flask, render_template, request

    app = Flask(__name__)


    class ToprakVerimlilik:
        def __init__(self, om, npk, max_om, max_npk):
            self.__om = om
            self.__npk = npk
            self.__max_om = max_om
            self.__max_npk = max_npk

        def hesapla_tfe(self):
            if (self.__max_om == 0) or (self.__max_npk == 0):
                raise ValueError("Maksimum Organik Madde Orani veya Maksimum Besin Miktari 0 Olamaz!")
            return (self.__om * self.__npk) / (self.__max_om * self.__max_npk)


    class SuKullanimiEndeksi:
        def __init__(self, mevcut_su, bitki_su_ihtiyaci):
            self.__mevcut_su = mevcut_su
            self.__bitki_su_ihtiyaci = bitki_su_ihtiyaci

        def hesapla_sye(self):
            if self.__bitki_su_ihtiyaci == 0:
                raise ValueError("Bitki Su İhtiyaci 0 Olamaz!")
            sye = self.__mevcut_su / self.__bitki_su_ihtiyaci
            return min(sye, 1)


    class IklimUygunlukKatsayisi:
        def __init__(self, mevcut_sicaklik, optimum_sicaklik):
            self.__mevcut_sicaklik = mevcut_sicaklik
            self.__optimum_sicaklik = optimum_sicaklik

        def hesapla_iak(self):
            if self.__optimum_sicaklik == 0:
                raise ValueError("Optimum Sicaklik 0 Olamaz!")
            iak = self.__mevcut_sicaklik / self.__optimum_sicaklik
            return min(iak, 1)


    class TarlaYonetimFaktoru:
        def __init__(self, gf, sf, zf):
            self.__gf = gf
            self.__sf = sf
            self.__zf = zf

        def hesapla_tmf(self):
            if not (0 <= self.__gf <= 1 and 0 <= self.__sf <= 1 and 0 <= self.__zf <= 1):
                raise ValueError("Katsayilar 0 ile 1 arasinda olmalidir.")
            tmf = self.__gf * self.__sf * self.__zf
            return tmf


    class HasatMiktari:
        def __init__(self, um, tfe, sye, iak, tmf):
            self.__um = um
            self.__tfe = tfe
            self.__sye = sye
            self.__iak = iak
            self.__tmf = tmf

        def hesapla_h(self):
            tfe = self.__tfe.hesapla_tfe()
            sye = self.__sye.hesapla_sye()
            iak = self.__iak.hesapla_iak()
            tmf = self.__tmf.hesapla_tmf()
            h = self.__um * tfe * sye * iak * tmf
            return h


    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            um = float(request.form['um'])
            om = float(request.form['om'])
            npk = float(request.form['npk'])
            max_om = float(request.form['max_om'])
            max_npk = float(request.form['max_npk'])
            mevcut_su = float(request.form['mevcut_su'])
            bitki_su_ihtiyaci = float(request.form['bitki_su_ihtiyaci'])
            mevcut_sicaklik = float(request.form['mevcut_sicaklik'])
            optimum_sicaklik = float(request.form['optimum_sicaklik'])
            gf = float(request.form['gf'])
            sf = float(request.form['sf'])
            zf = float(request.form['zf'])

            tfe_obj = ToprakVerimlilik(om, npk, max_om, max_npk)
            sye_obj = SuKullanimiEndeksi(mevcut_su, bitki_su_ihtiyaci)
            iak_obj = IklimUygunlukKatsayisi(mevcut_sicaklik, optimum_sicaklik)
            tmf_obj = TarlaYonetimFaktoru(gf, sf, zf)

            hasat = HasatMiktari(um, tfe_obj, sye_obj, iak_obj, tmf_obj)
            h = hasat.hesapla_h()

            return render_template('result.html', h=h, tfe=tfe_obj.hesapla_tfe(), sye=sye_obj.hesapla_sye(),
                                   iak=iak_obj.hesapla_iak(), tmf=tmf_obj.hesapla_tmf())

        return render_template('index.html')


    if __name__ == '__main__':
        app.run(debug=True)
