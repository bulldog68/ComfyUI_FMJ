# ollama_prompt.py
import os
import csv
from pathlib import Path
from ollama import Client

CSV_DIR = Path(__file__).parent / "csv"

def load_prompts_from_csv():
    """Charge les prompts depuis csv/*.csv"""
    prompts = {}
    if not CSV_DIR.exists():
        return prompts
    for csv_file in CSV_DIR.glob("*.csv"):
        try:
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if 'prompt_style' in reader.fieldnames and 'system_prompt' in reader.fieldnames:
                    for row in reader:
                        style = row['prompt_style'].strip()
                        system_prompt = row['system_prompt'].strip()
                        if style and system_prompt:
                            prompts[style] = system_prompt
        except Exception as e:
            print(f"❌ Erreur lecture {csv_file}: {e}")
    return prompts

class FMJOllamaPromptGenerator:
    """🦜FMJ Ollama Prompt Generator — Génère des prompts avancés via Ollama."""
    
    @classmethod
    def INPUT_TYPES(cls):
        PROMPT_STYLES = load_prompts_from_csv()
        style_list = list(PROMPT_STYLES.keys()) if PROMPT_STYLES else ["_aucun_prompt_dans_csv_"]
        return {
            "required": {
                # 🔸 ENTRÉE TEXTE EXTERNE (obligatoire)
                "text": ("STRING", {"forceInput": True}),
                "prompt_style": (style_list, {"default": style_list[0]}),
                "model_name": ("STRING", {"default": "qwen3:2b"}),
                "ollama_url": ("STRING", {"default": "http://localhost:11434"}),
                "max_tokens": ("INT", {
                    "default": 512,
                    "min": 1,
                    "max": 16384,
                    "tooltip": "Nombre max de tokens à générer (16384 pour prompts longs)."
                }),
                "temperature": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 10.0, "step": 0.1}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "keep_alive": ("INT", {
                    "default": 5,
                    "min": -1,
                    "max": 120,
                    "tooltip": "Durée (min) de mise en cache du modèle. -1=persistant, 0=décharger immédiatement."
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("response", "debug_info")
    FUNCTION = "generate"
    CATEGORY = "🌀FMJ"

    def generate(self, text, prompt_style, model_name, ollama_url, max_tokens, temperature, seed, keep_alive):
        # Charger les prompts
        PROMPT_STYLES = load_prompts_from_csv()
        system_instruction = PROMPT_STYLES.get(prompt_style)
        if system_instruction is None:
            error_msg = f"❌ Style '{prompt_style}' introuvable. Vérifiez le dossier 'csv/'."
            return (error_msg, error_msg)

        # Construire le prompt utilisateur avec le texte fourni
        if prompt_style == "qwen_edit":
            user_prompt = text  # Pour qwen_edit, le texte est la requête d'édition
        else:
            user_prompt = f"Sujet : {text}\n\nRéponse :"

        # Configurer le client Ollama
        client = Client(host=ollama_url.rstrip('/'))

        try:
            response = client.generate(
                model=model_name,
                system=system_instruction,
                prompt=user_prompt,
                options={
                    "num_predict": max_tokens,
                    "temperature": temperature,
                    "seed": seed
                },
                keep_alive=f"{keep_alive}m"
            )

            output_text = response.get('response', '').strip()
            if not output_text:
                output_text = "⚠️ Réponse vide de la part du modèle."
            debug = f"✅ Prompt généré\nStyle : {prompt_style}\nModèle : {model_name}"
            return (output_text, debug)

        except Exception as e:
            error_detail = f"❌ Erreur LLM : {str(e)}"
            return (error_detail, error_detail)
