# utils/config.py
import json

def carregar_configuracao():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"CANAL_PERMITIDO_ID": None}

def salvar_configuracao(config):
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

config = carregar_configuracao()
