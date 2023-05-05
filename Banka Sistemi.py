from tkinter import *
import sqlite3, os
from tkinter import messagebox

class BankaSistemiGiriş():
    def __init__(self):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.gui()

    def gui(self):
        self.window = Tk()
        self.window.title("Lessy Bankası")
        self.window.geometry("500x350")
        self.window.config(background = "#808080")

        # Labels

        kartNoL = Label(self.window, text = "Kart No:", background = "#808080", font = "Courier 11 bold")
        kartNoL.pack(), kartNoL.place(x = 60, y = 110)

        sifreL = Label(self.window, text = "Şifre:", background = "#808080", font = "Courier 11 bold")
        sifreL.pack(), sifreL.place(x = 60, y = 150)

        # Entries

        self.kartNoE = Entry(self.window, background = "#808080", font = "Courier 11 bold")
        self.kartNoE.pack(), self.kartNoE.place(x = 240, y = 110)

        self.sifreE = Entry(self.window, background = "#808080", font = "Courier 11 bold", show = "*")
        self.sifreE.pack(), self.sifreE.place(x = 240, y = 150)

        # Button

        kayitOlB = Button(self.window, text = "Kayıt ol", width = 9, border = True, borderwidth = 3, background = "#808080", highlightcolor = "yellow", highlightthickness = 1, command = self.kayitOl)
        kayitOlB.pack(), kayitOlB.place(x = 180, y = 270)

        girişYapB = Button(self.window, text = "Giriş yap", width = 9, border = True, borderwidth = 3, background = "#808080", highlightcolor = "yellow", highlightthickness = 1, command = self.girisYap)
        girişYapB.pack(), girişYapB.place(x = 265, y = 270)

        self.window.mainloop()

    def kayitOl(self):
        # Get entries 

        kartNo = int(self.kartNoE.get())
        sifre  = self.sifreE.get()

        # Database connection

        conn = sqlite3.connect(f"{self.path}/veritabani.db")
        cursor = conn.cursor()

        # Create table - if not exists - 

        cursor.execute("""CREATE TABLE IF NOT EXISTS bilgiler(
                    KartNo int,
                    Şifre text,
                    Bakiye int
                    )""")

        cursor.execute(f"""SELECT * FROM bilgiler WHERE KartNo = {kartNo} """)
        user = cursor.fetchone()
        
        if user != None:
            messagebox.showerror(title = "Hata!", message = "Kullanıcı zaten kayıtlı!")
        else:
            messagebox.showinfo(title = "Başarılı!", message = "Kayıt olundu!")
            cursor.execute(f"INSERT INTO bilgiler VALUES('{kartNo}','{sifre}', {0})")

        conn.commit()
        conn.close()

    def girisYap(self):
        # Get entries 
        
        kartNo = int(self.kartNoE.get())
        sifre  = self.sifreE.get()

        # Database connection

        conn = sqlite3.connect(f"{self.path}/veritabani.db")
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM bilgiler WHERE KartNo = {kartNo} """)
        user = cursor.fetchone()

        try:
            if sifre == user[1]:
                messagebox.showinfo(title = "Başarılı!", message = "Giriş yapıldı!")

        except:
            messagebox.showerror(title = "Hata!", message = "Giriş başarısız!")
        conn.commit()
        conn.close()


        self.window.destroy()
        Run = BankaSistemi(kartNo, user[2])

class BankaSistemi():
    def __init__(self, kartNo, bakiye):
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.kartNo = kartNo
        self.bakiye = bakiye
        self.gui()

    def gui(self):
        self.window = Tk()
        self.window.title("Lessy Bankası")
        self.window.geometry("550x150")
        self.window.config(background = "#808080")

        kartNoL = Label(self.window, text = f"Kart No: {self.kartNo}", font = "Courier 11 bold", background = "#808080")
        kartNoL.pack(), kartNoL.place(x = 180, y = 10)

        bakiyeGoruntuleB = Button(self.window, width = 14, text = "Bakiye görüntüle", background = "#808080", highlightthickness = 1, borderwidth = 3, command = self.bakiyeGoruntule)
        bakiyeGoruntuleB.pack(), bakiyeGoruntuleB.place(x = 10, y = 75)
        
        paraCekB = Button(self.window, width = 14, text = "Para çek", background = "#808080", highlightthickness = 1, borderwidth = 3, command = self.paraCek)
        paraCekB.pack(), paraCekB.place(x = 10, y = 110)

        paraYatirB = Button(self.window, width = 14, text = "Para yatır", background = "#808080", highlightthickness = 1, borderwidth = 3, command = self.paraYatir)
        paraYatirB.pack(), paraYatirB.place(x = 430, y = 75)
        
        cikisB = Button(self.window, width = 14, text = "Çıkış", background = "#808080", highlightthickness = 1, borderwidth = 3, command = lambda : quit())
        cikisB.pack(), cikisB.place(x = 430, y = 110)

        self.window.mainloop()

    def bakiyeGoruntule(self):
        conn = sqlite3.connect(f"{self.path}/veritabani.db")
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM bilgiler WHERE KartNo = {self.kartNo} """)
        user = cursor.fetchone()
        self.bakiye = user[2]

        windowT = Toplevel(self.window)
        windowT.title("Bakiye görüntüle"), windowT.geometry("300x200"), windowT.config(background = "#808080")
        
        bakiyeL = Label(windowT, text = f"Bakiyeniz: {self.bakiye}", font = "Courier 12 bold", background = "#808080")
        bakiyeL.pack(), bakiyeL.place(x = 85, y = 80)
        
        windowT.mainloop()

    def paraCek(self):
        conn = sqlite3.connect(f"{self.path}/veritabani.db")
        cursor = conn.cursor()

        self.windowT = Toplevel(self.window)
        self.windowT.title("Para çek"), self.windowT.geometry("400x200"), self.windowT.config(background = "#808080")

        cekilecekMiktarL = Label(self.windowT, text = f"Çekilecek miktarı giriniz", font = "Courier 12 bold", background = "#808080")
        cekilecekMiktarL.pack(), cekilecekMiktarL.place(x = 75, y = 40)

        self.cekilecekMiktarE = Entry(self.windowT, font = "Courier 10 bold", background = "#808080")
        self.cekilecekMiktarE.pack(), self.cekilecekMiktarE.place(x = 125, y = 95)

        onaylaB = Button(self.windowT, text = "Onayla", background = "#808080", width = 14, highlightthickness = 1, borderwidth = 3, command = self.paraCekCommand)
        onaylaB.pack(), onaylaB.place(x = 152, y = 150)

        cursor.execute(f"""UPDATE bilgiler SET Bakiye = 50 WHERE KartNo = {self.kartNo}""")

    def paraYatir(self):
        self.windowT = Toplevel(self.window)
        self.windowT.title("Para çek"), self.windowT.geometry("400x200"), self.windowT.config(background = "#808080")

        yatirilacakMiktarL = Label(self.windowT, text = f"Yatıralacak miktarı giriniz", font = "Courier 12 bold", background = "#808080")
        yatirilacakMiktarL.pack(), yatirilacakMiktarL.place(x = 60, y = 30)

        self.yatirilacakMiktarE = Entry(self.windowT, font = "Courier 10 bold", background = "#808080")
        self.yatirilacakMiktarE.pack(), self.yatirilacakMiktarE.place(x = 120, y = 95)

        onaylaB = Button(self.windowT, text = "Onayla", background = "#808080", width = 14, highlightthickness = 1, borderwidth = 3, command = self.paraYatirCommand)
        onaylaB.pack(), onaylaB.place(x = 147, y = 150)

    def paraCekCommand(self):
        cekilecekMiktar = int(self.cekilecekMiktarE.get())

        if cekilecekMiktar <= self.bakiye:
            messagebox.showinfo(title = "Başarılı!", message = "Para başarıyla çekildi!")
            self.bakiye -= cekilecekMiktar

            conn = sqlite3.connect(f"{self.path}/veritabani.db")
            cursor = conn.cursor()
            
            cursor.execute(f"""UPDATE bilgiler SET Bakiye = {self.bakiye} WHERE KartNo = {self.kartNo}""")
            conn.commit()
            conn.close()
            self.windowT.destroy()

        else:
            messagebox.showerror(title = "Hata!", message = "Yetersiz bakiye!")

    def paraYatirCommand(self):
        yatirilacakMiktar = int(self.yatirilacakMiktarE.get())

        messagebox.showinfo(title = "Başarılı!", message = "Para başarıyla yatırıldı!")
        self.bakiye += yatirilacakMiktar

        conn = sqlite3.connect(f"{self.path}/veritabani.db")
        cursor = conn.cursor()
            
        cursor.execute(f"""UPDATE bilgiler SET Bakiye = {self.bakiye} WHERE KartNo = {self.kartNo}""")
        conn.commit()
        conn.close()
        self.windowT.destroy()

Run = BankaSistemiGiriş()