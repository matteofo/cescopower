import configparser

class Config:
    mac_addr: str
    ip_addr: str
    password: str
    satellite: bool
    
    def __init__(self, ip, mac, password, satellite):
        self.ip_addr = ip
        self.mac_addr = mac
        self.password = password
        self.satellite = satellite

def load_config() -> Config:
    parser = configparser.ConfigParser()
    parser.read("./cesco.conf")

    if 'cesco' not in parser:
        return None
    
    cesco = parser['cesco']
    
    if 'ip_addr' not in cesco or 'mac_addr' not in cesco:
        return None

    if not 'satellite' in cesco:
        sat = False
    else:
        sat = True if cesco['satellite'] == "True" else False

    return Config(cesco['ip_addr'], cesco['mac_addr'], cesco['password'], sat)

def write_config(cfg: Config):
    parser = configparser.ConfigParser()

    parser['cesco'] = {}
    parser['cesco']['ip_addr'] = cfg.ip_addr
    parser['cesco']['mac_addr'] = cfg.mac_addr
    parser['cesco']['password'] = load_config().password
    parser['cesco']['satellite'] = str(cfg.satellite)

    with open("./cesco.conf", 'w') as file:
        parser.write(file)