from flask import *
from wol import *
import cesconfig, json, dom

app = Flask(__name__)

@app.route("/")
def root():
    config = cesconfig.load_config()
    status = get_powerstatus(config)

    meta = dom.refresh(5, "./")

    return render_template("index.html", meta=meta.html(), status=status)

@app.route("/wake")
def wake():
    config = cesconfig.load_config()

    meta = dom.refresh(3, "./")

    wake = try_wake(config)
    notif = dom.notification("WOL inviato!", "Nessun errore.")

    if wake != 0:
        notif = dom.notification("Errore nel WOL!", f"Codice uscita {wake}.")

    status = get_powerstatus(config)

    return render_template("index.html", status=status, meta=meta.html(), notif=notif.html())

@app.route("/config")
def config():
    config = cesconfig.load_config()

    return render_template("config.html", ip=config.ip_addr, mac=config.mac_addr)

@app.route("/setconf", methods=['POST'])
def setconf():
    ip = request.form["ip"]
    mac = request.form["mac"]

    config = Config(ip, mac)
    cesconfig.write_config(config)

    meta = dom.refresh(5, "./")
    status = get_powerstatus(config)
    notif = dom.notification("Config. aggiornata!", f"IP: {config.ip_addr}, MAC: {config.mac_addr}")

    return render_template("index.html", meta=meta.html(), status=status, notif=notif.html())


if __name__ == "__main__":
    app.run('0.0.0.0', 6969, True)