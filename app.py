from flask import Flask, request, jsonify
from flask_cors import CORS
from bson import ObjectId
from mongo_conn import usuarios_col  # colección de Mongo
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


def serialize_doc(doc):
    """Convierte ObjectId a str para poder devolver JSON."""
    if not doc:
        return doc
    doc = dict(doc)
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc


# ---------- HEALTHCHECK / PING ----------
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "API MarketLink OK"}), 200


# ---------- CREAR USUARIO ----------
@app.route("/usuarios", methods=["POST"])
def crear_usuario_api():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Se requiere un JSON en el cuerpo"}), 400

    usuario = {
        "nombre": data.get("nombre"),
        "email": data.get("email"),
        "password": data.get("password"),
        "rol": data.get("rol", "usuario")
    }

    if not usuario["nombre"] or not usuario["email"] or not usuario["password"]:
        return jsonify({"error": "nombre, email y password son obligatorios"}), 400

    result = usuarios_col.insert_one(usuario)
    usuario["_id"] = result.inserted_id

    return jsonify({
        "message": "Usuario creado",
        "data": serialize_doc(usuario)
    }), 201


# ---------- LISTAR USUARIOS ----------
@app.route("/usuarios", methods=["GET"])
def listar_usuarios_api():
    usuarios = [serialize_doc(u) for u in usuarios_col.find()]
    return jsonify(usuarios), 200


# ---------- OBTENER USUARIO POR ID ----------
@app.route("/usuarios/<id_usuario>", methods=["GET"])
def obtener_usuario_api(id_usuario):
    try:
        oid = ObjectId(id_usuario)
    except:
        return jsonify({"error": "ID inválido"}), 400

    usuario = usuarios_col.find_one({"_id": oid})
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify(serialize_doc(usuario)), 200


# ---------- ACTUALIZAR USUARIO ----------
@app.route("/usuarios/<id_usuario>", methods=["PUT"])
def actualizar_usuario_api(id_usuario):
    try:
        oid = ObjectId(id_usuario)
    except:
        return jsonify({"error": "ID inválido"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"error": "Se requiere un JSON en el cuerpo"}), 400

    if "_id" in data:
        data.pop("_id")

    result = usuarios_col.update_one({"_id": oid}, {"$set": data})

    if result.matched_count == 0:
        return jsonify({"error": "Usuario no encontrado"}), 404

    usuario_actualizado = usuarios_col.find_one({"_id": oid})
    return jsonify({
        "message": "Usuario actualizado",
        "data": serialize_doc(usuario_actualizado)
    }), 200


# ---------- ELIMINAR USUARIO ----------
@app.route("/usuarios/<id_usuario>", methods=["DELETE"])
def eliminar_usuario_api(id_usuario):
    try:
        oid = ObjectId(id_usuario)
    except:
        return jsonify({"error": "ID inválido"}), 400

    result = usuarios_col.delete_one({"_id": oid})

    if result.deleted_count == 0:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({"message": "Usuario eliminado"}), 200


if __name__ == "__main__":
    # Puerto 5000 para el backend
    app.run(host="0.0.0.0", port=5000)


