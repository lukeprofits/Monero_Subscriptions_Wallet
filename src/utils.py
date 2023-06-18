def make_payment_id():
    return ''.join([random.choice('0123456789abcdef') for _ in range(16)])


