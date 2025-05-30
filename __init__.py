import os
try:
    from .creaprompt import CreaPrompt
    print("➡️CreaPrompt: Importation réussie de creaprompt.py")
except Exception as e:
    print(f"➡️CreaPrompt: Erreur lors de l'importation de creaprompt.py: {e}")
    raise

NODE_CLASS_MAPPINGS = {
    "CreaPrompt": CreaPrompt,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "CreaPrompt": "CreaPrompt FMJ",
}
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]