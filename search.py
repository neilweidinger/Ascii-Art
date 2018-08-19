def binarySearch(ray, target):
    l = 0
    r = len(ray) - 1

    while l <= r:
        m = int((l + r) / 2)

        if ray[m] > target:
            r = m - 1
        elif ray[m] < target:
            l = m + 1
        else:
            return m

    return -1

def leftmost(ray, target):
    l = 0
    r = len(ray)

    while l < r:
        m = int((l + r) / 2)
        # print("ray[{}]: {}".format(m, ray[m]))
        # print("l: {}\t r:{}".format(l, r))
        if ray[m] < target:
            l = m + 1
        else:
            r = m

    return l - 1

def rightmost(ray, target):
    l = 0
    r = len(ray)

    while l < r:
        m = int((l + r) / 2)
        # print("ray[{}]: {}".format(m, ray[m]))
        # print("l: {}\t r:{}".format(l, r))
        if ray[m] > target:
            r = m
        else:
            l = m + 1

    return l

if __name__ == "__main__":
    nums = [1, 2, 3, 4, 7, 8, 10, 11, 13, 14, 15, 21]
    target = 8

    print("exact: ")
    exact = binarySearch(nums, target)
    print("nums[{}] = {}".format(exact, nums[exact]))

    print("rightmost: ")
    right = rightmost(nums, target)
    print("nums[{}] = {}".format(right, nums[right]))

    print("leftmost: ")
    left = leftmost(nums, target)
    print("nums[{}] = {}".format(left, nums[left]))
