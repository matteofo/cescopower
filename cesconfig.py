import configparser

class Config:
    mac_addr: str
    ip_addr: str
    password: str
    
    def __init__(self, ip, mac, password):
        self.ip_addr = ip
        self.mac_addr = mac
        self.password = password

def load_config() -> Config:
    parser = configparser.ConfigParser()
    parser.read("./cesco.conf")

    if 'cesco' not in parser:
        return None
    
    cesco = parser['cesco']
    
    if 'ip_addr' not in cesco or 'mac_addr' not in cesco:
        return None

    return Config(cesco['ip_addr'], cesco['mac_addr'], cesco['password'])

def write_config(cfg: Config):
    parser = configparser.ConfigParser()

    parser['cesco'] = {}
    parser['cesco']['ip_addr'] = cfg.ip_addr
    parser['cesco']['mac_addr'] = cfg.mac_addr
    parser['cesco']['password'] = load_config().password

    with open("./cesco.conf", 'w') as file:
        parser.write(file)