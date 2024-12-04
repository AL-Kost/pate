import ollama
from app_config import AppConfig

def translate_text_ollama(text):
    lang_name = AppConfig.TRANSLATION_LANGUAGE
    prompt = AppConfig.TRANSLATION_PROMPT.format(language=lang_name, text=text)
    messages = [{'role': 'user', 'content': prompt}]
    try:
        response = ollama.chat(model=AppConfig.OLLAMA_MODEL, messages=messages)
        return response['message']['content'].strip().replace("-", "–")
    except Exception as e:
        return f"Translation failed: {str(e)}"
