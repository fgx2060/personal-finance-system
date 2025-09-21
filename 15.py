import tkinter as tk
from tkinter import ttk, messagebox, font, simpledialog
from tkinter import scrolledtext
import json
from datetime import datetime
import os
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rc("font", family="Microsoft JhengHei", size=12)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class LoginWindow:
    def __init__(self):
        # 創建主視窗
        self.root = tk.Tk()
        self.root.title("使用者登入")
        self.logged_in = False  # 新增 logged_in 屬性，初始值為 False

        # 設定視窗的尺寸和位置
        window_width = self.root.winfo_screenwidth()
        window_height = self.root.winfo_screenheight()
        width = 450
        height = 300
        left = int((window_width - width) / 2)
        top = int((window_height - height) / 2)
        self.root.geometry(f"{width}x{height}+{left}+{top}")
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=10)
        # 創建使用者名稱標籤和輸入框
        username_label = tk.Label(self.root, text="使用者名稱:")
        username_label.pack(pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=10)

        # 創建密碼標籤和輸入框
        password_label = tk.Label(self.root, text="密碼:")
        password_label.pack(pady=10)
        self.password_entry = tk.Entry(self.root, show="*")  # 用星號(*)顯示密碼
        self.password_entry.pack(pady=10)

        # 創建登入按鈕
        login_button = tk.Button(
            self.root, text="登入", command=self.on_login_button_click
        )
        login_button.pack(pady=20)

    def check_login(self, username, password):
        # 在這裡添加實際的使用者驗證邏輯
        # 這裡只是一個簡單的示例
        if username == "user" and password == "password":
            return True
        else:
            return False

    def on_login_button_click(self):
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        if self.check_login(entered_username, entered_password):
            messagebox.showinfo("登入成功", "歡迎回來，{}".format(entered_username))
            self.logged_in = True  # 設定 logged_in 為 True
            self.close_login_window()
        else:
            messagebox.showerror("登入失敗", "使用者名稱或密碼錯誤")

    def close_login_window(self):
        # 關閉登入畫面
        self.root.destroy()

    def open_main_window(self):
        # 只有在"登入成功時"才開啟主視窗
        if self.logged_in:
            root = tk.Tk()
            money_app = Money(root)
            root.mainloop()

    def run(self):
        # 啟動主迴圈
        self.root.mainloop()


