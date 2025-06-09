# scanner/sqlmap_scanner.py

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
            return result.stdout
        else:
            return f"[!] SQLMap bajarilmadi:\n{result.stderr}"
    except FileNotFoundError:
        return "[!] SQLMap dasturi topilmadi. Iltimos, uni o‘rnatganingizni tekshiring."
    except subprocess.CalledProcessError as e:
        return f"[!] SQLMap xatolik: {e.output}"
    except Exception as e:
        return f"[!] SQLMap bajarishda istisno yuz berdi: {str(e)}"