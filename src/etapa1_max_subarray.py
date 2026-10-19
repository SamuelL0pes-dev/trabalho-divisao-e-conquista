from typing import List, Tuple


def _tie_break(cand_sum: int, cand_start: int, cand_end: int,
               best_sum: int, best_start: int, best_end: int) -> bool:
    if cand_sum > best_sum:
        return True
    if cand_sum < best_sum:
        return False

    cand_len = cand_end - cand_start + 1
    best_len = best_end - best_start + 1
    if cand_len < best_len:
        return True
    if cand_len > best_len:
        return False

    return cand_start < best_start


def max_subarray_brute_force(arr: List[int]) -> Tuple[int, int, int]:
    n = len(arr)
    if n == 0:
        raise ValueError("O vetor não pode ser vazio.")

    best_sum = arr[0]
    best_start = 0
    best_end = 0

    for i in range(n):
        current_sum = 0
        for j in range(i, n):
            current_sum += arr[j]
            if _tie_break(current_sum, i, j, best_sum, best_start, best_end):
                best_sum = current_sum
                best_start = i
                best_end = j

    return best_sum, best_start, best_end


def _find_max_crossing_subarray(arr: List[int], low: int, mid: int, high: int) -> Tuple[int, int, int]:
    max_left_sum = arr[mid]
    max_left_idx = mid
    current_sum = 0

    for i in range(mid, low - 1, -1):
        current_sum += arr[i]
        if current_sum > max_left_sum:
            max_left_sum = current_sum
            max_left_idx = i
        elif current_sum == max_left_sum:
            if i > max_left_idx:
                max_left_idx = i

    max_right_sum = arr[mid + 1]
    max_right_idx = mid + 1
    current_sum = 0

    for j in range(mid + 1, high + 1):
        current_sum += arr[j]
        if current_sum > max_right_sum:
            max_right_sum = current_sum
            max_right_idx = j
        elif current_sum == max_right_sum:
            if j < max_right_idx:
                max_right_idx = j

    crossing_sum = max_left_sum + max_right_sum
    return crossing_sum, max_left_idx, max_right_idx


def _max_subarray_dc_rec(arr: List[int], low: int, high: int) -> Tuple[int, int, int]:
    if low == high:
        return arr[low], low, high

    mid = (low + high) // 2

    left_sum, left_start, left_end = _max_subarray_dc_rec(arr, low, mid)
    right_sum, right_start, right_end = _max_subarray_dc_rec(arr, mid + 1, high)
    cross_sum, cross_start, cross_end = _find_max_crossing_subarray(arr, low, mid, high)

    best_sum, best_start, best_end = left_sum, left_start, left_end

    if _tie_break(right_sum, right_start, right_end, best_sum, best_start, best_end):
        best_sum, best_start, best_end = right_sum, right_start, right_end

    if _tie_break(cross_sum, cross_start, cross_end, best_sum, best_start, best_end):
        best_sum, best_start, best_end = cross_sum, cross_start, cross_end

    return best_sum, best_start, best_end


def max_subarray_divide_conquer(arr: List[int]) -> Tuple[int, int, int]:
    n = len(arr)
    if n == 0:
        raise ValueError("O vetor não pode ser vazio.")
    return _max_subarray_dc_rec(arr, 0, n - 1)


def max_subarray_kadane(arr: List[int]) -> Tuple[int, int, int]:
    n = len(arr)
    if n == 0:
        raise ValueError("O vetor não pode ser vazio.")

    best_sum = arr[0]
    best_start = 0
    best_end = 0

    current_sum = arr[0]
    current_start = 0

    for i in range(1, n):
        x = arr[i]
        if current_sum <= 0:
            current_sum = x
            current_start = i
        else:
            current_sum += x

        if _tie_break(current_sum, current_start, i, best_sum, best_start, best_end):
            best_sum = current_sum
            best_start = current_start
            best_end = i

    return best_sum, best_start, best_end
