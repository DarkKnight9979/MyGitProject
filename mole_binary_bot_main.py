
import tkinter as tk
from tkinter import ttk
import threading
from iqoptionapi.stable_api import IQ_Option
import time

# إعداد الاتصال بمنصة IQ Option
class IQBot:
    def __init__(self, email, password):
        self.IQ = IQ_Option(email, password)
        self.IQ.connect()
        while not self.IQ.check_connect():
            print("فشل الاتصال. إعادة المحاولة...")
            self.IQ.connect()
        print("تم الاتصال بنجاح")

    def start_trade(self, asset, direction, amount, duration):
        check, id = self.IQ.buy(amount, asset, direction, duration)
        if check:
            print(f"تم فتح صفقة {direction.upper()} على {asset} لمدة {duration} دقيقة")
        else:
            print("فشل في فتح الصفقة")

# واجهة المستخدم
class MoLeBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MoLe Binary Bot")
        self.root.geometry("700x400")
        self.root.configure(bg="#e0f8e0")

        title = tk.Label(root, text="MoLe Binary Bot", font=("Helvetica", 20, "bold"), bg="#e0f8e0", fg="green")
        title.pack(pady=10)

        # اختيار الاستراتيجية
        self.strategy_label = tk.Label(root, text="قائمة الاستراتيجيات:", bg="#e0f8e0")
        self.strategy_label.pack()
        self.strategy_combo = ttk.Combobox(root, values=["1", "2", "3", "4", "5"])
        self.strategy_combo.pack()

        # اختيار العملة
        self.asset_label = tk.Label(root, text="قائمة العملات:", bg="#e0f8e0")
        self.asset_label.pack()
        self.asset_combo = ttk.Combobox(root, values=["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCHF"])
        self.asset_combo.pack()

        # مدة الصفقة
        self.duration_label = tk.Label(root, text="مدة الصفقة (دقيقة):", bg="#e0f8e0")
        self.duration_label.pack()
        self.duration_combo = ttk.Combobox(root, values=["1", "5", "10", "15"])
        self.duration_combo.pack()

        # خيار المارتينجال
        self.martingale_var = tk.IntVar()
        self.martingale_check = tk.Checkbutton(root, text="تفعيل المارتينجال", variable=self.martingale_var, bg="#e0f8e0")
        self.martingale_check.pack()

        self.martingale_entry = tk.Entry(root)
        self.martingale_entry.insert(0, "2.0")
        self.martingale_entry.pack()

        # زر التشغيل
        self.start_button = tk.Button(root, text="تشغيل البوت", bg="green", fg="white", command=self.start_bot)
        self.start_button.pack(pady=10)

        # خانة الإيميل والباسورد للاتصال
        self.email_entry = tk.Entry(root)
        self.email_entry.insert(0, "البريد الإلكتروني")
        self.email_entry.pack()

        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.insert(0, "كلمة المرور")
        self.password_entry.pack()

    def start_bot(self):
        threading.Thread(target=self.run_bot).start()

    def run_bot(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        bot = IQBot(email, password)

        asset = self.asset_combo.get()
        duration = int(self.duration_combo.get())
        direction = "call"  # ثابتة الآن، ويمكنك ربطها بتحليل لاحق
        amount = 1

        if self.martingale_var.get():
            try:
                multiplier = float(self.martingale_entry.get())
                print(f"مارتينجال مفعل بنسبة {multiplier}")
            except:
                print("قيمة المارتينجال غير صحيحة")

        strategy = self.strategy_combo.get()
        print(f"تشغيل البوت باستخدام الاستراتيجية رقم {strategy}")
        bot.start_trade(asset, direction, amount, duration)

if __name__ == "__main__":
    root = tk.Tk()
    app = MoLeBotGUI(root)
    root.mainloop()
