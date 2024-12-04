class AppConfig:
    OLLAMA_MODEL = "aya-expanse:32b-q4_K_M"
    MAX_CHARS_PER_LINE = 100
    TRANSLATION_LANGUAGE = "Russian"
    TRANSLATION_PROMPT = "Translate this text to {language}, don't say anything else: {text} \n{language}:"
    FB2_NAMESPACE = {'fb': 'http://www.gribuser.ru/xml/fictionbook/2.0'}
    TEMP_FOLDER = "temp_fb2"
    PATE_LOGO_PATH = "images/pate_icon.svg"
