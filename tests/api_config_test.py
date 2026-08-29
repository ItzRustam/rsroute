# RSRoute
# Copyright (c) 2026 ItzRustam
# SPDX-License-Identifier: BSD-3-Clause

from dotenv import load_dotenv
import os 
from app.config import RSRouteConfig
from app.config import (_GEMINI_KEY, 
                        _OPEN_AI_API_KEY,
                        _GROQ_API_KEY,
                        _HF_TOKEN,
                        _MISTRALAI_KEY,
                        _OPENROUTER_KEY) # Keys `.env` name



def api_config_test(provider : str, key : str):
    providers = ["groq", "hf", "huggingface", "openrouter", "openai", "gemini", "mistral"]
    #  Invalid Providers
    if provider.lower() not in providers:
        return False, f"Invalid Provider supported = {providers}"

    # Matching Providers & performing Tasks
    match provider.lower():
        case "groq":
            RSRouteConfig.set_groq_key(key=key)
            if os.getenv(_GROQ_API_KEY) == key:
                return True, "Groq API Changed in Runtime successfully."
            else:
                return False, "Error while matching Keys in Runtime."
            
        case "gemini":
            RSRouteConfig.set_gemini_key(key=key)
            if os.getenv(_GEMINI_KEY) == key:
                 return True, "Gemini API Changed in Runtime successfully."
            else:
                return False, "Error while matching Keys in Runtime."
            
        case "openai":
            RSRouteConfig.set_openai_key(key=key)
            if os.getenv(_OPEN_AI_API_KEY) == key:
                 return True, "OpenAI API Changed in Runtime successfully."
            else:
                return False, "Error while matching Keys in Runtime."

            
        case "openrouter":
            RSRouteConfig.set_openrouter_key(key=key)
            if os.getenv(_OPENROUTER_KEY) == key:
                return True, "OpenRouter API Changed in Runtime successfully."
            else:
                return False, "Error while matching Keys in Runtime."
        
        case "mistral":
            RSRouteConfig.set_mistral_key(key=key)
            if os.getenv(_MISTRALAI_KEY) == key:
                return True, "MistralAI API Changed in Runtime successfully."
            else:
                return False, "Error while matching Keys in Runtime."
            
        case "hf":
            RSRouteConfig.set_hf_key(key=key)
            if os.getenv(_HF_TOKEN) == key:
                return True, "Huggingface API Changed in Runtime successfully."
            else:
                return False, "Error while matching Keys in Runtime."
            
        case "huggingface":
            RSRouteConfig.set_hf_key(key=key)
            if os.getenv(_HF_TOKEN) == key:
                return True, "Huggingface API Changed in Runtime successfully."
            else:
                return False, "Error while matching Keys in Runtime."

        
