# scanners/nikto_scanner.py

import subprocess
from typing import List, Optional

def run_nikto_scan(target: str, extra_args: Optional[List[str]] = None) -> str:
    if extra_args is None:
        extra_args = []

    cmd = ["nikto", "-h", target] + extra_args

    try:
        print(f"[+] Nikto skaneri ishga tushirildi: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            tips = generate_nikto_recommendations(result.stdout)
            return f"{result.stdout}\n\n{tips}"
        else:
            return f"[!] Nikto bajarilmadi:\n{result.stderr}"
    except FileNotFoundError:
        return "[Xatolik] Nikto dasturi topilmadi. Iltimos, uni o‘rnatganingizni tekshiring."
    except subprocess.CalledProcessError as e:
        return f"[!] SQLMap xatolik: {e.output}"
    except Exception as e:
        return f"[Xatolik] Nikto bajarishda istisno yuz berdi: {str(e)}"
    
def generate_nikto_recommendations(output: str) -> str:
    tips = ["\n[🔐 Tavsiyalar]"]

    if "X-Frame-Options header is not present" in output:
        tips.append("- 'X-Frame-Options' yo‘q: Clickjackingdan himoya qilish uchun bu headerni qo‘shing.")

    if "X-XSS-Protection header is not defined" in output:
        tips.append("- 'X-XSS-Protection' yo‘q: brauzerning XSSdan himoya qiluvchi funksiyasi o‘chirib qo‘yilgan.")

    if "X-Content-Type-Options header is not set" in output:
        tips.append("- 'X-Content-Type-Options' yo‘q: MIME tipni aniqlashda brauzerning noto‘g‘ri taxmini xavf tug‘diradi.")

    if "Server:" in output:
        tips.append("- Server banneri aniqlangan: Versiya ma’lumotlarini yashirish xavfsizlikni oshiradi.")

    if "Allowed HTTP Methods" in output:
        tips.append("- HTTP metodlar ro‘yxati ochiq: faqat kerakli metodlarni ruxsat bering (GET, POST).")

    if "OSVDB-" in output:
        tips.append("- Potensial zaifliklar aniqlandi (OSVDB): tafsilotlarni ko‘rib chiqing va yangilashlarni bajaring.")

    if "Cookie without HttpOnly flag" in output:
        tips.append("- Cookie’lar HttpOnly flag’siz: JavaScript orqali o‘g‘irlanish xavfi mavjud.")

    if len(tips) == 1:
        tips.append("- Jiddiy zaifliklar aniqlanmadi.")

    return "\n".join(tips)