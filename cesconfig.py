import configparser

class Config:
    mac_addr: str
    ip_addr: str
    
    def __init__(self, ip, mac):
        self.ip_addr = ip
        self.mac_addr = mac

def load_config() -> Config:
    parser = configparser.ConfigParser()
    parser.read("./cesco.conf")

    if 'cesco' not in parser:
        return None
    
    cesco = parser['cesco']
    
    if 'ip_addr' not in cesco or 'mac_addr' not in cesco:
        return None

    return Config(cesco['ip_addr'], cesco['mac_addr'])

def write_config(cfg: Config):
    parser = configparser.ConfigParser()

    parser['cesco'] = {}
    parser['cesco']['ip_addr'] = cfg.ip_addr
    parser['cesco']['mac_addr'] = cfg.mac_addr

    with open("./cesco.conf", 'w') as file:
        parser.write(file)