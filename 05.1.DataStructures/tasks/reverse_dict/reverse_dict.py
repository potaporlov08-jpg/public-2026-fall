import typing as tp


def revert(dct: tp.Mapping[str, str]) -> dict[str, list[str]]:
    """
    :param dct: dictionary to revert in format {key: value}
    :return: reverted dictionary {value: [key1, key2, key3]}
    """
    res = dict()
    for key, value in dct.items():
        if value not in res:
            res[value] = [key]
        else:
            res[value].append(key)
    return res
