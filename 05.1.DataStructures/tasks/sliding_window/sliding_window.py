from collections import deque


def sliding_window_max(nums: list[int], k: int) -> list[int]:
    """
    Returns maximum values for every sliding window of size k.

    Args:
        nums: Input list of numbers.
        k: Window size.

    Returns:
        List of window maximums.
        If nums is empty, k <= 0, or k > len(nums), returns an empty list.
    """
    if not nums or k <= 0 or k > len(nums):
        return []

    res = []
    wind = deque()
    for i, num in enumerate(nums):
        while wind and wind[0] <= i - k:
            wind.popleft()
        while wind and nums[wind[-1]] <= num:
            wind.pop()
        wind.append(i)
        if i >= k - 1:
            res.append(nums[wind[0]])
    return res
