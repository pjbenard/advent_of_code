from tqdm import tqdm


def parse_data(data):
    diskmap = list(map(int, data[0]))
    fullmap = []
    for id_block, len_block in enumerate(diskmap):
        if id_block % 2:
            fullmap.extend([-1] * len_block)
        else:
            fullmap.extend([id_block // 2] * len_block)

    return diskmap, fullmap


def swap(list_vals, id1, id2):
    temp = list_vals[id1]
    list_vals[id1] = list_vals[id2]
    list_vals[id2] = temp


def swap_mulindex(list_vals, ids1, ids2):
    for id1, id2 in zip(ids1, ids2):
        swap(list_vals, id1, id2)


def checksum(fullmap):
    SUM = sum(id * val for id, val in enumerate(fullmap) if val > 0)
    return SUM


def part1(data):
    diskmap, fullmap = parse_data(data)

    id_freespace = 0  # fullmap.index(-1)
    id_block = len(fullmap) - 1

    while id_freespace < id_block:
        if fullmap[id_freespace] > -1:
            id_freespace += 1
            continue

        if fullmap[id_block] < 0:
            id_block -= 1
            continue

        swap(fullmap, id_freespace, id_block)
        id_freespace += 1
        id_block -= 1

    return checksum(fullmap)


def part2(data):
    diskmap, fullmap = parse_data(data)

    blocks = []
    id_block_fullmap = 0
    for len_block in diskmap:
        tuple_id_len = (id_block_fullmap, len_block)
        blocks.append(tuple_id_len)
        id_block_fullmap += len_block

    for file_block in tqdm(blocks[::-2]):
        id_file, len_file = file_block
        for id_freespace, freespace_block in enumerate(blocks[1::2]):
            id_fp_fullmap, len_freespace = freespace_block
            if len_freespace == 0:
                continue
            elif id_fp_fullmap > id_file:
                break
            elif len_file <= len_freespace:
                range_freespace = range(id_fp_fullmap, id_fp_fullmap + len_file)
                range_file = range(id_file, id_file + len_file)
                swap_mulindex(fullmap, range_freespace, range_file)
                blocks[id_freespace * 2 + 1] = (
                    id_fp_fullmap + len_file,
                    len_freespace - len_file,
                )
                break

    return checksum(fullmap)


if __name__ == "__main__":
    with open("2024/data/09_test.txt") as file:
        data = file.read().splitlines()
    diskmap, fullmap = parse_data(data)
    print(diskmap)
    print(fullmap)

    blocks = []
    id_block_fullmap = 0
    for len_block in diskmap:
        tuple_id_len = (id_block_fullmap, len_block)
        blocks.append(tuple_id_len)
        id_block_fullmap += len_block
    print(blocks)

    for file_block in tqdm(blocks[::-2]):
        id_file, len_file = file_block
        for id_freespace, freespace_block in enumerate(blocks[1::2]):
            id_fp_fullmap, len_freespace = freespace_block
            if len_freespace == 0:
                continue
            if id_fp_fullmap > id_file:
                break
            if len_file <= len_freespace:
                print(file_block, freespace_block)
                print(fullmap[id_file : id_file + len_file])
                range_freespace = range(id_fp_fullmap, id_fp_fullmap + len_file)
                range_file = range(id_file, id_file + len_file)
                swap_mulindex(fullmap, range_freespace, range_file)
                blocks[id_freespace * 2 + 1] = (
                    id_fp_fullmap + len_file,
                    len_freespace - len_file,
                )
                print(fullmap)
                break

    # print(fullmap)
    print(checksum(fullmap))
