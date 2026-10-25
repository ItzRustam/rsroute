from app.providers import ChatGroq
from app.providers.groq_client import GROQ_MODELS
from app.Errors import InvalidRequest

"NOTE: Test Function only on Fake API_KEY."
def test_groq(KEY : str = None, query : str = None, real_api = False):
    # Model Initlize
    try:
        model = ChatGroq(api_key=KEY)

    except InvalidRequest as ir:
        return True, ir

    except Exception as e:
        return False, e

    try:
        output = model(query=query)

    except InvalidRequest as ir:
        return True, ir

    # With Real API Key, This never Occur
    # using return True for docker image
    except Exception as e:
        if real_api: # BUG then
            return False, e
        # No BUG but fake API issue
        return True, e
    # real api and worked successfully

    else:
        if not(real_api): # BUG then
            return False, "Unexpected Error Occur."
        return True, output


def test_groq_models(KEY : str = "my_groq_key"):
    """Only `GROQ_MODELS` must be accepted, everything else must raise InvalidRequest (no network used)."""
    for name in GROQ_MODELS:
        try:
            ChatGroq(api_key=KEY, model=name)
        except Exception as e:
            return False, f"allowed model `{name}` rejected: {e}"

    for bad in ["llama-3.3-70b-versatile", "qwen/qwen3-32b", "", "random-model"]:
        try:
            ChatGroq(api_key=KEY, model=bad)
        except InvalidRequest:
            continue
        except Exception as e:
            return False, f"`{bad}` raised {type(e).__name__} instead of InvalidRequest"
        return False, f"model `{bad}` should have been rejected"

    return True, "Only allowed Groq models are accepted."
