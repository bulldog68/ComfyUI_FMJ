# __init__.py

from .ollama_manager import FMJLlmConfigNode
from .ollama_unload import FMJUnloadAllLLM
from .ollama_prompt import FMJOllamaPromptGenerator
from .ollama_vision import FMJLlmOllamaVision

NODE_CLASS_MAPPINGS = {
    "FMJLlmConfigNode": FMJLlmConfigNode,
    "FMJUnloadAllLLM": FMJUnloadAllLLM,
    "FMJOllamaPromptGenerator": FMJOllamaPromptGenerator,
    "FMJLlmOllamaVision": FMJLlmOllamaVision,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FMJLlmConfigNode": "⚙️ FMJ Llm Config",
    "FMJUnloadAllLLM": "🧹 FMJ Unload All LLM",
    "FMJOllamaPromptGenerator": "🦙FMJ Ollama Prompt Generator",
    "FMJLlmOllamaVision": "👁️ FMJ Llm Ollama Vision",
}
