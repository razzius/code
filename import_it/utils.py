def trim_prefix(s, prefix):
    if s.startswith(prefix):
        return s[len(prefix) :]
    return s


def trim_suffix(s, suffix):
    if s.endswith(suffix):
        return s[: -len(suffix)]
    return s
