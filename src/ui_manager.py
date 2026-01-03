# src/ui_manager.py
import os
import time

def print_dashboard(node_id, role, files_status):
    """
    Muestra la tabla de estado en tiempo real (Punto 5 de la Rúbrica)
    """
    # Limpia la terminal en Ubuntu sin generar scroll
    os.system('clear') 
    
    print("="*60)
    print(f" SISTEMA DISTRIBUIDO BITTORRENT - NODO: {node_id}")
    print(f" ROL ACTUAL: {role}")
    print("="*60)
    print(f"{'Archivo':<20} {'Progreso':<20} {'Estado'}")
    print("-"*60)
    
    for file_name, progress in files_status.items():
        # Generar barra de progreso visual
        bar_length = 20
        filled = int(round(bar_length * progress / 100))
        bar = '█' * filled + '-' * (bar_length - filled)
        
        status = "COMPLETO" if progress == 100 else "DESCARGANDO"
        print(f"{file_name:<20} |{bar}| {progress:>6.2f}%  {status}")
    
    print("-"*60)
    print("[*] Presiona Ctrl+C para salir de forma segura.")

# Ejemplo de integración en el DownloadManager
# files_status = {"Harry_Potter.mp4": 25.5, "Archivo2.zip": 100.0}