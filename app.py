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
            "akdeniz": "Akdeniz Bolgesi",
            "akdeniz bolgesi": "Akdeniz Bolgesi",
            "akdeniz bölgesi": "Akdeniz Bolgesi",
            "dogu anadolu": "Doguanadolu Bolgesi",
            "doguanadolu bolgesi": "Doguanadolu Bolgesi",
            "doğu anadolu": "Doguanadolu Bolgesi",
            "doğu anadolu bölgesi": "Doguanadolu Bolgesi",
            "guneydogu": "Guneydogu Bolgesi",
            "guneydoğu bolgesi": "Guneydogu Bolgesi",
            "guneydogu bolgesi": "Guneydogu Bolgesi",
            "güneydoğu": "Guneydogu Bolgesi",
            "güneydoğu bölgesi": "Guneydogu Bolgesi",

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
            1: "https://upload.wikimedia.org/wikipedia/commons/f/f8/Pear_Fruit.JPG",  # Armut
            2: "https://upload.wikimedia.org/wikipedia/commons/a/ab/ARPA_1.JPG",  # Arpa
            3: "https://upload.wikimedia.org/wikipedia/commons/4/47/A_sunflower.jpg",  # Aycicegi
            4: "https://upload.wikimedia.org/wikipedia/commons/6/6e/Cucurbita_pepo.jpg",  # Balkabagi
            5: "https://upload.wikimedia.org/wikipedia/commons/a/aa/Bamya.JPG",  # Bamya
            6: "https://upload.wikimedia.org/wikipedia/commons/9/91/Pea_pods.jpg",  # Bezelye
            7: "https://upload.wikimedia.org/wikipedia/commons/5/5c/Assorted_Peppers.jpg",  # Biber
            8: "https://upload.wikimedia.org/wikipedia/commons/a/a0/Borulce.jpg",  # Borulce
            9: "https://upload.wikimedia.org/wikipedia/commons/5/51/Triticum_aestivum.JPG",  # Bugday
            10: "https://upload.wikimedia.org/wikipedia/commons/2/2b/Rye_field.jpg",  # Cavdar
            11: "https://upload.wikimedia.org/wikipedia/commons/c/c8/Tea_leaves.jpg",  # Cay
            12: "https://upload.wikimedia.org/wikipedia/commons/3/3f/Still-life-with-walnuts.jpg",  # Ceviz
            13: "https://upload.wikimedia.org/wikipedia/commons/d/d4/Strawberries.jpg",  # Cilek
            14: "https://upload.wikimedia.org/wikipedia/commons/8/89/Tomato_je.jpg",  # Domates
            15: "https://upload.wikimedia.org/wikipedia/commons/1/15/Red_Apple.jpg",  # Elma
            16: "https://upload.wikimedia.org/wikipedia/commons/b/bb/Plum_purple.jpg",  # Erik
            17: "https://upload.wikimedia.org/wikipedia/commons/1/1b/Green_Beans.jpg",  # Fasulye
            18: "https://upload.wikimedia.org/wikipedia/commons/2/22/Hazelnuts.jpg",  # Findik
            19: "https://upload.wikimedia.org/wikipedia/commons/3/31/Pistachio_macro_white_background.jpg",  # Fistik
            20: "https://upload.wikimedia.org/wikipedia/commons/a/a5/Rose_flower.jpg",  # Gul
            21: "https://upload.wikimedia.org/wikipedia/commons/4/41/Papaver_somniferum_%28opium_poppy%29.jpg",
            # Hashas
            22: "https://upload.wikimedia.org/wikipedia/commons/7/71/Ripe_Fig.jpg",  # Incir
            23: "https://upload.wikimedia.org/wikipedia/commons/3/3e/Watermelon.jpg",  # Karpuz
            24: "https://upload.wikimedia.org/wikipedia/commons/4/43/Cantaloupe.jpg",  # Kavun
            25: "https://upload.wikimedia.org/wikipedia/commons/2/2f/Apricot.jpg",  # Kayisi
            26: "https://upload.wikimedia.org/wikipedia/commons/7/75/Chestnuts.jpg",  # Kestane
            27: "https://upload.wikimedia.org/wikipedia/commons/a/a6/Sweet_Cherry.jpg",  # Kiraz
            28: "https://upload.wikimedia.org/wikipedia/commons/a/ac/Kivi_on_tree.jpg",  # Kivi
            29: "https://upload.wikimedia.org/wikipedia/commons/a/a8/Cabbage.jpg",  # Lahana
            30: "https://upload.wikimedia.org/wikipedia/commons/c/cd/Lemon.jpg",  # Limon
            31: "https://upload.wikimedia.org/wikipedia/commons/a/a8/Lettuce_Mar._2014_01.jpg",  # Marul
            32: "https://upload.wikimedia.org/wikipedia/commons/1/15/Lentils_Flowers.jpg",  # Mercimek
            33: "https://upload.wikimedia.org/wikipedia/commons/f/fc/Sweetcorn_crop.JPG",  # Misir
            34: "https://upload.wikimedia.org/wikipedia/commons/5/5d/Banana_on_tree.jpg",  # Muz
            35: "https://upload.wikimedia.org/wikipedia/commons/6/6e/Pomegranate.jpg",  # Nar
            36: "https://upload.wikimedia.org/wikipedia/commons/1/14/Tangerines.jpg",  # Narenciye
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
            result = "{} en iyi ürün bu.".format(crop)

        else:
            result = "Sorry, we could not determine the best crop to be cultivated with the provided data."

        # Sonucu döndür
        return render_template('oneri.html', result=result)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)