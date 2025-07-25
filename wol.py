from cesconfig import Config
import subprocess

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

def try_wake(cfg: Config):
    proc = subprocess.Popen(
        ["wakeonlan", "-i", cfg.ip_addr, cfg.mac_addr],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        text=True,
    )

    proc.communicate()
    return proc.returncode