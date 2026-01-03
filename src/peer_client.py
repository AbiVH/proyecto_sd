# src/peer_client.py
import socket
import threading
import json
import os

def download_piece(peer_ip, peer_port, piece_index, file_path):
    """Descarga un fragmento específico de un peer remoto"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((peer_ip, peer_port))
            # Mensaje de solicitud de pieza
            request = {"type": "REQUEST_PIECE", "index": piece_index}
            s.sendall(json.dumps(request).encode())
            
            chunk = s.recv(1024 * 1024) # Recibe 1MB [cite: 101]
            # Guardar en la posición correcta del archivo (Transparencia)
            with open(file_path, "r+b") as f:
                f.seek(piece_index * 1024 * 1024)
                f.write(chunk)
            return True
    except Exception as e:
        return False

class DownloadManager:
    def __init__(self, total_pieces, file_name, tracker_info):
        self.downloaded_count = 0
        self.total_pieces = total_pieces
        self.is_sharing_early = False # Regla del 20%
        self.file_name = file_name

    def check_progress(self):
        """Monitorea el progreso para activar la política del 20% """
        progress = (self.downloaded_count / self.total_pieces) * 100
        print(f"[*] Progreso de {self.file_name}: {progress:.2f}%")
        
        if progress >= 20.0 and not self.is_sharing_early:
            print("[!] Hito del 20% alcanzado. Activando modo servidor para compartir...")
            self.is_sharing_early = True
            # Aquí se llamaría a la función de UPDATE_STATUS del Tracker [cite: 33]