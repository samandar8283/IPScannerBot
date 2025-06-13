# 🛡️ Axborot Tizimlaridagi Zaifliklarni Avtomatik Aniqlovchi Bot

## 📌 Loyihaning qisqacha tavsifi

Ushbu loyiha orqali foydalanuvchi tarmoq va veb-ilovalardagi xavfsizlik zaifliklarini aniqlashi mumkin. Bot `Nmap`, `SQLmap` va `Nikto` kabi mashhur skanerlovchi vositalar yordamida ishlaydi. Har bir vosita foydalanuvchi bilan interaktiv tarzda ishlaydi va natijalar tavsiyalar bilan birga saqlanadi.

---

## 🚀 Asosiy funksiyalar

- Nmap orqali port va xizmatlarni skanerlash
- SQLmap orqali SQL zaifliklarini aniqlash
- Nikto orqali veb-server zaifliklarini topish
- Skanerlash natijalarini `.txt` fayl sifatida saqlash
- Tavsiyalarni avtomatik generatsiya qilish
- Xavfsiz input kiritish va tekshiruv

---

## 🧰 Texnologiyalar

- Python 3.x
- Nmap
- SQLmap
- Nikto
- Git, GitHub
- Ubuntu/Linux terminal muhiti

---

## 🛠️ O‘rnatish

```bash
# Repozitoriyani yuklab oling:
git clone https://github.com/samandar8283/IPScannerBot.git

# Loyihaga o‘ting:
cd IPScannerBot

# Skanerlash vositalarini o'rnating:
sudo apt install nmap sqlmap nikto

# Virtual muhit yarating:
python3 -m venv venv
source venv/bin/activate
```

---

## ▶️ Foydalanish

```bash
# Botni ishga tushiring:
python3 main.py

# Terminalda vosita tanlanadi (masalan, Nmap), parametrlar belgilanadi va nishon manzili kiritiladi.
```

---

## 📁 Hisobotlar

Har bir skanerlashdan so‘ng natijalar `reports/` papkasida saqlanadi:

```
reports/<vosita_nomi>_reports/<nishon>_<vosita>_vaqt.txt
```

---

## 👨‍💻 Muallif

**Yusupov Samandarbek** | GitHub: [@samandar8283](https://github.com/samandar8283)

---

## 🌐 Foydali havolalar

- [Nmap GitHub sahifasi](https://github.com/nmap/nmap)
- [SQLmap GitHub sahifasi](https://github.com/sqlmapproject/sqlmap)
- [Nikto GitHub sahifasi](https://github.com/sullo/nikto)

---

---

# 🛡️ Vulnerability Scanner Bot for Information Systems

## 📌 Project Description

This project helps users automatically scan and detect vulnerabilities in networks and web applications. It integrates with powerful tools like `Nmap`, `SQLmap`, and `Nikto`, providing a simple interactive terminal interface.

---

## 🚀 Key Features

- Port and service scanning using Nmap
- SQL vulnerability detection using SQLmap
- Web server scanning using Nikto
- Saving results in `.txt` report files
- Automatic generation of recommendations
- Safe user input and validation

---

## 🧰 Technologies

- Python 3.x
- Nmap
- SQLmap
- Nikto
- Git, GitHub
- Ubuntu/Linux terminal

---

## 🛠️ Installation

```bash
# Clone the repository:
git clone https://github.com/samandar8283/IPScannerBot.git

# Navigate into the project:
cd IPScannerBot

# Install the scanning tools:
sudo apt install nmap sqlmap nikto

# Create a virtual environment:
python3 -m venv venv
source venv/bin/activate
```

---

## ▶️ Usage

```bash
# Run the bot:
python3 main.py

# Select a tool (e.g., Nmap), choose parameters, and input a target.
```

---

## 📁 Reports

After each scan, results will be saved in the following format:

```
reports/<tool_name>_reports/<target>_<tool>_time.txt
```

---

## 👨‍💻 Author

**Yusupov Samandarbek** | GitHub: [@samandar8283](https://github.com/samandar8283)

---

## 🌐 Useful Links

- [Nmap GitHub page](https://github.com/nmap/nmap)
- [SQLmap GitHub page](https://github.com/sqlmapproject/sqlmap)
- [Nikto GitHub page](https://github.com/sullo/nikto)