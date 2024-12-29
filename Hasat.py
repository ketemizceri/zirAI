from flask import Flask, render_template, request
from math import isclose

app = Flask(__name__)

# Toprak Verimlilik, Su Kullanimi Endeksi, Iklim Uygunluk Katsayisi, Tarla Yonetimi Faktoru, Hasat Miktari sınıflarını aynen bırakıyoruz

class ToprakVerimlilik:
    def __init__(self, om, npk, max_om, max_npk):
        self.__om = om
        self.__npk = npk
        self.__max_om = max_om
        self.__max_npk = max_npk

    def get_om(self):
        return self.__om

    def set_om(self, om):
        self.__om = om

    def get_npk(self):
        return self.__npk

    def set_npk(self, npk):
        self.__npk = npk

    def get_max_om(self):
        return self.__max_om

    def set_max_om(self, max_om):
        self.__max_om = max_om

    def get_max_npk(self):
        return self.__max_npk

    def set_max_npk(self, max_npk):
        self.__max_npk = max_npk

    def hesapla_tfe(self):
        if self.__max_om == 0 or self.__max_npk == 0:
            raise ValueError("Maksimum Organik Madde Orani veya Maksimum Besin Miktari 0 Olamaz!")
        return (self.__om * self.__npk) / (self.__max_om * self.__max_npk)


class SuKullanimiEndeksi:
    def __init__(self, mevcut_su, bitki_su_ihtiyaci):
        self.__mevcut_su = mevcut_su
        self.__bitki_su_ihtiyaci = bitki_su_ihtiyaci

    def get_mevcut_su(self):
        return self.__mevcut_su

    def set_mevcut_su(self, mevcut_su):
        self.__mevcut_su = mevcut_su

    def get_bitki_su_ihtiyaci(self):
        return self.__bitki_su_ihtiyaci

    def set_bitki_su_ihtiyaci(self, bitki_su_ihtiyaci):
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

    def get_mevcut_sicaklik(self):
        return self.__mevcut_sicaklik

    def set_mevcut_sicaklik(self, mevcut_sicaklik):
        self.__mevcut_sicaklik = mevcut_sicaklik

    def get_optimum_sicaklik(self):
        return self.__optimum_sicaklik

    def set_optimum_sicaklik(self, optimum_sicaklik):
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

    def get_gf(self):
        return self.__gf

    def set_gf(self, gf):
        self.__gf = gf

    def get_sf(self):
        return self.__sf

    def set_sf(self, sf):
        self.__sf = sf

    def get_zf(self):
        return self.__zf

    def set_zf(self, zf):
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

    def get_um(self):
        return self.__um

    def set_um(self, um):
        self.__um = um

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
        # Kullanıcıdan gelen verileri al
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

        # Nesneleri oluştur
        tfe_obj = ToprakVerimlilik(om, npk, max_om, max_npk)
        sye_obj = SuKullanimiEndeksi(mevcut_su, bitki_su_ihtiyaci)
        iak_obj = IklimUygunlukKatsayisi(mevcut_sicaklik, optimum_sicaklik)
        tmf_obj = TarlaYonetimFaktoru(gf, sf, zf)

        # Hasat miktarını hesapla
        hasat = HasatMiktari(um, tfe_obj, sye_obj, iak_obj, tmf_obj)
        h = hasat.hesapla_h()

        # Sonuçları render et
        return render_template('result.html', h=h, tfe=tfe_obj.hesapla_tfe(), sye=sye_obj.hesapla_sye(), iak=iak_obj.hesapla_iak(), tmf=tmf_obj.hesapla_tmf())

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
