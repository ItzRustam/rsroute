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

