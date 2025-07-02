import random
import json
import os
import time
import hashlib
from datetime import datetime

# Modifié : chemin vers le dossier csvkontex
script_directory = os.path.dirname(__file__)
folder_paths = {
    "csv": os.path.join(script_directory, "csvkontex")
}

def new_random_seed(seed):
    rng = random.Random(seed)
    return rng.randint(1, 1125899906842624)

def getfilename(folder):
    try:
        return [filename[3:-4] for filename in sorted(os.listdir(folder)) if filename.endswith(".csv")]
    except Exception as e:
        print(f"➡️FMJ Kontex: Erreur lors de la lecture du dossier {folder}: {e}")
        return []

def select_random_line_from_collection(seed):
    rng = random.Random(seed)
    file_path = os.path.join(folder_paths["csv"], "collection.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]
            return rng.choice(lines) if lines else ""
    except Exception as e:
        print(f"➡️FMJ Kontex: Erreur lors de la lecture de collection.txt: {e}")
        return ""

def select_random_line_from_csv_file(category, folder, seed):
    rng = random.Random(seed)
    try:
        for filename in sorted(os.listdir(folder)):
            if filename.endswith(".csv") and filename[3:-4] == category:
                file_path = os.path.join(folder, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines = [line.strip() for line in file if line.strip()]
                    return rng.choice(lines) if lines else ""
        return ""
    except Exception as e:
        print(f"➡️FMJ Kontex: Erreur lors de la lecture de {category}: {e}")
        return ""

# Modifié : Changement du nom de la classe
class FMJKontex:

    RETURN_TYPES = ("STRING", "STRING", "INT")
    RETURN_NAMES = ("prompt", "prompt_debug", "seed")
    OUTPUT_IS_LIST = (True, True, False)
    FUNCTION = "create_prompt"
    CATEGORY = "FMJ"  # Groupe inchangé
    DESCRIPTION = "To reset all categories to disabled, right-click and select Fix Node."

    @classmethod
    def INPUT_TYPES(cls):
        required = {}
        folder_path = folder_paths["csv"]
        try:
            for filename in sorted(os.listdir(folder_path)):
                if filename.endswith(".csv"):
                    file_path = os.path.join(folder_path, filename)
                    lines = []
                    with open(file_path, 'r', encoding='utf-8') as file:
                        lines = [line.strip() for line in file if line.strip()]
                    required[filename[3:-4]] = (["disabled", "🎲random"] + lines, {"default": "disabled"})
        except Exception as e:
            print(f"➡️FMJ Kontex: Erreur lors de la lecture du dossier csvkontex: {e}")

        return {
            "required": required,
            "optional": {
                "KontexPrompt_Collection": (["disabled", "enabled"], {"default": "disabled"}),
                "seed": ("INT", {"default": 0, "min": -1125899906842624, "max": 1125899906842624}),
                "prefix": ("STRING", {"multiline": True, "default": ""}),
                "suffix": ("STRING", {"multiline": True, "default": ""}),
            },
            "hidden": {
                "prompt": "PROMPT",
                "extra_pnginfo": "EXTRA_PNGINFO",
                "unique_id": "UNIQUE_ID",
                "node": "NODE",
            }
        }

    @classmethod
    def IS_CHANGED(cls, seed, KontexPrompt_Collection, prefix, suffix, **kwargs):
        input_str = f"{seed}:{KontexPrompt_Collection}:{prefix}:{suffix}:{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.sha256(input_str.encode()).hexdigest()

    def create_prompt(self, seed=0, KontexPrompt_Collection="disabled", prefix="", suffix="",
                     prompt=None, extra_pnginfo=None, unique_id=None, node=None, **kwargs):
        execution_id = time.time()
        folder_path = folder_paths["csv"]
        name_of_files = getfilename(folder_path)
        final_values = []
        debug_values = []

        original_seed = seed
        if seed in (-1, -2, -3):
            seed = new_random_seed(original_seed)
            if unique_id and extra_pnginfo and isinstance(extra_pnginfo, list) and len(extra_pnginfo) > 0:
                try:
                    if isinstance(extra_pnginfo[0], dict) and "workflow" in extra_pnginfo[0]:
                        workflow = extra_pnginfo[0]["workflow"]
                        workflow_node = next((x for x in workflow["nodes"] if str(x["id"]) == str(unique_id)), None)
                        if workflow_node and "widgets_values" in workflow_node:
                            for index, widget_value in enumerate(workflow_node["widgets_values"]):
                                if widget_value == original_seed:
                                    workflow_node["widgets_values"][index] = seed
                except Exception as e:
                    print(f"➡️FMJ Kontex: Erreur lors de la mise à jour des métadonnées du workflow: {e}")

            if prompt and str(unique_id) in prompt and 'inputs' in prompt[str(unique_id)] and 'seed' in prompt[str(unique_id)]['inputs']:
                try:
                    prompt[str(unique_id)]['inputs']['seed'] = seed
                except Exception as e:
                    print(f"➡️FMJ Kontex: Erreur lors de la mise à jour du prompt: {e}")

        if KontexPrompt_Collection == "enabled":
            prompt_value = select_random_line_from_collection(seed=seed)
            if prompt_value:
                final_prompt = prompt_value
                if prefix:
                    final_prompt = f"{prefix},{final_prompt}"
                if suffix:
                    final_prompt = f"{final_prompt},{suffix}"
                final_values.append(final_prompt)
                debug_values.append(f"➡️{final_prompt}")
        else:
            values = [""] * len(name_of_files)
            for i, filename in enumerate(name_of_files):
                if kwargs.get(filename, "disabled") == "🎲random":
                    values[i] = select_random_line_from_csv_file(filename, folder_path, seed=seed)
                else:
                    values[i] = kwargs.get(filename, "disabled").strip()

            concatenated_values = ",".join(value for value in sorted(values) if value and value != "disabled")
            if concatenated_values:
                final_prompt = concatenated_values
                if prefix:
                    final_prompt = f"{prefix},{final_prompt}"
                if suffix:
                    final_prompt = f"{final_prompt},{suffix}"
                final_values.append(final_prompt)
                debug_values.append(f"➡️{final_prompt}")

        final_values = [v for v in final_values if v]
        debug_values = [v for v in debug_values if v]
        final_values.sort()
        debug_values.sort()
        final_values_str = ",".join(final_values) if final_values else ""
        debug_values_str = ",".join(debug_values) if debug_values else ""

        print(f"➡️FMJ Kontex: Prompt généré (exécution {execution_id}): {final_values_str}")
        print(f"➡️FMJ Kontex: Graine finale: {seed}")
        return (final_values, debug_values, seed)

# Modifié : Mappings pour le nouveau node
NODE_CLASS_MAPPINGS = {
    "FMJKontex": FMJKontex,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "FMJKontex": "FMJ Kontex",
}
