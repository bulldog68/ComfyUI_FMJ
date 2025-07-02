import os
try:
    from .fmjcreaprompt import FMJCreaPrompt
    print("➡️FMJ CreaPrompt: Importation réussie de fmjcreaprompt.py")
except Exception as e:
    print(f"➡️FMJ CreaPrompt: Erreur lors de l'importation de fmjcreaprompt.py: {e}")
    raise

try:
    from .fmjkontex import FMJKontex
    print("➡️FMJ Kontex: Importation réussie de fmjkontex.py")
except Exception as e:
    print(f"➡️FMJ Kontex: Erreur lors de l'importation de fmjkontex.py: {e}")
    raise

# Modifié : Combinaison des deux nodes
NODE_CLASS_MAPPINGS = {
    "FMJCreaPrompt": FMJCreaPrompt,
    "FMJKontex": FMJKontex,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FMJCreaPrompt": "FMJ CreaPrompt",
    "FMJKontex": "FMJ Kontex",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
