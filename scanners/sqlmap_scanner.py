# scanners/sqlmap_scanner.py

import subprocess
from typing import List, Optional

def run_sqlmap_scan(target: str, extra_args: Optional[List[str]] = None) -> str:
    if extra_args is None:
        extra_args = ["--batch"]

    cmd = ["sqlmap", "-u", target] + extra_args

    try:
        print(f"[+] SQLMap skaneri ishga tushirildi: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            tips = generate_sqlmap_recommendations(result.stdout)
            return f"{result.stdout}\n\n{tips}"
        else:
            return f"[!] SQLMap bajarilmadi:\n{result.stderr}"
    except FileNotFoundError:
        return "[!] SQLMap dasturi topilmadi. Iltimos, uni o‘rnatganingizni tekshiring."
    except subprocess.CalledProcessError as e:
        return f"[!] SQLMap xatolik: {e.output}"
    except Exception as e:
        return f"[!] SQLMap bajarishda istisno yuz berdi: {str(e)}"

def generate_sqlmap_recommendations(output: str) -> list[str]:
    tips = ["\n[🔐 Tavsiyalar]"]

    if "parameter" in output and "is vulnerable" in output:
        tips.append("- SQL Injection aniqlandi: Parametrlar foydalanuvchi kiritmalariga filtrlanmasdan yuborilmoqda. Prepared statements yoki ORM ishlatish zarur.")

    if "current user: '" in output:
        tips.append("- SQLi orqali foydalanuvchi aniqlandi: Bu zaiflik orqali tizimdagi user'ga oid ma'lumotlar olingan. Kirishni cheklang, minimal huquqli userlardan foydalaning.")

    if "current database: '" in output:
        tips.append("- SQLi orqali ma'lumotlar bazasi aniqlandi: Hujumchi asosiy bazani aniqlay olmoqda. Application user huquqlarini minimallashtiring.")

    if "available databases" in output:
        tips.append("- SQLi orqali barcha bazalar ko‘rinmoqda: Bu juda xavfli. Web app database foydalanuvchisi faqat 1ta ma'lumotlar bazasiga kirish huquqiga ega bo‘lishi kerak.")

    if "has database management system" in output:
        tips.append("- SQLi orqali DBMS turi aniqlandi: Hujumchi DBMS zaifliklarini nishonga olishi mumkin. WAF va input validationni kuchaytiring.")

    if "file read" in output:
        tips.append("- SQLi orqali fayl o‘qish mumkin: LOCAL_INFILE yoki xp_cmdshell kabi xavfli funksiyalarni o‘chiring.")

    if "password hashes" in output:
        tips.append("- SQLi orqali foydalanuvchi parollari yoki xeshlar topildi: Parollarni shifrlang (bcrypt, Argon2) va maxfiylik siyosatini yangilang.")

    if "writes to the filesystem" in output:
        tips.append("- SQLi orqali fayl yozish mumkin: Bu RCE’ga olib kelishi mumkin. Fayl tizimga yozishni cheklash, AppArmor/SELinuxdan foydalanish zarur.")

    if "access file system" in output:
        tips.append("- Fayl tizimiga kirish imkoni bor: SQLi orqali local fayllarni o‘qish yoki yozish mumkin. Fayl tizim huquqlarini tekshiring.")

    if "command execution" in output:
        tips.append("- SQLi orqali buyruq bajarish (RCE) mumkin: Bu tizim xavfsizligi uchun katta tahdid. Web server va DB ni alohida joylashtirish zarur.")

    if not tips or len(tips) == 1:
        tips.append("- Hech qanday aniq xavfsizlik tavsiyasi aniqlanmadi.")

    return "\n".join(tips)
