# main.py

import os
import re
import sys
import shlex
from datetime import datetime
from scanners.nmap_scanner import run_nmap_scan
from scanners.sqlmap_scanner import run_sqlmap_scan
from scanners.nikto_scanner import run_nikto_scan

def safe_input(prompt: str = "") -> str | None:
    try:
        value = input(prompt)
        if value.strip().lower() == 'q':
            print("\nSkanerlash yakunlandi.")
            sys.exit(0)
        return value
    except KeyboardInterrupt:
        print("\n[!] Foydalanuvchi Ctrl-C bosdi. Skanerlash yakunlandi.")
        sys.exit(0)
    except EOFError:
        print("\n[!] Kiritish bekor qilindi (EOF). Skanerlash yakunlandi.")
        sys.exit(0)

def sanitize_filename(text: str) -> str:
    text = re.sub(r'^https?://', '', text)
    text = text.replace('/', '_').replace('-', '_')
    return re.sub(r'[^\w\._]', '_', text)

def save_report(tool_name, target, data):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_path = f"reports/{tool_name}_reports"
    os.makedirs(folder_path, exist_ok=True)
    safe_target = sanitize_filename(target)
    file_path = f"{folder_path}/{safe_target}_{tool_name}_{now}.txt"
    with open(file_path, "w") as f:
        f.write(data)
    print(f"[+] Hisobot saqlandi: {file_path}")

def validate_ports(ports_str: str) -> bool:
    ports = ports_str.split(",")
    for port in ports:
        port = port.strip()
        if not port.isdigit():
            return False
        port_num = int(port)
        if port_num < 1 or port_num > 65535:
            return False
    return True

def nmap_param_menu() -> list[str]:
    while True:
        print("\nNmap parametrini tanlang:")
        print(" 1) Tez xizmat-versiya skani    (-sV -T4 -A -v) [default]")
        print(" 2) TCP SYN (Stealth) skani     (-sS)")
        print(" 3) UDP portlarini tekshirish   (-sU)")
        print(" 4) OS aniqlash + versiya       (-sV -O)")
        print(" 5) Maxsus portlar roʻyxati     (-p <roʻyxat>)")
        print(" 6) Maxsus parametrlar kiritish [advanced]")
        print(" 0) Orqaga")
        print(" q) Skanerlashni yakunlash")
        
        opt = safe_input(" Tanlovingizni kiriting (0-6): ").strip().lower()

        if opt == "1":
            return ["-sV", "-T4", "-A", "-v"]
        elif opt == "2":
            return ["-sS"]
        elif opt == "3":
            return ["-sU"]
        elif opt == "4":
            return ["-sV", "-O"]
        elif opt == "5":
            while True:
                ports = safe_input(" Port(lar)ni vergul bilan ajratgan holda kiriting (masalan 22,80,443): ").strip()
                if validate_ports(ports):
                    return ["-sV", "-p", ports]
                else:
                    print("[!] Portlar noto‘g‘ri kiritildi. Iltimos, faqat 1-65535 oralig‘idagi sonlarni vergul bilan ajratgan holda kiriting.")
        elif opt == "6":
            while True:
                raw = safe_input(" Nmap parametrlarini aynan shunday sintaksisda kiriting: -sV -A -p 22,80\n Parametrlarni kiriting: ")
                try:
                    args = shlex.split(raw)
                    return args
                except ValueError as e:
                    print(f"[!] Sintaksisda xatolik: {e}")
        elif opt == "0":
            run()
        elif opt == "q":
            print("\nSkanerlash yakunlandi.")
            sys.exit()
        else:
            print("[!] Noto‘g‘ri tanlov. Iltimos, faqat 0 dan 6 gacha bo'lgan raqam kiriting.")

def sqlmap_param_menu() -> list[str]:
    while True:
        print("\nSQLMap parametrini tanlang:")
        print(" 1) Tez skan                    (--batch) [default]")
        print(" 2) DB ro‘yxati                 (--dbs)")
        print(" 3) Jadval ro‘yxati             (--tables)")
        print(" 4) Maʼlumotni dump qilish      (--dump)")
        print(" 5) Chuqurlik/xavf darajasi     (--level / --risk)")
        print(" 6) Maxsus parametrlar kiritish [advanced]")
        print(" 0) Orqaga")
        print(" q) Skanerlashni yakunlash")

        opt = safe_input(" Tanlovingizni kiriting (0-6): ").strip()

        if opt == "1":
            return ["--batch"]
        elif opt == "2":
            return ["--batch", "--dbs"]
        elif opt == "3":
            db = safe_input("  Bazani nomini kiriting (masalan users): ").strip()
            return ["--batch", "-D", db, "--tables"]
        elif opt == "4":
            db = safe_input("  Bazani nomini kiriting (masalan users): ").strip()
            tbl = safe_input("  Jadval nomini kiriting (barcha jadvallar kerak bo'lsa bo‘sh qoldiring): ").strip()
            args = ["--batch", "-D", db]
            if tbl:
                args += ["-T", tbl]
            return args + ["--dump"]
        elif opt == "5":
            lvl = safe_input("  Level (1-5): ").strip() or "3"
            risk = safe_input("  Risk  (1-3): ").strip() or "1"
            return ["--batch", f"--level={lvl}", f"--risk={risk}"]
        elif opt == "6":
            while True:
                raw = safe_input(" SQLMap parametrlarini aynan shunday sintaksisda kiriting: --dump --batch --threads=10\n Parametrlarni kiriting: ")
                try:
                    args = shlex.split(raw)
                    return args
                except ValueError as e:
                    print(f"[!] Sintaksisda xatolik: {e}")
        elif opt == "0":
            run()
        elif opt == "q":
            print("\nSkanerlash yakunlandi.")
            sys.exit()
        else:
            print("[!] Noto‘g‘ri tanlov. Iltimos, faqat 0 dan 6 gacha bo'lgan raqam kiriting.")
        
