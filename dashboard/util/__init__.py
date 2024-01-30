import os


def osnvironget(env):
    val = os.environ.get(env)
    if val is not None:
        if val != "":
            return val
    return None
