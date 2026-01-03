# src/persistence_manager.py
import json
import os

class CheckpointManager:
    def __init__(self, file_id, total_pieces):
        self.state_file = f"meta/{file_id}_state.json"
        self.total_pieces = total_pieces
        self.bitfield = self._load_state()

    def _load_state(self):
        """Carga el progreso previo desde el disco [cite: 64, 81]"""
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        # Si es nuevo, inicializa el bitfield en 0
        return [0] * self.total_pieces

    def save_piece_status(self, index, status=1):
        """Guarda el progreso de forma persistente cada 5 piezas [cite: 101]"""
        self.bitfield[index] = status
        with open(self.state_file, 'w') as f:
            json.dump(self.bitfield, f)

    def get_missing_indices(self):
        """Identifica qué piezas faltan para reanudar la descarga [cite: 82]"""
        return [i for i, status in enumerate(self.bitfield) if status == 0]

    def get_progress_percentage(self):
        downloaded = sum(self.bitfield)
        return (downloaded / self.total_pieces) * 100