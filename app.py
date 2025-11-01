from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import secrets
import string
import hashlib
import base64

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# --------------------- Home Route ---------------------
@app.route("/")
def home():
    return render_template("password-generator.html")

# --------------------- Password Generator ---------------------
@app.route("/generate", methods=["POST"])
def generate_password():
    data = request.get_json(force=True, silent=True)
    length = int(data.get("length", 12))
    include_upper = data.get("uppercase", True)
    include_lower = data.get("lowercase", True)
    include_numbers = data.get("numbers", True)
    include_symbols = data.get("symbols", True)

    chars = ""
    if include_upper:
        chars += string.ascii_uppercase
    if include_lower:
        chars += string.ascii_lowercase
    if include_numbers:
        chars += string.digits
    if include_symbols:
        chars += "!@#$%^&*()-_=+[]{}|;:,.<>?/~"

    if not chars:
        return jsonify({"error": "No character types selected"}), 400

    password = "".join(secrets.choice(chars) for _ in range(length))
    return jsonify({"password": password})

# --------------------- Hash Password ---------------------
@app.route("/hash", methods=["POST"])
def hash_password():
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    password = data.get("password", "")
    if not isinstance(password, str) or password == "":
        return jsonify({"error": "Password is required"}), 400

    algorithm = data.get("algorithm", "pbkdf2").lower()
    if algorithm not in ("sha256", "pbkdf2"):
        return jsonify({"error": "Unsupported algorithm"}), 400

    # Simple SHA-256
    if algorithm == "sha256":
        digest = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return jsonify({"hash": digest})

    # PBKDF2 (salted)
    iterations = int(data.get("iterations", 100000))
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations, dklen=32)
    dk_b64 = base64.b64encode(dk).decode("utf-8")
    return jsonify({"hash": dk_b64})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
