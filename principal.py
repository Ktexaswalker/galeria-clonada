from flask import Flask, render_template, request, redirect, send_from_directory
from bson import ObjectId
from pymongo import MongoClient
import os
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message

def comprueba_fondo():
    pass

DOCUMENTOS = ["doc", "docx"]

def usuario():
    pass

def password():
    pass

EXTENSIONES = ["png", "jpg", "jpeg"]
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./static/fondos"


client = MongoClient("mongodb://localhost:27017/")
bd = client.fondos_flask
misfondos = bd.fondos

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "ktexasw@gmail.com"
app.config["MAIL_PASSWORD"] = "qwer1234,.-"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
mail = Mail(app)

@app.route("/", methods=["GET", "POST"])
@app.route("/galeria")
def barra():
    tema = request.values.get("tema")
    estilos = {}
    if tema == None:
        estilos["todos"] = "active"
        return render_template("index.html", activo=estilos, fondos=misfondos.find())
    else:
        estilos[tema] = "active"
        return render_template("index.html", activo=estilos, fondos=misfondos.find({"tags":{"$in":[tema]}}))

@app.route("/aportar")
def aportar():
    return render_template("aportar.html")

@app.route("/insertar", methods=["POST"])
def volver():
    archivo = request.values.get("archivo")
    titulo = request.values.get("titulo")
    descripcion = request.values.get("descripcion")
    tag = []
    if request.values.get("animales"):  #Si existe... haz
        tag.append("animales")
    if request.values.get("naturaleza"):
        tag.append("naturaleza")
    if request.values.get("ciudad"):
        tag.append("ciudad")
    if request.values.get("deportes"):
        tag.append("deportes")
    if request.values.get("personas"):
        tag.append("personas")

    f = request.files['archivo']
    if f.filename == "":
        return render_template("aportar.html", mensaje="Hay que indicar un archivo de fondo")
    else:
        if archivo_permitido(f.filename):
            archivo = secure_filename(f.filename)
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], archivo))  #guardo archivo en carpeta fondos
        else:
            return render_template("aportar.html", mensaje="El archivo indicado no es una imagen!")
    misfondos.insert({"imagen":archivo, "titulo":titulo, "descripcion":descripcion, "tags":tag})
    return redirect("/")

def archivo_permitido(nombre):
    return "." in nombre and nombre.rsplit(".", 1)[1] in EXTENSIONES

@app.route("/form_email")
def email():
    id = request.values.get("_id")
    documento = misfondos.find_one({"_id": ObjectId(id)})
    return render_template("form_email.html", id=id, titulo=documento["titulo"], 
    descripcion=documento["descripcion"], email="", fondo=documento["imagen"])

@app.route("/email", methods=["POST"])
def enviar_email():
    id = request.values.get("_id")
    documento = misfondos.find_one({"_id": ObjectId(id)})
    
    msg = Message("¡Saludos desde Fondos de pantalla!", sender="ktexasw@gmail.com")
    msg.recipients = [request.values.get("email")]
    msg.body = "En este email tiene adjunto el fondo de pantalla solicitado:"
    msg.html = render_template("email.html")
    mail.send(msg)
  
    return render_template("email.html", titulo=documento["titulo"], descripcion=documento["descripcion"])


if __name__ == "__main__":
    app.run(debug=True)




"""
@app.route("/", methods=["GET", "POST"])
@app.route("/galeria")
def galeria():
    t=request.values.get("tema")
    estilos={}
    if t == None:
        l=misfondos.find()
        estilos["todos"]="active"
    else:
        l=misfondos.find({"tags": {"$in":[t]}})
        estilos[t]="active"  
    return render_template("index.html",activo=estilos, fondo=l)

@app.route("/aportar")
def aportar():
    return render_template("aportar.html")

@app.route("/insertar", methods=["POST"])
def insertar():
    f = request.files["archivo"]
    if f.filename == "":
         return render_template("aportar.html",mensaje="Hay que indicar un archivo de fondo")
    else:
        if archivo_permitido(f.filename):
            archivo = secure_filename(f.filename)
            f.save(os.path.join(app.config["UPLOAD_FOLDER"], archivo))
        else:
             return render_template("aportar.html",mensaje="¡El archivo indicado no es una imagen!")

    tit = request.values.get("titulo")
    desc = request.values.get("descripcion")
    tags=[]
    if request.values.get("animales"):
        tags.append("animales")
    if request.values.get("naturaleza"):
        tags.append("naturaleza")
    if request.values.get("ciudad"):
        tags.append("ciudad")
    if request.values.get("deporte"):
        tags.append("deporte")
    if request.values.get("personas"):
        tags.append("personas")
    misfondos.insert({"titulo":tit, "descripcion":desc, "fondo": archivo, "tags":tags})
    return redirect("/")

@app.route("/form_email")
def formulario_email():
    id=request.values.get("_id")
    documento=misfondos.find_one({"_id":ObjectId(id)})
    return render_template("form_email.html", id=id, fondo=documento["fondo"],
     titulo=documento["titulo"], descripcion=documento["descripcion"])

@app.route("/email", methods=["POST"])
def enviaemail():
    id=request.values.get("_id")
    documento=misfondos.find_one({"_id":ObjectId(id)})
    msg = Message("Fondos de pantalla Flask", sender = "alumno@cepibase.int")
    msg.recipients = [request.values.get("email")]
    msg.body = "Este es el fondo de pantalla seleccionado de nuestra galería."
    msg.html = render_template("email.html", titulo=documento["titulo"], descripcion=documento["descripcion"])
    with app.open_resource("./static/fondos/" + documento["fondo"]) as adj:
        msg.attach(documento["fondo"], "image/jpeg", adj.read())
    mail.send(msg)
    return redirect("/")
"""
