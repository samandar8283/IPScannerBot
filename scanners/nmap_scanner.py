# scanners/nmap_scanner.py

import re
import subprocess
from typing import List, Optional

def run_nmap_scan(target: str, extra_args: Optional[List[str]] = None) -> str:
    if extra_args is None:
        extra_args = ["-sV", "-T4", "-A", "-v"]

    cmd = ["nmap", *extra_args, target]

    try:
        print(f"[+] Nmap skaneri ishga tushirildi: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            tips = generate_nmap_recommendations(result.stdout)
            return f"{result.stdout}\n\n{tips}"
        else:
            return f"[!] Nmap bajarilmadi:\n{result.stderr}"
    except FileNotFoundError:
        return "[Xatolik] Nmap dasturi topilmadi. Iltimos, uni o‘rnatganingizni tekshiring."
    except subprocess.CalledProcessError as e:
        return f"[!] Nmap xatolik: {e.output}"
    except Exception as e:
        return f"[Xatolik] Nmap bajarishda istisno yuz berdi: {str(e)}"

def generate_nmap_recommendations(output: str) -> str:
    tips = ["\n[🔐 Tavsiyalar]"]

    if re.search(r"21/tcp\s+open", output):
        tips.append("- FTP ochiq: SSL yo‘qligini tekshiring. FTP o‘rniga SFTP yoki FTPS ishlatish tavsiya etiladi.")

    if re.search(r"22/tcp\s+open", output):
        tips.append("- SSH porti ochiq: ruxsat etilgan IP-larni cheklang, root bilan ulanishni o‘chiring, Fail2ban o‘rnating.")

    if re.search(r"23/tcp\s+open", output):
        tips.append("- Telnet porti ochiq: Juda zaif xizmat. Telnetni o‘chiring, o‘rniga SSH’dan foydalaning.")

    if re.search(r"25/tcp\s+open", output):
        tips.append("- SMTP porti ochiq: SPAM relayni tekshiring. TLS yo‘qligi xavf tug‘diradi.")

    if re.search(r"53/tcp\s+open", output) or re.search(r"53/udp\s+open", output):
        tips.append("- DNS porti (53) ochiq: DNS server bo‘lmasa yopilsin. DNS amplification hujumlari xavfi mavjud.")

    if re.search(r"80/tcp\s+open", output):
        tips.append("- HTTP porti ochiq, ammo HTTPS yo‘q: TLS yo‘qligi xavfli. HTTPS’ga o‘ting.")

    if re.search(r"110/tcp\s+open", output):
        tips.append("- POP3 porti ochiq: TLS yo‘qligi xavfli. POP3S (SSL bilan) ishlatish tavsiya etiladi.")

    if re.search(r"139/tcp\s+open", output) or re.search(r"445/tcp\s+open", output):
        tips.append("- SMB portlari ochiq: faqat lokal tarmoqda ishlatilishi kerak. Internetga ochiq bo‘lsa xavfli.")

    if re.search(r"143/tcp\s+open", output):
        tips.append("- IMAP porti ochiq: TLS yo‘qligi xavfli. IMAPS (SSL bilan) ishlatish kerak.")
    
    if re.search(r"443/tcp\s+open", output):
        tips.append("- HTTP'dan HTTPS'ga avtomatik yo‘naltirishni yoqing, faqat kerakli metodlarga ruxsat bering.")

    if re.search(r"445/tcp\s+open", output):
        tips.append("- SMB porti ochiq: WannaCry kabi hujumlarga yo‘l ochilishi mumkin. Agar kerak bo‘lmasa, o‘chiring.")
    
    if re.search(r"3306/tcp\s+open", output):
        tips.append("- MySQL ochiq: default foydalanuvchilarni olib tashlang va kuchli parollar o‘rnating.")

    if re.search(r"3389/tcp\s+open", output):
        tips.append("- RDP porti ochiq: Internetga ochiq bo‘lsa xavfli. MFA va IP filtering ishlatilsin.")

    if re.search(r"5900/tcp\s+open", output):
        tips.append("- VNC porti ochiq: TLS yo‘qligi xavfli. Kuchli parollarni o‘rnatish zarur.")

    if re.search(r"8080/tcp\s+open", output) and not re.search(r"8443/tcp\s+open", output) and not re.search(r"443/tcp open", output):
        tips.append("- Web server (8080) ochiq, ammo HTTPS yo‘q: HTTP xavfsiz emas. HTTPSga o‘tkazing.")

    if "No exact OS matches" in output:
        tips.append("- OS aniqlanmadi: hostni ping orqali yopgan bo‘lishi mumkin yoki firewall bor.")
    
    if "Too many fingerprints match this host" in output:
        tips.append("- Juda ko‘p fingerprintlar mos kelmoqda: tizimda chalkashlik bor. Versiyalarni tekshiring.")
    
    if "open" not in output:
        tips.append("- Ochiq portlar aniqlanmadi. Ehtimol, barcha portlar yopiq yoki host offline.")
    
    if len(tips) == 1:
        tips.append("- Ochiq portlar topildi, lekin xavfsizlikka oid muhim tavsiyalar aniqlanmadi.")
    
    return "\n".join(tips)
