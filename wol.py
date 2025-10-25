from cesconfig import Config
import subprocess, requests

def get_powerstatus(cfg: Config):
    proc = subprocess.Popen(
        ["ping", "-c", "1", "-i", "0.2", cfg.ip_addr],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        text=True,
    )

    try:
        # Wait for the process to finish or `timeout` is reached
        proc.wait(timeout=0.5)
    except subprocess.TimeoutExpired:
        # End the process with `SIGTERM` signal
        proc.kill()

    return proc.returncode == 0

def wake_wol(cfg: Config):
    proc = subprocess.Popen(
        ["wakeonlan", "-i", cfg.ip_addr, cfg.mac_addr],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        text=True,
    )

    proc.communicate()
    return proc.returncode

def wake_satellite(cfg: Config):
    try:
        r = requests.get("http://" + cfg.ip_addr + "/power")
        return r.status_code
    except:
        return 0

def wake_auto(cfg: Config):
    if cfg.satellite:
        return wake_satellite(cfg) == 200
    else:
        return wake_wol(cfg) == 0