class Money:
    def __init__(self, root):
        self.root = root
        self.root.title("個人財務管理系統-第10組")
        self.資料 = self.載入資料()

        # 設定視窗的尺寸和位置
        window_width = self.root.winfo_screenwidth()
        window_height = self.root.winfo_screenheight()
        width = 850
        height = 600
        left = int((window_width - width) / 2)
        top = int((window_height - height) / 2)
        self.root.geometry(f"{width}x{height}+{left}+{top}")
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=10)
        # # 設定視窗背景色
        # self.root.configure(background="#F0F0F0")
        self.支出分類 = [
            "早餐",
            "午餐",
            "晚餐",
            "消夜",
            "飲品",
            "點心",
            "購物",
            "娛樂",
            "交通",
            "日用品",
            "醫療",
            "數位",
            "醫美",
            "房租",
            "水果",
            "社交",
            "禮物",
        ]
        self.收入分類 = ["薪資", "獎金", "投資"]
        self.自訂分類 = []
        self.建立目標區域()
        self.建立記錄區域()
        self.建立報表與分析區域()

    def 建立目標區域(self):
        目標框架 = ttk.Frame(self.root)
        目標框架.pack(pady=10)

        ttk.Label(目標框架, text="每月儲蓄目標：").grid(row=0, column=0)
        self.目標輸入 = ttk.Entry(目標框架)
        self.目標輸入.grid(row=0, column=1)
        ttk.Button(目標框架, text="設定目標", command=self.設定目標).grid(row=0, column=2)

    def 建立記錄區域(self):
        記錄框架 = ttk.Frame(self.root)
        記錄框架.pack(pady=10, anchor="center")

        ttk.Label(記錄框架, text="類別：").grid(row=0, column=0)
        self.類別輸入 = ttk.Combobox(記錄框架, values=["收入", "支出"], state="readonly")
        self.類別輸入.bind("<<ComboboxSelected>>", self.更新分類選項)
        self.類別輸入.grid(row=0, column=1)
        self.類別輸入.set("")  # 設定初始值為空字串

        ttk.Label(記錄框架, text="分類：").grid(row=0, column=2)
        self.分類輸入 = ttk.Combobox(記錄框架, values=[], state="readonly")
        self.分類輸入.grid(row=0, column=3)
        # 新增分類按鈕
        ttk.Button(記錄框架, text="新增分類", command=self.新增分類).grid(row=0, column=7)

        ttk.Label(記錄框架, text="金額：").grid(row=0, column=4)
        self.金額輸入 = ttk.Entry(記錄框架)
        self.金額輸入.grid(row=0, column=5)
        ttk.Button(記錄框架, text="記錄交易", command=self.記錄交易).grid(row=0, column=6)

        # 記錄列表框
        ttk.Label(記錄框架, text="我的記錄：").grid(row=1, column=1)
        self.記錄列表框 = tk.Listbox(記錄框架, width=50, height=10)
        self.記錄列表框.grid(row=2, column=0, columnspan=8)

    def 建立報表與分析區域(self):
        # 按鈕排列方式改為水平排列
        按鈕框架 = ttk.Frame(self.root)
        按鈕框架.pack(pady=10)

        ttk.Button(按鈕框架, text="生成報表", command=self.生成報表).pack(side=tk.LEFT, padx=10)
        ttk.Button(按鈕框架, text="收入圖表", command=self.生成收入圓餅圖).pack(side=tk.LEFT, padx=10)
        ttk.Button(按鈕框架, text="支出圖表", command=self.生成支出圓餅圖).pack(side=tk.LEFT, padx=10)

    def 載入資料(self):
        if os.path.exists("expense_data.json"):
            with open("expense_data.json", "r") as file:
                資料 = json.load(file)
        else:
            資料 = {"目標": {}, "記錄": []}

        return 資料

    def 儲存資料(self):
        with open("expense_data.json", "w") as file:
            json.dump(self.資料, file)
        messagebox.showinfo("儲存成功", "資料已成功儲存！")

    def 設定目標(self):
        目標金額 = self.目標輸入.get()
        # 檢查目標金額是否為數字
        if not 目標金額.isdigit():
            messagebox.showerror("錯誤", "請輸入有效的數字作為目標金額。")
            return
        # 轉換目標金額為整數
        目標金額 = int(目標金額)
        self.資料["目標"]["每月儲蓄"] = 目標金額
        messagebox.showinfo("目標設定成功", f"已設定每月儲蓄目標為 {目標金額} 元")

    def 記錄交易(self):
        金額輸入值 = self.金額輸入.get()
        # 檢查金額輸入是否為數字
        if not 金額輸入值.isdigit():
            messagebox.showerror("錯誤", "請輸入有效的數字作為金額。")
            return
        金額 = int(金額輸入值)

        類別 = self.類別輸入.get()
        分類 = self.分類輸入.get()

        記錄時間 = datetime.now().strftime("%Y-%m-%d")
        記錄 = {"時間": 記錄時間, "類別": 類別, "分類": 分類, "金額": 金額}
        self.資料["記錄"].append(記錄)
        self.更新記錄列表框()
        messagebox.showinfo(
            "記錄成功", f"已記錄收入支出：\n時間: {記錄時間}\n類別: {類別}, 分類: {分類}, 金額: {金額} 元"
        )

    def 更新記錄列表框(self):
        self.記錄列表框.delete(0, tk.END)
        for 記錄 in self.資料["記錄"]:
            記錄字串 = f"{記錄['時間']}, {記錄['類別']}, {記錄['分類']}, {記錄['金額']} 元"
            self.記錄列表框.insert(tk.END, 記錄字串)

    def 生成報表(self):
        總收入 = sum(int(記錄["金額"]) for 記錄 in self.資料["記錄"] if 記錄["類別"] == "收入")
        總支出 = sum(int(記錄["金額"]) for 記錄 in self.資料["記錄"] if 記錄["類別"] == "支出")
        每月儲蓄目標 = int(self.資料["目標"].get("每月儲蓄", 0))

        支出資訊列表 = [
            {"項目": 記錄["分類"], "金額": int(記錄["金額"]), "時間": 記錄["時間"]}
            for 記錄 in self.資料["記錄"]
            if 記錄["類別"] == "支出"
        ]
        前兩大支出 = sorted(支出資訊列表, key=lambda x: x["金額"], reverse=True)[:2]

        報表 = f"每月報表：\n總收入: {總收入} 元\n總支出: {總支出} 元\n"

        if 每月儲蓄目標 > 0:  # 如果有輸入每月儲蓄目標
            # 達成目標
            if 總收入 - 總支出 >= 每月儲蓄目標:
                報表 += "你好棒! 已達成每月儲蓄目標！\n"
                目標金額 = 每月儲蓄目標
                報表 += f"目標: {目標金額} 元，剩餘: {總收入 - 總支出} 元\n\n"
                if 前兩大支出:
                    報表 += "以下是相對較多的支出項：\n"
                    for 支出 in 前兩大支出:
                        報表 += f" {支出['項目']}, 金額: {支出['金額']} 元\n"
            # 未達成目標
            elif 總收入 - 總支出 < 每月儲蓄目標:
                報表 += "未達成每月儲蓄目標\n"
                目標金額 = 每月儲蓄目標
                差額 = max(目標金額 - (總收入 - 總支出), 0)
                報表 += f"目標: {目標金額} 元，剩餘: {總收入 - 總支出} 元\n距離目標相差: {差額} 元\n\n"
                if 前兩大支出:
                    報表 += "建議減少以下支出：\n"
                    for 支出 in 前兩大支出:
                        報表 += f" {支出['項目']}, 金額: {支出['金額']} 元\n"
        else:
            報表 += ""

        messagebox.showinfo("每月報表", 報表)

    def 生成收入圓餅圖(self):
        # 取得收入圓餅圖資料
        收入數據 = {"薪資": 0, "獎金": 0, "投資": 0}
        for 記錄 in self.資料["記錄"]:
            if 記錄["類別"] == "收入":
                收入項目 = 記錄["分類"]
                金額 = int(記錄["金額"])
                if 收入項目 in 收入數據:
                    收入數據[收入項目] += 金額
                else:
                    # 新增分類時，更新收入數據
                    收入數據[收入項目] = 金額

        # 檢查是否有收入，若無則顯示提示訊息
        if not any(收入數據.values()):
            messagebox.showinfo("提示", "收入為0，無法生成圓餅圖。")
            return

        # 檢查收入類別是否為0，若是則從字典中移除
        if 收入數據["薪資"] == 0:
            del 收入數據["薪資"]
        if 收入數據["獎金"] == 0:
            del 收入數據["獎金"]
        if 收入數據["投資"] == 0:
            del 收入數據["投資"]

        # 繪製收入圓餅圖
        標籤 = list(收入數據.keys())
        值 = list(收入數據.values())

        fig, ax = plt.subplots()
        labels = [f"{category} ({amount}元)" for category, amount in 收入數據.items()]
        ax.pie(收入數據.values(), labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        ax.set_title("收入分析圓餅圖")

        # 在tkinter視窗中顯示收入圓餅圖
        圓餅圖框架 = ttk.Frame(self.root, name="圓餅圖框架")
        圓餅圖框架.pack(side=tk.LEFT, padx=10, pady=10)
        繪圖區 = FigureCanvasTkAgg(fig, master=圓餅圖框架)
        繪圖區.draw()
        繪圖區.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def 生成支出圓餅圖(self):
        # 取得支出項目圓餅圖資料
        支出項目數據 = {}
        for 記錄 in self.資料["記錄"]:
            if 記錄["類別"] == "支出":
                支出項目 = 記錄["分類"]
                金額 = int(記錄["金額"])
                if 支出項目 in 支出項目數據:
                    支出項目數據[支出項目] += 金額
                else:
                    支出項目數據[支出項目] = 金額

        # 檢查是否有支出，若無則顯示提示訊息
        if not any(支出項目數據.values()):
            messagebox.showinfo("提示", "支出為0，無法生成圓餅圖。")
            return

        # 繪製支出項目圓餅圖
        fig, ax = plt.subplots()
        labels = [f"{category} ({amount}元)" for category, amount in 支出項目數據.items()]
        ax.pie(支出項目數據.values(), labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        ax.set_title("支出分析圓餅圖")

        # 在tkinter視窗中顯示支出項目圓餅圖
        圓餅圖框架 = ttk.Frame(self.root, name="圓餅圖框架")
        圓餅圖框架.pack(side=tk.RIGHT, padx=10, pady=10)
        繪圖區 = FigureCanvasTkAgg(fig, master=圓餅圖框架)
        繪圖區.draw()
        繪圖區.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def 清除圓餅圖(self):
        # 清除先前的圓餅圖
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Frame) and "圓餅圖" in str(widget):
                widget.destroy()

    def 新增分類(self):
        # 獲取使用者輸入的自訂分類
        自訂分類 = simpledialog.askstring("新增分類", "請輸入自訂分類：")

        # 檢查使用者是否按下取消或未輸入內容
        if 自訂分類 is None or 自訂分類.strip() == "":
            return

        選擇類別 = self.類別輸入.get()

        # 將新增的分類加入到對應的分類列表
        if 選擇類別 == "支出":
            self.支出分類.append(自訂分類)
        elif 選擇類別 == "收入":
            self.收入分類.append(自訂分類)

        # 更新分類選項
        self.更新分類選項()
        self.分類輸入.set(自訂分類)

        # 清除並重新生成收入圓餅圖
        # self.清除圓餅圖()
        # self.生成收入圓餅圖()

    def 更新分類選項(self, event=None):
        選擇類別 = self.類別輸入.get()

        if 選擇類別 == "支出":
            支出分類 = [
                "早餐",
                "午餐",
                "晚餐",
                "消夜",
                "飲品",
                "點心",
                "購物",
                "娛樂",
                "交通",
                "日用品",
                "醫療",
                "數位",
                "醫美",
                "房租",
                "水果",
                "社交",
                "禮物",
            ]
            self.分類輸入["values"] = 支出分類 + self.自訂分類輸入()
        elif 選擇類別 == "收入":
            收入分類 = ["薪資", "獎金", "投資"]
            self.分類輸入["values"] = 收入分類 + self.自訂分類輸入()
        else:
            self.分類輸入["values"] = []

    def 自訂分類輸入(self):
        return []


if __name__ == "__main__":
    # 創建應用實例並運行
    login_window = LoginWindow()
    login_window.run()

    # 在登入成功後才創建主程式
    if login_window.logged_in:
        root = tk.Tk()
        app = Money(root)
        root.mainloop()
