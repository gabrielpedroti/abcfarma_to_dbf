from datetime import datetime
import os

LOG_DIR = os.path.join(os.getcwd(), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# --- SALVA LOG EM ARQUIVO TXT ---
def salvar_log(mensagem):
    with open(os.path.join(LOG_DIR, "log_execucao.txt"), "a", encoding="utf-8") as log:
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        log.write(f"{timestamp} - {mensagem}\n")