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
            "guneydogu": "Guneydogu Anadolu Bolgesi",
            "guneydoğu bolgesi": "Guneydogu Anadolu Bolgesi",
            "guneydogu bolgesi": "Guneydogu Anadolu Bolgesi",
            "güneydoğu": "Guneydogu Anadolu Bolgesi",
            "güneydoğu bölgesi": "Guneydogu Anadolu Bolgesi",
            "iç anadolu" : "Ic Anadolu Bolgesi",
            "iç anadolu bölgesi": "Ic Anadolu Bolgesi",
            "ıc anadolu bolgesi": "Ic Anadolu Bolgesi",
            "ıc anadolu": "Ic Anadolu Bolgesi",

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
            1: "https://www.istockphoto.com/tr/foto%C4%9Fraflar/armut",  # Armut
            2: "https://www.serkatarim.com.tr/arpa-nasil-yetistirilir/",  # Arpa
            3: "https://osterras.com/aycicegi/",  # Aycicegi
            4: "https://www.e-fidancim.com/urun/geleneksel-tatlilik-recelllik-balkabagi-fidesi-5-adet",  # Balkabagi
            5: "https://www.tohumevi.com.tr/urun/sultani-bamya-tohumu",  # Bamya
            6: "https://cookidoo.com.tr/recipes/recipe/tr-TR/r751324",  # Bezelye
            7: "https://www.nefisyemektarifleri.com/blog/biber-cesitleri-ve-faydalari-nelerdir/",  # Biber
            8: "https://www.demircibahcesi.com/taze-borulce",  # Borulce
            9: "https://www.auroracereali.com/tr/prodotto/ekmeklik-bugday/",  # Bugday
            10: "https://ciftcideneve.com/urun/5575/organik-cavdar-dogal-organik-dogal-organik-bugday-ve-bulgur",  # Cavdar
            11: "https://pixabay.com/tr/photos/%C3%A7ay-tarlas%C4%B1-/",  # Cay
            12: "https://www.bakkalhasan.com/urun/ceviz-kabuklu-maras-18-yayla-10-kg-cok-cok-al-cok-az-daha-ode",  # Ceviz
            13: "https://www.agrowy.com/bitki-yetistiriciligi/cilek-yetistiriciligi",  # Cilek
            14: "https://www.medicalpark.com.tr/domatesin-zararlari/hg-3885",  # Domates
            15: "https://www.sadahastanesi.com/tr/1-elma-kac-kalori-elmanin-besin-degeri",  # Elma
            16: "https://www.buyukanadoluhastanesi.com/haber/2190/erigin-faydalari-erik-tuketmeniz-icin-11-neden",  # Erik
            17: "https://www.tarimdunyasi.net/2023/08/15/taze-fasulye-neden-100-lira-oldu/",  # Fasulye
            18: "https://www.altungida.com.tr/findik-nedir/",  # Findik
            19: "https://www.ozgurleblebi.com/Cig-Kabuklu-Fistik",  # Fistik
            20: "https://www.tohumevi.com.tr/urun/kirmizi-gul-fidani-yediveren-kokulu",  # Gul
            21: "https://www.google.com/imgres?q=ha%C5%9Fha%C5%9F%20foto&imgurl=https%3A%2F%2Fwww.demirbasmakina.com%2Fimaj%2Fblog-gorselleri%2Fhashas-ezmesi-nerede-kullanilir-demirbas.jpg&imgrefurl=https%3A%2F%2Fwww.demirbasmakina.com%2Fhashas-ezmesi-nerede-kullanilir&docid=p-1H76D-gRbA6M&tbnid=Id0IBieB9Qf6XM&vet=12ahUKEwiqkLey6cOKAxUNVfEDHao7IDcQM3oECH4QAA..i&w=900&h=592&hcb=2&ved=2ahUKEwiqkLey6cOKAxUNVfEDHao7IDcQM3oECH4QAA",
            # Hashas
            22: "https://www.google.com/imgres?q=incir%20foto&imgurl=https%3A%2F%2Fwww.tazekuru.com%2FUserFiles%2FFotograflar%2F148-70-buyuk-jpg-70-buyuk.jpg&imgrefurl=https%3A%2F%2Fwww.tazekuru.com%2Fkurutulmus-incir-map-paket-50gr&docid=JRHAtKJKVkUQqM&tbnid=agiwn7Bn8MybPM&vet=12ahUKEwiHpdK96cOKAxXuVPEDHWfoItEQM3oECBcQAA..i&w=700&h=700&hcb=2&ved=2ahUKEwiHpdK96cOKAxXuVPEDHWfoItEQM3oECBcQAA",  # Incir
            23: "http://t2.gstatic.com/licensed-image?q=tbn:ANd9GcRSD4__jt0WNMkqOCyLMnCg6rYIrt909b6pVEqZOLVFLW1cNeRuEsfgQNJQWIqceCcc",  # Karpuz
            24: "https://www.zengardentr.com/urun/altin-kalpler-kavun-tohumu-geleneksel-hearts-of-gold-melon-1",  # Kavun
            25: "https://www.medicalpark.com.tr/kayisi-cekirdegi-faydalari/hg-4028",  # Kayisi
            26: "https://misbell.net/kestane-cesitleri/",  # Kestane
            27: "http://www.saygifidancilik.com/kiraz/",  # Kiraz
            28: "https://www.medicalpark.com.tr/kivinin-faydalari/hg-2933",  # Kivi
            29: "https://tohumbaba.com/urun/lahana-tohumu/",  # Lahana
            30: "https://www.lezzet.com.tr/lezzetten-haberler/limon-nasil-secilir",  # Limon
            31: "https://tr.wikipedia.org/wiki/Marul",  # Marul
            32: "https://surmeliciftligi.com/urun/kirmizi-mercimek-kg/",  # Mercimek
            33: "https://abptds.com/misir-kurutma-neden-onemlidir/",  # Misir
            34: "https://www.organikciyizbiz.com/organik-muz-organik-ufuklar",  # Muz
            35: "https://upload.wikimedia.org/wikipedia/commons/6/6e/Pomegranate.jpg",  # Nar
            36: "https://www.cnnturk.com/saglik/narin-faydalari-nelerdir-nelere-iyi-gelir-nar-nasil-tuketilir-ne-ise-yarar-1688140",  # Narenciye
            37: "https://upload.wikimedia.org/wikipedia/commons/e/ec/Chickpeas.jpg",  # Nohut
            38: "https://upload.wikimedia.org/wikipedia/commons/2/22/Cotton_plant_bolls.jpg",  # Pamuk
            39: "https://upload.wikimedia.org/wikipedia/commons/c/ca/Sugar_Beet.jpg",  # Pancar
            40: "https://upload.wikimedia.org/wikipedia/commons/d/de/Brown_Potato.jpg",  # Patates
            41: "https://upload.wikimedia.org/wikipedia/commons/e/e2/Eggplant.jpg",  # Patlican
            42: "https://upload.wikimedia.org/wikipedia/commons/4/44/New_Zealand_Spinach.jpg",  # Pazi
            43: "https://upload.wikimedia.org/wikipedia/commons/5/57/Rice-Plant.jpg",  # Pirinc
            44: "https://upload.wikimedia.org/wikipedia/commons/9/96/Cucumber01.jpg",  # Salatalik
            45: "https://upload.wikimedia.org/wikipedia/commons/4/47/Sarimsak.JPG",  # Sarimsak
            46: "https://upload.wikimedia.org/wikipedia/commons/3/34/Peach.jpg",  # Seftali
            47: "https://upload.wikimedia.org/wikipedia/commons/c/cf/Onions.jpg",  # Sogan
            48: "https://upload.wikimedia.org/wikipedia/commons/a/ae/Tobacco_Field.jpg",  # Tutun
            49: "https://upload.wikimedia.org/wikipedia/commons/6/63/Grapes.jpg",  # Uzum
            50: "https://upload.wikimedia.org/wikipedia/commons/d/db/Alfalfa.jpg",  # Yonca
            51: "https://upload.wikimedia.org/wikipedia/commons/0/0c/Oats.jpg",  # Yulaf
            52: "https://upload.wikimedia.org/wikipedia/commons/e/e7/Olive_Tree.jpg",  # Zeytin
            53: "https://upload.wikimedia.org/wikipedia/commons/f/fa/Pistachio_tree.jpg",  # Antepfistigi
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