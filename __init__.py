import os
try:
    from .fmjcreaprompt import FMJCreaPrompt
    print("➡️FMJ CreaPrompt: Importation réussie de fmjcreaprompt.py")
except Exception as e:
    print(f"➡️FMJ CreaPrompt: Erreur lors de l'importation de fmjcreaprompt.py: {e}")
    raise

NODE_CLASS_MAPPINGS = {
    "FMJCreaPrompt": FMJCreaPrompt,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "FMJCreaPrompt": "FMJ CreaPrompt",
}
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]