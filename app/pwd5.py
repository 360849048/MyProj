MASK_TABLE = [
 [1, 8, 4, 2, 3],
 [7, 3, 5, 4, 2],
 [3, 6, 4, 8, 5],
 [4, 2, 7, 6, 0],
 [3, 2, 4, 9, 7],
 [6, 7, 5, 1, 3],
 [9, 5, 6, 7, 8],
 [3, 0, 2, 4, 1],
 [4, 6, 1, 2, 3],
 [6, 1, 7, 8, 5]
]

KEY_TABLE = [
 [101, 112, 4, 1, 110, 2, 5, 99, 3, 6],
 [8, 110, 2, 106, 1, 105, 5, 103, 4, 8],
 [104, 6, 106, 9, 7, 102, 4, 107, 0, 8],
 [4, 107, 104, 1, 103, 0, 1, 111, 7, 2],
 [9, 106, 2, 8, 105, 8, 2, 9, 6, 1],
 [101, 1, 103, 2, 6, 1, 109, 1, 7, 8],
 [98, 8, 2, 1, 7, 105, 5, 6, 99, 4],
 [99, 5, 3, 102, 9, 112, 8, 111, 4, 7],
 [3, 7, 107, 5, 104, 6, 1, 0, 7, 7],
 [2, 108, 100, 105, 7, 0, 101, 109, 5, 8]
]


def createPwd5(random_codes):
    if type(random_codes) != str:
        random_codes = str(random_codes)
    if len(random_codes) != 10:
        raise Exception('The length of "random_codes" must be 10')
    last_random = int(random_codes[-1])
    mask_array = MASK_TABLE[int(random_codes[last_random])]
    rotate_left_num = mask_array[-1]

    rand_cover = []
    for i in range(10):
        rand_cover.append(KEY_TABLE[i][int(random_codes[i])])
        if rand_cover[i] <= 9:
            rand_cover[i] += 48

    key_input_temp = rand_cover.copy()
    for i in range(rotate_left_num):
        key_input_temp.append(key_input_temp.pop(0))

    key_input = ""
    for i in range(10):
        key_input += chr(key_input_temp[i])

    return key_input


if __name__ == '__main__':
    # Test
    print(createPwd5("7103601446"))
