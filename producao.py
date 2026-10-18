import requests

BASE = "http://127.0.0.1:8000"

novos_usuarios = [
    {"name": "Carla Mendes", "card_number": "6666"},
    {"name": "Diego Rocha", "card_number": "7777"},
    {"name": "Elisa Martins", "card_number": " 8888"},
    {"name": "João Nogueira", "card_number": " 9999"},
    {"name": "Evelyn Balbino", "card_number": "4444"},
]

for usuario in novos_usuarios:
    r = requests.post(f"{BASE}/users", json=usuario)
    if r.status_code == 201:
        print("Criado:", r.json())
    elif r.status_code == 409:
        print("Já existe, ignorado:", usuario["name"])
    else:
        print("Erro", r.status_code, r.text)

print(requests.get(f"{BASE}/users").json())