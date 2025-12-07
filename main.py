import os
from replit_ai import Chat
import subprocess
import time

PREGUNTA_FILE = "pregunta.txt"
CHAT_FILE = "chat.txt"

def ask_ai(prompt):
    response = Chat.complete(
        model="replit/gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def append_to_chat(prompt, answer):
    with open(CHAT_FILE, "a", encoding="utf-8") as f:
        f.write("\n\nUsuario: " + prompt)
        f.write("\nIA: " + answer)

def clear_pregunta_file():
    with open(PREGUNTA_FILE, "w", encoding="utf-8") as f:
        f.write("")  # vaciar archivo

def git_push():
    token = os.environ["GITHUB_TOKEN"]  # <-- SEGURO

    # Configurar remote con token
    subprocess.run([
        "git", "remote", "set-url", "origin",
        f"https://{token}@github.com/PrincipeGhost/GitHub.git"  # <-- AQUI CAMBIA TU REPO
    ])

    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Nueva respuesta del chat"], stderr=subprocess.DEVNULL)
    subprocess.run(["git", "push"], stderr=subprocess.DEVNULL)

print("🤖 IA monitoreando pregunta.txt… Escribe preguntas en el archivo desde GitHub.")
print("CTRL+C para salir.\n")

while True:
    try:
        if os.path.exists(PREGUNTA_FILE):
            with open(PREGUNTA_FILE, "r", encoding="utf-8") as f:
                pregunta = f.read().strip()

            if pregunta:
                print("Pregunta detectada:", pregunta)

                respuesta = ask_ai(pregunta)
                print("Respuesta:", respuesta)

                append_to_chat(pregunta, respuesta)
                clear_pregunta_file()
                git_push()

        time.sleep(5)

    except KeyboardInterrupt:
        print("\nChat detenido manualmente.")
        break
