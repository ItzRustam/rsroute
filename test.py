from app.config import RSRouteConfig

# RSRouteConfig.set_mistral_key(key="yup_done.mistral.key")

import os
from dotenv import load_dotenv
load_dotenv()

print(os.getenv("MISTRAL_API_KEY"))