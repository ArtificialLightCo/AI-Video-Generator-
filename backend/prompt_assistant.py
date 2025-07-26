# backend/prompt_assistant.py
from gpt4all import GPT4All

class PromptAssistant:
    """
    On-device LLM for refining and enriching user prompts.
    """
    def __init__(self, model_path: str):
        # Load a local GPT4All GGML model
        self.model = GPT4All(model_path)

    def suggest(self, prompt: str, max_tokens: int = 128) -> str:
        """
        Refine the user's video prompt to be more detailed and vivid
        without altering its core meaning.
        """
        system = (
            "You are an AI assistant specialized in enhancing video generation "
            "prompts. Rewrite the user's prompt to be more descriptive, vivid, "
            "and structured, preserving the original intent."
        )
        full = f"{system}\n\nUser Prompt: {prompt}\n\nRefined Prompt:"
        resp = self.model.generate(full, max_tokens=max_tokens)
        # Strip off any leading/trailing whitespace or prompt echoes
        return resp.strip()
