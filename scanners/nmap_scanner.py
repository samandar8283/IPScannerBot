# scanners/nmap_scanner.py
    
import subprocess
from typing import List, Optional

def run_nmap_scan(target: str, extra_args: Optional[List[str]] = None) -> str:
    if extra_args is None:
        extra_args = ["-sV", "-T4", "-A", "-v"]

    cmd = ["nmap", *extra_args, target]

    try:
        print(f"[+] Nmap skaneri ishga tushirildi: {' '.join(cmd)}")
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return output
    except FileNotFoundError:
        return "[Xatolik] Nmap dasturi topilmadi. Iltimos, uni o‘rnatganingizni tekshiring."
    except subprocess.CalledProcessError as e:
        return f"[!] Nmap xatolik: {e.output}"
    except Exception as e:
        return f"[Xatolik] Nmap bajarishda istisno yuz berdi: {str(e)}"