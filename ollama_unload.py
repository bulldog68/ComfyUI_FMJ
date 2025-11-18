# ollama_unload.py
import requests

class FMJUnloadAllLLM:
    """🧹 FMJ Unload All LLM — Décharge tous les modèles Ollama (localhost:11434)."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "trigger": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)
    FUNCTION = "unload_all"
    CATEGORY = "🌀FMJ"

    def unload_all(self, trigger):
        OLLAMA_URL = "http://localhost:11434"  # URL fixe
        
        if not trigger:
            return ("⚠️ Déchargement non déclenché (trigger = False).",)
        
        try:
            requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={"model": "dummy", "keep_alive": 0},
                timeout=5
            )
            return ("✅ Tous les modèles Ollama ont été déchargés.",)
        except Exception as e:
            return (f"❌ Erreur lors du déchargement : {str(e)}",)
