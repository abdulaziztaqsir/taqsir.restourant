import json
from abc import ABC, abstractmethod


# Ma'lumotlarni JSON faylda saqlash va yuklash
class MalumotlarBoshqaruvchisi:
    FAYL_NOMI = "malumotlar.json"

    @staticmethod
    def yuklash():
        try:
            with open(MalumotlarBoshqaruvchisi.FAYL_NOMI, "r") as fayl:
                return json.load(fayl)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"mijozlar": [], "buyurtmalar": [], "menyu": []}

    @staticmethod
    def saqlash(malumotlar):
        with open(MalumotlarBoshqaruvchisi.FAYL_NOMI, "w") as fayl:
            json.dump(malumotlar, fayl, indent=4)


# Abstraksiya - Restoran Entity
class RestoranEntity(ABC):
    @abstractmethod
    def malumot_korsat(self):
        pass


# Mijoz Class
class Mijoz(RestoranEntity):
    def __init__(self, ism, telefon):
        self.ism = ism
        self.telefon = telefon

    def malumot_korsat(self):
        return f"Mijoz: {self.ism}, Telefon: {self.telefon}"


# Menyu Elementi Class
class MenyuElementi(RestoranEntity):
    def __init__(self, nomi, narxi):
        self.nomi = nomi
        self.narxi = narxi

    def malumot_korsat(self):
        return f"Menyu: {self.nomi}, Narxi: ${self.narxi}"


# Buyurtma Class (Polimorfizm - turli malumot_korsat implementatsiyasi)
class Buyurtma(RestoranEntity):
    def __init__(self, mijoz, taomlar):
        self.mijoz = mijoz
        self.taomlar = taomlar
        self.jami_narx = sum(taom.narxi for taom in taomlar)

    def malumot_korsat(self):
        return f"Buyurtma: {self.mijoz.ism}, Taomlar: {', '.join(taom.nomi for taom in self.taomlar)} | Jami: ${self.jami_narx}"


# CRM Tizimi (Inkapsulatsiya & Meros)
class CRM:
    def __init__(self):
        self.malumotlar = MalumotlarBoshqaruvchisi.yuklash()
        self.mijozlar = [Mijoz(m["ism"], m["telefon"]) for m in self.malumotlar["mijozlar"]]
        self.menyu = [MenyuElementi(m["nomi"], m["narxi"]) for m in self.malumotlar["menyu"]]
        self.buyurtmalar = []

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
        print("Buyurtma muvaffaqiyatli berildi!")
        print(buyurtma.malumot_korsat())

    def mijozlar_korsat(self):
        for mijoz in self.mijozlar:
            print(mijoz.malumot_korsat())

    def menyuni_korsat(self):
        for taom in self.menyu:
            print(taom.malumot_korsat())


# Konsol Ilovasi
if __name__ == "__main__":
    crm = CRM()
    while True:
        print("\n---Taqsir.restourant---")
        print("\n1. Mijoz qo'shish")
        print("2. Menyuga taom qo'shish")
        print("3. Buyurtma berish")
        print("4. Mijozlarni ko'rish")
        print("5. Menyuni ko'rish")
        print("6. Chiqish")
        tanlov = input("Tanlang: ").strip()

        print(f"Tanlangan qiymat: '{tanlov}'")  # Diagnostika uchun

        if tanlov == "1":
            ism = input("Mijoz ismini kiriting: ")
            telefon = input("Telefon raqamini kiriting: ")
            crm.mijoz_qosh(ism, telefon)
        elif tanlov == "2":
            nomi = input("Taom nomini kiriting: ")
            narxi = float(input("Narxini kiriting: "))
            crm.menyuga_qosh(nomi, narxi)
        elif tanlov == "3":
            ism = input("Mijoz ismini kiriting: ")
            taomlar = input("Buyurtma taomlarini kiriting (vergul bilan ajrating): ").split(",")
            crm.buyurtma_ber(ism, [t.strip() for t in taomlar])
        elif tanlov == "4":
            crm.mijozlar_korsat()
        elif tanlov == "5":
            crm.menyuni_korsat()
        elif tanlov == "6":
            break
        else:
            print("Noto'g'ri tanlov, qayta urinib ko'ring!")
