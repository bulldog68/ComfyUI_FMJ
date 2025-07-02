import os
try:
    from .fmjcreaprompt import FMJCreaPrompt
    print("➡️FMJ CreaPrompt: Importation réussie de fmjcreaprompt.py")
except Exception as e:
    print(f"➡️FMJ CreaPrompt: Erreur lors de l'importation de fmjcreaprompt.py: {e}")
    raise

try:
    from .fmjkontext import FMJKontext
    print("➡️FMJ Kontext: Importation réussie de fmjkontext.py")
except Exception as e:
    print(f"➡️FMJ Kontext: Erreur lors de l'importation de fmjkontext.py: {e}")
    raise

# Modifié : Combinaison des deux nodes
NODE_CLASS_MAPPINGS = {
    "FMJCreaPrompt": FMJCreaPrompt,
    "FMJKontext": FMJKontext,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FMJCreaPrompt": "FMJ CreaPrompt",
    "FMJKontext": "FMJ Kontext",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
