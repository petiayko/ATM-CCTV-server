import subprocess
import platform


def check_ping(hostname):
    try:
        subprocess.check_output(f'ping -{"n" if platform.system().lower() == "windows" else "c"} 1 {hostname}',
                                shell=True)
    except Exception:
        return False
    return True
