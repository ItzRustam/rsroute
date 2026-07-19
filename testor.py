from tests import auth_test

# Authrentication Test
# Case #1 - None.
auth_test()

# Case #2 - Invalid key suffix
auth_test(master_key="blablabla")

# Case #3 - Invalid key
auth_test(master_key="rsllm_invalid_token")

# Case #4 - Valid Key
auth_test(master_key="rsllm_xxxxxxx") # Hidded the Key.
