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

