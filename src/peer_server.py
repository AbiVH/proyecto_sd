# src/peer_server.py
import socket
import threading
import os
import hashlib
import json

PIECE_SIZE = 1024 * 1024  # 1MB por pieza [cite: 101]

def get_file_metadata(file_path):
    """Divide el archivo en piezas y genera hashes para integridad """
    file_size = os.path.getsize(file_path)
    pieces = []
    with open(file_path, "rb") as f:
        while True:
            data = f.read(PIECE_SIZE)
            if not data:
                break
            pieces.append(hashlib.sha256(data).hexdigest()) # [cite: 101]
    return pieces, file_size

def handle_request(client_socket, file_path):
    """Envia fragmentos específicos usando desplazamientos (seek) [cite: 58, 79]"""
    try:
        data = client_socket.recv(1024).decode()
        request = json.loads(data)
        
        if request['type'] == 'REQUEST_PIECE':
            index = request['index']
            offset = index * PIECE_SIZE
            
            with open(file_path, "rb") as f:
                f.seek(offset)
                chunk = f.read(PIECE_SIZE)
                client_socket.sendall(chunk) # [cite: 33]
    finally:
        client_socket.close()

def start_peer_server(port, file_to_share):
    """Inicia el hilo servidor del Peer para subir datos [cite: 89]"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # [cite: 34]
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[*] Peer servidor activo en puerto {port}, compartiendo {file_to_share}")
    
    while True:
        conn, addr = server.accept()
        # Worker Thread efímero para cada petición [cite: 90]
        threading.Thread(target=handle_request, args=(conn, file_to_share)).start()