

_SUPPORTED_CODES = [1, 4, 31, 32]


def _base(msg, code):
    if (not code in _SUPPORTED_CODES):
        raise "Code %s not supported for log" % code

    return "\033[%dm%s\033[0m" % (code, msg)


def bold(msg):
    return _base(msg, 1)


def underline(msg):
    return _base(msg, 4)


def red(msg):
    return _base(msg, 31)


def green(msg):
    return _base(msg, 32)
