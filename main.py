import json
from abc import ABC, abstractmethod


class MalumotlarBoshqaruvchisi:
    FAYL_NOMI = "malumotlar.json"

    @staticmethod
    def yuklash():
        try:
            with open(MalumotlarBoshqaruvchisi.FAYL_NOMI, "r") as fayl:
                return json.load(fayl)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"mijozlar": [], "buyurtmalar": [], "menyu": [], "xodimlar": [], "parkofka": []}

    @staticmethod
    def saqlash(malumotlar):
        with open(MalumotlarBoshqaruvchisi.FAYL_NOMI, "w") as fayl:
            json.dump(malumotlar, fayl, indent=4)


class RestoranEntity(ABC):
    @abstractmethod
    def malumot_korsat(self):
        pass


class Mijoz(RestoranEntity):
    def __init__(self, ism, telefon):
        self.ism = ism
        self.telefon = telefon

    def malumot_korsat(self):
        return f"Mijoz: {self.ism}, Telefon: {self.telefon}"


class MenyuElementi(RestoranEntity):
    def __init__(self, nomi, narxi):
        self.nomi = nomi
        self.narxi = narxi

    def malumot_korsat(self):
        return f"Menyu: {self.nomi}, Narxi: ${self.narxi}"


class Buyurtma(RestoranEntity):
    def __init__(self, mijoz, taomlar):
        self.mijoz = mijoz
        self.taomlar = taomlar
        self.jami_narx = sum(taom.narxi for taom in taomlar)

    def malumot_korsat(self):
        return f"Buyurtma: {self.mijoz.ism}, Taomlar: {', '.join(taom.nomi for taom in self.taomlar)} | Jami: ${self.jami_narx}"


class Xodim(RestoranEntity):
    def __init__(self, ism, lavozim):
        self.ism = ism
        self.lavozim = lavozim

    def malumot_korsat(self):
        return f"Xodim: {self.ism}, Lavozim: {self.lavozim}"


class RestoranParkofkasi:
    def __init__(self):
        self.parkofka = []

    def mashina_qosh(self, raqam):
        self.parkofka.append(raqam)
        print("Mashina parkofkaga qo'shildi!")

    def mashinalarni_korsat(self):
        print("Parkofkada turgan mashinalar:", ", ".join(self.parkofka))


class Hisobot:
    @staticmethod
    def kunlik_hisobot(buyurtmalar):
        jami_summa = sum(b.jami_narx for b in buyurtmalar)
        print(f"Kunlik tushum: ${jami_summa}")
        print(f"Jami buyurtmalar soni: {len(buyurtmalar)}")


class CRM:
    def __init__(self):
        self.malumotlar = MalumotlarBoshqaruvchisi.yuklash()
        self.malumotlar["buyurtmalar"] = []  # Eski buyurtmalarni tozalash
        self.mijozlar = [Mijoz(m["ism"], m["telefon"]) for m in self.malumotlar.get("mijozlar", [])]
        self.menyu = [MenyuElementi(m["nomi"], m["narxi"]) for m in self.malumotlar.get("menyu", [])]
        self.buyurtmalar = []  # Toza buyurtmalar ro'yxati
        self.xodimlar = [Xodim(x["ism"], x["lavozim"]) for x in self.malumotlar.get("xodimlar", [])]
        self.parkofka = RestoranParkofkasi()

    def mijoz_qosh(self, ism, telefon):
        mijoz = Mijoz(ism, telefon)
        self.mijozlar.append(mijoz)
        self.malumotlar["mijozlar"].append({"ism": ism, "telefon": telefon})
        MalumotlarBoshqaruvchisi.saqlash(self.malumotlar)
        print("Mijoz qo'shildi!")

    def menyuga_qosh(self, nomi, narxi):
        taom = MenyuElementi(nomi, narxi)
        self.menyu.append(taom)
        self.malumotlar["menyu"].append({"nomi": nomi, "narxi": narxi})
        MalumotlarBoshqaruvchisi.saqlash(self.malumotlar)
        print("Menyu elementi qo'shildi!")

    def buyurtma_ber(self, mijoz_ismi, taom_nomi):
        mijoz = next((m for m in self.mijozlar if m.ism == mijoz_ismi), None)
        if not mijoz:
            print("Mijoz topilmadi!")
            return

        taomlar = [t for t in self.menyu if t.nomi in taom_nomi]
        if not taomlar:
            print("Menyudan taom topilmadi!")
            return

        buyurtma = Buyurtma(mijoz, taomlar)
        self.buyurtmalar.append(buyurtma)
        self.malumotlar["buyurtmalar"].append({"mijoz": mijoz.ism, "taomlar": taom_nomi})
        MalumotlarBoshqaruvchisi.saqlash(self.malumotlar)
        print("Buyurtma muvaffaqiyatli berildi!")
        print(buyurtma.malumot_korsat())


if __name__ == "__main__":
    crm = CRM()

    # Parkofka
    crm.parkofka.mashina_qosh("01.001.RRR")
    crm.parkofka.mashinalarni_korsat()

    # Mijoz
    crm.mijoz_qosh("Azimjon", "+998 94 480 49 00")

    # Menyuga Taomlar qoshish
    crm.menyuga_qosh("Osh", 50.0)
    crm.menyuga_qosh("Shashlik", 30.0)

    # Buyurtma qilish
    crm.buyurtma_ber("Ali", ["Osh", "Shashlik"])

    # Kunlik hisobot
    Hisobot.kunlik_hisobot(crm.buyurtmalar)
