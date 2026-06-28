from pathlib import Path

def load_config():
    config_path = Path(__file__).resolve().parent.parent / "config" / "config.txt"
    if config_path.is_file():
        print(f"Loading configuration from {config_path}")
        content = config_path.read_text(encoding="utf-8").strip()
        if not content:
            print("Configuration file is empty.")
            return {}
        config = {}
        print(f"Raw config content:\n{content}")
        for line in content.splitlines():
            if not line or "=" not in line:
                continue
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()
            
        if "regex" not in config:
            print("Configuration file does not contain a 'regex' entry.")
            return {}
        return config
    
    print(f"Configuration file {config_path} not found. Using default settings.")
    return {}

def apply_regex(text: str, regex_config: dict) -> list:
    """Apply regex transformations to the extracted text based on the config.

    Args:
        text: The extracted text from the PDF.
        regex_config: A dictionary containing regex patterns and their replacements.

    Returns:
        The transformed text after applying the regex rules.
    """
    import re
    if regex_config is None or "regex" not in regex_config:
        print("Regex configuration missing. Returning no matches.")
        return []
    matches = []
    pattern = regex_config["regex"]
    matches = re.findall(pattern, text, re.DOTALL)
    return matches