def nikto_param_menu() -> list[str]:
    while True:
        print("\nNikto parametrlarini tanlang:")
        print(" 1) Oddiy skan (-h) [default]")
        print(" 2) Maksimal xavfsizlik (-Tuning, -123b, -Display, v) [to‘liq skan]")
        print(" 3) Muayyan portda skan (-p PORT) [faqat bitta port]")
        print(" 4) Maxsus parametrlar kiritish [advanced]")
        print(" 0) Orqaga")
        print(" q) Skanerlashni yakunlash")

        opt = safe_input(" Tanlovingizni kiriting (0-4): ").strip()

        if opt == "1":
            return []
        elif opt == "2":
            return ["-Tuning", "123b", "-Display", "v"]  
        elif opt == "3":
            while True:
                port = safe_input(" Portni kiriting: ").strip()
                if port.isdigit():
                    port_num = int(port)
                    if 0 < port_num < 65536:
                        return ["-p", port]
                    else:
                        print("[!] Port noto‘g‘ri: Iltimos, faqat 1-65535 oralig‘idagi son kiriting.")
                else:
                    print("[!] Port noto‘g‘ri: Iltimos, faqat 1-65535 oralig‘idagi son kiriting.")
        elif opt == "4":
            while True:
                raw = safe_input(" Nikto parametrlarini aynan shunday sintaksisda kiriting: -p 443 -ssl -Tuning 123\n Parametrlarni kiriting: ")
                try:
                    args = shlex.split(raw)
                    return args
                except ValueError as e:
                    print(f"[!] Sintaksisda xatolik: {e}")
        elif opt == "0":
            run()
        elif opt == "q":
            print("\nSkanerlash yakunlandi.")
            sys.exit()
        else:
            print("[!] Noto‘g‘ri tanlov. Iltimos, faqat 0 dan 4 gacha bo'lgan raqam kiriting.")

def run():
    while True:
        print("\nSkanerlash vositasini tanlang:")
        print("1. Nmap")
        print("2. SQLMap")
        print("3. Nikto")
        print("q. Skanerlashni yakunlash")

        choice = safe_input("Tanlovingizni kiriting (1-3): ").strip().lower()

        if choice not in ['q', '1', '2', '3']:
            print("[!] Noto‘g‘ri tanlov. Iltimos, faqat 1 dan 3 gacha bo'lgan raqam kiriting.")
        
        elif choice == "q":
            print("\nSkanerlash yakunlandi.")
            sys.exit()
        elif choice == "1":
            extra = nmap_param_menu()
            if extra == []:
                return
            target = safe_input("\n Skaner qilinadigan IP/domen/subnet ni kiriting: ").strip()
            result = run_nmap_scan(target, extra)
            save_report("nmap", target, result)
            print("\n📄 Nmap skaner natijasi:\n", result)
            return

        elif choice == "2":
            extra = sqlmap_param_menu()
            if extra == []:
                return
            target = safe_input("\n Skaner qilinadigan URL manzilni kiriting (masalan, http://testphp.vulnweb.com/artists.php?artist=1): ").strip()
            result = run_sqlmap_scan(target, extra)
            save_report("sqlmap", target, result)
            print("\n📄 SQLMap skaner natijasi:\n", result)
            return

        elif choice == "3":
            extra = nikto_param_menu()
            if extra is None:
                return
            target = safe_input("\n Skaner qilinadigan URL manzilini kiriting (https:// bilan): ").strip()
            result = run_nikto_scan(target, extra)
            save_report("nikto", target, result)
            print("\n📄 Nikto skaner natijasi:\n")
            print(result)
            return

def main():
    while True:
        run()
        again = safe_input("\nYana skanerlashni xohlaysizmi? Davom etish (D) / Skanerlashni yakunlash (Q): ").strip().lower()
        if again != 'd':
            print("\nSkanerlash yakunlandi.")
            break
        print("\n-----------------------------------\n")

if __name__ == "__main__":
    main()
