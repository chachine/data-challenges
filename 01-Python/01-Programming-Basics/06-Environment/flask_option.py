# pylint: disable=missing-docstring

import os

def start():
    """returns the right message"""
    if os.getenv("FLASK_ENV") is None:
        return 'Starting in empty mode...'
    else:
        return f'Starting in {os.getenv("FLASK_ENV")} mode...'

if __name__ == "__main__":
    print(start())
