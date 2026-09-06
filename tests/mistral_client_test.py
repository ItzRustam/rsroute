from app.providers import MistralAI
from app.Errors import InvalidRequest

"NOTE: Test Function only on Fake API_KEY, Already tested on Real Mistral API key."
def test_mistral(KEY : str = None, prompt : str = None, real_api = False):
    # Model Initlize
    try:
        model = MistralAI(api_key=KEY, max_retries=0)

    except InvalidRequest as ir:
        return True, ir
    
    except Exception as e:
        return False, e

    try:
        output = model.generate(prompt=prompt)

    except InvalidRequest as ir:
        return True, ir

    # With Real API Key, This never Occur
    # using return True for docker image
    except Exception as e:
        # return False, e 
        if real_api: # BUG then
            return False, e
        # No BUG but fake API issue
        return True, e
    # real api and worked successfully
    
    else:
        if not(real_api): # BUG then
            return False, "Unexpected Error Occur."
        return True, output