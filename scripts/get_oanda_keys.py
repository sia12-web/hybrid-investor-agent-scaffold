import keyring


def mask(v):
    return (v[:3] + "..." + v[-3:]) if v and len(v) > 6 else v


for k in ("api_key", "account_id", "environment"):
    v = keyring.get_password("oanda", k)
    print(f"{k}: {mask(v)}")
