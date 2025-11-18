# ollama_vision.py
import torch
from PIL import Image as PILImage
import numpy as np
from io import BytesIO
import base64
import csv
from pathlib import Path
from ollama import Client

def tensor_to_base64(image_tensor):
    """Convertit un tenseur ComfyUI en base64 (méthode identique au node fonctionnel)."""
    image = image_tensor.squeeze(0)
    i = 255. * image.cpu().numpy()
    img = PILImage.fromarray(np.clip(i, 0, 255).astype(np.uint8))
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_bytes = base64.b64encode(buffered.getvalue())
    return str(img_bytes, 'utf-8')

CSVV_DIR = Path(__file__).parent / "csvv"

def load_vision_prompts():
    """Charge les prompts depuis csvv/*.csv"""
    prompts = {}
    if not CSVV_DIR.exists():
        return prompts
    for csv_file in CSVV_DIR.glob("*.csv"):
        try:
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if 'description_type' in reader.fieldnames and 'system_prompt' in reader.fieldnames:
                    for row in reader:
                        dtype = row['description_type'].strip()
                        prompt = row['system_prompt'].strip()
                        if dtype and prompt:
                            prompts[dtype] = prompt
        except Exception as e:
            print(f"❌ Erreur lecture {csv_file}: {e}")
    return prompts

class FMJLlmOllamaVision:
    """👁️ FMJ Llm Ollama Vision — Analyse d'images via modèles multimodaux."""
    
    @classmethod
    def INPUT_TYPES(cls):
        prompts = load_vision_prompts()
        desc_types = list(prompts.keys()) or ["_aucun_prompt_dans_csvv_"]
        return {
            "required": {
                "image": ("IMAGE",),
                "description_type": (desc_types, {"default": desc_types[0]}),
                "model_name": ("STRING", {"default": "qwen3-vl:2b"}),
                "ollama_url": ("STRING", {"default": "http://localhost:11434"}),
                "max_tokens": ("INT", {
                    "default": 512,
                    "min": 1,
                    "max": 16384,
                    "tooltip": "Nombre max de tokens pour la description (16384 pour détails)."
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
    RETURN_NAMES = ("description", "debug_info")
    FUNCTION = "describe_image"
    CATEGORY = "🌀FMJ"

    def describe_image(self, image, description_type, model_name, ollama_url, max_tokens, temperature, seed, keep_alive):
        prompts = load_vision_prompts()
        system_prompt = prompts.get(description_type)
        if system_prompt is None:
            error_msg = f"❌ Type '{description_type}' introuvable. Vérifiez le dossier 'csvv/'."
            return (error_msg, error_msg)

        try:
            img_b64 = tensor_to_base64(image)
        except Exception as e:
            return (f"❌ Échec conversion image : {e}", str(e))

        client = Client(host=ollama_url.rstrip('/'))

        try:
            # --- MÉTHODE IDENTIQUE AU NODE FONCTIONNEL ---
            response = client.generate(
                model=model_name,
                system=system_prompt,         # ← Instruction système séparée
                prompt="Décris cette image.",   # ← Prompt utilisateur simple
                images=[img_b64],              # ← Image en base64
                options={
                    "num_predict": max_tokens,
                    "temperature": temperature,
                    "seed": seed
                },
                keep_alive=f"{keep_alive}m"
            )
            # -------------------------------------------

            desc = response.get('response', '').strip()
            if not desc:
                desc = "⚠️ Description vide de la part du modèle."
            debug = f"✅ Vision réussie\nType : {description_type}\nModèle : {model_name}"
            return (desc, debug)

        except Exception as e:
            error_detail = f"❌ Erreur Vision : {str(e)}"
            return (error_detail, error_detail)
