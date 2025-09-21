# personal-finance-system
程式概念設計與方法 - 個人財務管理系統

## 💰 個人財務管理系統 (Personal Finance System)
用 Python Tkinter 製作的桌面版記帳與月報工具，支援登入驗證、收入/支出記錄、每月儲蓄目標、月報建議，以及 Matplotlib 視覺化（收入/支出圓餅圖）。

## ✨ 功能特色
 - 登入系統：簡易帳密驗證（示範用 user / password），登入成功才可進入主程式
 - 收支記帳：類別（收入/支出）＋分類（可自訂）＋金額
 - 每月儲蓄目標：輸入目標後，月報會提示是否達標與建議
 - 月報與建議：自動彙整本月總收入/支出、差額、與前兩大支出建議
 - 資料持久化：自動讀寫 expense_data.json
 - 圖表分析：收入/支出圓餅圖（Matplotlib 內嵌於 Tkinter 視窗）

## 🗂 專案結構
```
personal-finance-system/
├─ 15.py                # 主程式：登入 + 記帳 + 報表 + 視覺化
├─ expense_data.json    # 程式運行後自動產生/更新的資料檔
└─ README.md
```

## 🛠 環境需求
 - Python 3.10+（建議）
 - 內建：tkinter（隨大多數 Python 一起提供）
 - 額外套件：
     - matplotlib
     
 - requirements.txt :
```
matplotlib==3.9.2
numpy==1.26.4
```
## 🚀 執行方式
```
python 15.py
```
登入示範帳密
```
- Username：user
- Password：password
```
登入成功後會開啟主視窗，提供以下操作：

1. 設定每月儲蓄目標：輸入數字後按「設定目標」
2. 記錄交易：
      - 類別：收入 / 支出
      - 分類：既有清單（如：早餐/午餐/房租/薪資…）或按「新增分類」
      - 金額：正整數
3. 查看記錄：下方清單「我的記錄」
4. 生成報表：彙整本月總收入/支出、是否達標、與建議
5. 收入/支出圖表：產生圓餅圖（Tkinter 視窗內嵌顯示）

## 🧠 使用說明
- 新增分類：先選「類別（收入/支出）」→ 按「新增分類」→ 輸入名稱，即可加入該類別的下拉選單
- 資料儲存：所有記錄與目標都會寫入 expense_data.json
- 月報建議：
    - 達標時：顯示恭喜與前兩大支出（供檢視）
    - 未達標時：顯示差額與建議減少的前兩大支出

## 🧩 常見問題（FAQ）
- 執行時找不到 Tkinter？

Windows/Mac 官方 Python 通常已內建；若是 Linux，請安裝對應的 tk 套件（如 sudo apt-get install python3-tk）。

- 中文顯示亂碼或方塊？

將 matplotlib.rc("font", family="Microsoft JhengHei", size=12) 改為系統可用字型，或移除 font 設定。

- 資料檔格式：expense_data.json
  ```
  { "目標": { "每月儲蓄": 20000 }, "記錄": [ { "時間": "2025-09-22", "類別": "支出", "分類": "午餐", "金額": 120 } ] }
  ```
  
