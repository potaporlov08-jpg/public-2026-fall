import typing as tp


def traverse_dictionary_mutable(d: dict, result: list, prefix: str = "") -> None:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param prefix: prefix for key used for passing total path through recursion
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    for key, value in d.items():
        new_key = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, dict):
            traverse_dictionary_mutable(value, result, new_key)
        else:
            result.append((new_key, value))


def traverse_dictionary_immutable(d: dict, prefix: str = "") -> list:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :param result: list with pairs: (full key from root to leaf joined by ".", value)
    :param prefix: prefix for key used for passing total path through recursion
    :return: None
    """
    result = []
    for key, value in d.items():
        new_key = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, dict):
            result = result + traverse_dictionary_immutable(value, new_key)
        else:
            result = result + [(new_key, value)]
    return result


def traverse_dictionary_iterative(d: dict) -> list:
    """
    :param dct: dictionary of undefined depth with integers or other dicts as leaves with same properties
    :return: list with pairs: (full key from root to leaf joined by ".", value)
    """
    result = []
    stack = [("", k, v) for k, v in reversed(list(d.items()))]
    while stack:
        prefix, key, value = stack.pop()
        new_key = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(value, dict):
            for k, v in reversed(list(value.items())):
                stack.append((new_key, k, v))
        else:
            result.append((new_key, value))
    return result
