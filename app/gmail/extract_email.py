import re

def extract_email(sender):
    match = re.search(r"<(.+?)>", sender)

    if match:
        return match.group(1)

    return sender