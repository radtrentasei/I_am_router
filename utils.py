# utils.py
"""
Funzioni di utilità generiche, inclusa la generazione degli ID router.
"""
def generate_ids(size):
    ids = [None for _ in range(size*size)]
    group = 1
    for row in range(0, size, 2):
        for col in range(0, size, 2):
            for lrow in range(2):
                for lcol in range(2):
                    r = row + lrow
                    c = col + lcol
                    if r < size and c < size:
                        idx = r * size + c
                        global_id = idx + 1
                        local_id = lrow * 2 + lcol + 1
                        ids[idx] = {
                            "global_id": global_id,
                            "group_id": group,
                            "local_id": local_id
                        }
            group += 1
    return ids
