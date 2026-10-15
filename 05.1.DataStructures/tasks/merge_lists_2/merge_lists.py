import typing as tp
import heapq


def merge(seq: tp.Sequence[tp.Sequence[int]]) -> list[int]:
    """
    :param seq: sequence of sorted sequences
    :return: merged sorted list
    """
    res = []
    heap = []
    for i, s in enumerate(seq):
        if s:
            heapq.heappush(heap, (s[0], i, 0))
    while heap:
        val, idx, el_idx = heapq.heappop(heap)
        res.append(val)

        next_el_idx = el_idx + 1
        if next_el_idx < len(seq[idx]):
            next_val = seq[idx][next_el_idx]
            heapq.heappush(heap, (next_val, idx, next_el_idx))
    return res
