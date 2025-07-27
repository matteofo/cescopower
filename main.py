from flask import *
from wol import *
import cesconfig, json, dom
import hashlib

app = Flask(__name__)

def verify_login() -> bool:
    config = cesconfig.load_config()

    cookie = request.cookies.get("cescopower-auth")
    if not cookie or cookie != config.password:
        return False
    
    return True

@app.route("/login", methods=["POST"])
def login():
    password = request.form["pass"]
    pass_hash = hashlib.sha256(password.encode()).hexdigest()

    config = cesconfig.load_config()

    print(pass_hash)

    if pass_hash == config.password:
        resp = make_response()
        resp.status = 302
        resp.headers.add("Location", "./")
        resp.headers.add("Refresh", 1)
        resp.set_cookie("cescopower-auth", pass_hash)
        return resp
    else:
        notif = dom.notification("Password errata!")
        return render_template("auth.html", notif=notif.html())
    
@app.route("/logout")
def logout():
    if not verify_login():
        return redirect(url_for("auth"))

    resp = make_response()
    resp.status = 302
    resp.headers.add("Location", "./")
    resp.set_cookie("cescopower-auth", "", max_age=0)
    return resp

@app.route("/auth")
def auth():
    if verify_login():
        return redirect("/")

    return render_template("auth.html")

@app.route("/")
def root():
    if not verify_login():
        return redirect(url_for("auth"))
    
    config = cesconfig.load_config()
    status = get_powerstatus(config)
    meta = dom.refresh(5, "./")

    return render_template("index.html", meta=meta.html(), status=status)

@app.route("/wake")
def wake():
    if not verify_login():
        return redirect(url_for("auth"))
    
    config = cesconfig.load_config()

    meta = dom.refresh(3, "./")
    wake = try_wake(config)
    notif = dom.notification("WOL inviato!")

    if wake != 0:
        notif = dom.notification(f"Errore {wake} nel WOL!")

    status = get_powerstatus(config)

    return render_template("index.html", status=status, meta=meta.html(), notif=notif.html())

@app.route("/config")
def config():
    if not verify_login():
        return redirect(url_for("auth"))
    
    config = cesconfig.load_config()

    return render_template("config.html", ip=config.ip_addr, mac=config.mac_addr)

@app.route("/setconf", methods=['POST'])
def setconf():
    if not verify_login():
        return redirect(url_for("auth"))

    ip = request.form["ip"]
    mac = request.form["mac"]

    config = Config(ip, mac, cesconfig.load_config().password)
    cesconfig.write_config(config)

    meta = dom.refresh(5, "./")
    status = get_powerstatus(config)
    notif = dom.notification("Config. aggiornata!")

    return render_template("index.html", meta=meta.html(), status=status, notif=notif.html())


if __name__ == "__main__":
    app.run('0.0.0.0', 6969, True)