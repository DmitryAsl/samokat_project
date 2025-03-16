import os


def relative_from_root(path: str):
    return os.path.normpath(os.path.join(os.path.dirname(__file__), '..', path))
