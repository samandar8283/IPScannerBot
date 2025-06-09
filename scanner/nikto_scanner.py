# scanner/nikto_scanner.py

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
            return result.stdout
        else:
            return f"[Xatolik] Nikto bajarilmadi:\n{result.stderr}"
    except FileNotFoundError:
        return "[Xatolik] Nikto dasturi topilmadi. Iltimos, uni o‘rnatganingizni tekshiring."
    except subprocess.CalledProcessError as e:
        return f"[!] SQLMap xatolik: {e.output}"
    except Exception as e:
        return f"[Xatolik] Nikto bajarishda istisno yuz berdi: {str(e)}"