#HASAT MIKTARI BULMA
#Derste Lemi Orhan Bey'in setter ve getterlar hakkinda yorumunu dinlemis olsak da yine de biz kullanmayi tercih ettik.

class ToprakVerimlilik:
    def __init__(self, om, npk, max_om, max_npk):
        # Private degiskenler
        self.__om = om                # Organik madde orani
        self.__npk = npk              # Besin maddeleri toplami
        self.__max_om = max_om         # Maksimum organik madde orani
        self.__max_npk = max_npk       # Maksimum besin miktari

    # Getter ve Setter
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
        if (self.__max_om == 0) or (self.__max_npk == 0):  # Bolme hatasini engellemek icin
            raise ValueError("Maksimum Organik Madde Orani veya Maksimum Besin Miktari 0 Olamaz! Lutfen Degistirin.")
        return (self.__om * self.__npk) / (self.__max_om * self.__max_npk)


class SuKullanimiEndeksi:
    def __init__(self, mevcut_su, bitki_su_ihtiyaci):
        # Private degiskenler
        self.__mevcut_su = mevcut_su
        self.__bitki_su_ihtiyaci = bitki_su_ihtiyaci

    # Getter ve Setter
    def get_mevcut_su(self):
        return self.__mevcut_su

    def set_mevcut_su(self, mevcut_su):
        self.__mevcut_su = mevcut_su

    def get_bitki_su_ihtiyaci(self):
        return self.__bitki_su_ihtiyaci

    def set_bitki_su_ihtiyaci(self, bitki_su_ihtiyaci):
        self.__bitki_su_ihtiyaci = bitki_su_ihtiyaci

    def hesapla_sye(self):
        if self.__bitki_su_ihtiyaci == 0:  # Bolme hatasini engellemek icin
            raise ValueError("Bitki Su İhtiyaci 0 Olamaz! Lutfen Degistirin.")
        sye = self.__mevcut_su / self.__bitki_su_ihtiyaci
        return min(sye, 1)  


class IklimUygunlukKatsayisi:
    def __init__(self, mevcut_sicaklik, optimum_sicaklik):
        # Private degiskenler
        self.__mevcut_sicaklik = mevcut_sicaklik
        self.__optimum_sicaklik = optimum_sicaklik

    # Getter ve Setter
    def get_mevcut_sicaklik(self):
        return self.__mevcut_sicaklik

    def set_mevcut_sicaklik(self, mevcut_sicaklik):
        self.__mevcut_sicaklik = mevcut_sicaklik

    def get_optimum_sicaklik(self):
        return self.__optimum_sicaklik

    def set_optimum_sicaklik(self, optimum_sicaklik):
        self.__optimum_sicaklik = optimum_sicaklik

    def hesapla_iak(self):
        if self.__optimum_sicaklik == 0:  # Bolme hatasini engellemek icin
            raise ValueError("Optimum Sicaklik 0 Olamaz! Lutfen Degistirin.")
        iak = self.__mevcut_sicaklik / self.__optimum_sicaklik
        return min(iak, 1)  # IAK > 1 ise 1 olarak kabul edilir


class TarlaYonetimFaktoru:
    def __init__(self, gf, sf, zf):
        # Private degiskenler
        self.__gf = gf  # Gubreleme Katsayisi
        self.__sf = sf  # Sulama Yonetimi Katsayisi
        self.__zf = zf  # Zararli Yonetimi Katsayisi

    # Getter ve Setter
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
            raise ValueError("Katsayilar 0 ile 1 arasinda olmalidir. Lutfen Degistirin.")
        tmf = self.__gf * self.__sf * self.__zf
        return tmf

#Hasat Miktari hesaplayan sinif
class HasatMiktari:
    def __init__(self, um, tfe, sye, iak, tmf):
        """
        um: Ekilen urun miktari (kg/da)
        tfe: Toprak Verimlilik Endeksi
        sye: Su Kullanimi Endeksi 
        iak: Iklim Uygunluk Katsayisi 
        tmf: Tarla Yonetimi Faktoru 
        """
        self.__um = um
        self.__tfe = tfe
        self.__sye = sye
        self.__iak = iak
        self.__tmf = tmf

    # Getter ve Setter
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

if __name__ == "__main__":
     # Kullanicidan giris alinmasi
    print("Lutfen asagidaki degerleri giriniz :")
    um = float(input("Ektiginiz Urun Miktari [kg/da] :"))
    om = float(input("Toprak Organik Madde Orani (OM) [%] :"))
    npk = float(input("Toplam Besin Miktari (NPK) [kg/da] :"))
    max_om = float(input("Maksimum Organik Madde Orani (maxOM) [%] :"))
    max_npk = float(input("Maksimum Besin Miktari (maxNPK) [kg/da] :"))
    mevcut_su = float(input("Mevcut Su Miktari [mm] :"))
    bitki_su_ihtiyaci = float(input("Bitki Su Ihtiyaci [mm] :"))
    mevcut_sicaklik = float(input("Mevcut Sicaklik [C°] :"))
    optimum_sicaklik = float(input("Optimum Sicaklik [C°] :"))
    gf = float(input("Gubreleme Katsayisi (0-1) :"))
    sf = float(input("Sulama Yonetimi Katsayisi (0-1) :"))
    zf = float(input("Zararli Yonetimi Katsayisi (0-1) :"))

    # Siniflardan nesne olusturulmasi
    tfe_obj = ToprakVerimlilik(om, npk, max_om, max_npk)
    sye_obj = SuKullanimiEndeksi(mevcut_su, bitki_su_ihtiyaci)
    iak_obj = IklimUygunlukKatsayisi(mevcut_sicaklik, optimum_sicaklik)
    tmf_obj = TarlaYonetimFaktoru(gf, sf, zf)

    # Hasat miktarini hesaplama
    hasat = HasatMiktari(um, tfe_obj, sye_obj, iak_obj, tmf_obj)
    h = hasat.hesapla_h()

    # Sonuçlarin ekrana yazdirilmasi
    print(f"\nToprak Verimlilik Endeksi (TFE): {tfe_obj.hesapla_tfe():.2f}")
    print(f"Su Kullanimi Endeksi (SYE): {sye_obj.hesapla_sye():.2f}")
    print(f"Iklim Uygunluk Katsayisi (IAK): {iak_obj.hesapla_iak():.2f}")
    print(f"Tarla Yonetimi Faktoru (TMF): {tmf_obj.hesapla_tmf():.2f}")
    print(f"\nHasat Miktari (H): {h:.2f} kg/da")

