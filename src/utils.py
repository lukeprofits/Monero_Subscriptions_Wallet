import random

def make_payment_id():
    return ''.join([random.choice('0123456789abcdef') for _ in range(16)])


def valid_address(address, primary = True):
    # Check if the wallet address is exactly 95 or 106 characters long
    if len(address) not in [95, 106]:
        return False

    # Check if the wallet address starts with the number 4

    if primary and address[0] != "4":
        return False

    # Check if the wallet address contains only valid characters
    valid_chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    for char in address:
        if char not in valid_chars:
            return False

    # If it passed all these checks
    return True

def walk_for_widget(walk_widget, target_widget):
    result = None
    for widget in walk_widget.walk():
        if type(widget) == target_widget:
            result = widget
            break
    return result