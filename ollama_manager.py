# ollama_manager.py
import requests

def get_ollama_models(base_url="http://localhost:11434"):
    """Récupère la liste des modèles disponibles dans Ollama."""
    try:
        response = requests.get(f"{base_url.rstrip('/')}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return [model["name"] for model in data.get("models", []) if "name" in model]
    except Exception as e:
        print(f"⚠️ FMJ Llm Config: impossible de charger les modèles : {e}")
    return ["llama3", "qwen3", "moondream", "llava", "phi3"]

class FMJLlmConfigNode:
    """⚙️ FMJ Llm Config — Configure l'URL Ollama et sélectionne un modèle."""

    @classmethod
    def INPUT_TYPES(cls):
        # Utilise l'URL par défaut pour charger les modèles
        models = get_ollama_models()
        if not models:
            models = ["llama3"]
        return {
            "required": {
                "ollama_url": ("STRING", {"default": "http://localhost:11434"}),
                "selected_model": (models, {"default": models[0]}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("model_name", "ollama_url")
    FUNCTION = "output_config"
    CATEGORY = "🌀FMJ"

    def output_config(self, ollama_url, selected_model):
        return (selected_model, ollama_url)


# 🔸 Enregistrement du nœud
NODE_CLASS_MAPPINGS = {
    "FMJLlmConfigNode": FMJLlmConfigNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FMJLlmConfigNode": "⚙️ FMJ Llm Config"  # 👈 Nom mis à jour
}
