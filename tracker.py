# tracker.py
import socket
import threading
import sqlite3
import json

# Configuración inicial de red [cite: 34]
HOST = '0.0.0.0' 
PORT = 5000

def init_db():
    """Inicializa la base de datos para persistencia del índice """
    conn = sqlite3.connect('tracker.db')
    cursor = conn.get_cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS peers 
                     (ip TEXT, port INTEGER, file_name TEXT, pieces TEXT, role TEXT)''')
    conn.commit()
    conn.close()

def handle_client(conn, addr):
    """Gestiona los mensajes JOIN y LIST de los nodos [cite: 33]"""
    try:
        data = conn.recv(1024).decode('utf-8')
        request = json.loads(data)
        
        if request['type'] == 'JOIN':
            # Registro inicial del nodo en la red [cite: 33]
            db = sqlite3.connect('tracker.db')
            cursor = db.cursor()
            cursor.execute("INSERT INTO peers VALUES (?, ?, ?, ?, ?)",
                           (addr[0], request['port'], request['file'], json.dumps(request['pieces']), 'Seeder'))
            db.commit()
            db.close()
            conn.send(json.dumps({"status": "OK", "message": "Registrado en el enjambre"}).encode())
            
    except Exception as e:
        print(f"Error atendiendo a {addr}: {e}")
    finally:
        conn.close()

def start_tracker():
    init_db()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SO_REUSEADDR para permitir reinicios rápidos en Ubuntu [cite: 34]
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Tracker escuchando en {HOST}:{PORT}...")
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_tracker()