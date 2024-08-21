def shortened_wallet(wallet, length=5):
    return f"{wallet[:length]}...{wallet[-length:]}"
