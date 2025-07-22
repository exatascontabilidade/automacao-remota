from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import base64
import os

app = Flask(__name__)
CORS(app, origins=["https://automacao-remota.vercel.app"])  # ✅ permite requisições da Vercel

# Token será definido como variável de ambiente no Render
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO = "exatascontabilidade/automacao-remota"
ARQUIVO = "comando.json"
API_URL = f"https://api.github.com/repos/{REPO}/contents/{ARQUIVO}"

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

@app.route("/executar", methods=["POST"])
def executar_comando():
    try:
        # Obter SHA atual
        res = requests.get(API_URL, headers=HEADERS)
        if res.status_code != 200:
            return jsonify(success=False, error="Erro ao obter SHA"), 500

        sha = res.json().get("sha")
        novo_conteudo = base64.b64encode(b'{"executar": true}').decode("utf-8")

        # Atualizar o arquivo
        payload = {
            "message": "🚀 Atualizar comando.json para executar",
            "content": novo_conteudo,
            "sha": sha
        }

        res_update = requests.put(API_URL, headers=HEADERS, json=payload)
        if res_update.status_code in [200, 201]:
            return jsonify(success=True)
        else:
            return jsonify(success=False, error=res_update.text), 500

    except Exception as e:
        return jsonify(success=False, error=str(e)), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify(message="API de automação ativa. Use POST /executar"), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
