def match_fingerprints(fp1, fp2):
    offsets = {}

    hashes1 = [h1 for h1, _ in fp1]
    hashes2 = [h2 for h2, _ in fp2]

    for h1, t1 in fp1:
        for h2, t2 in fp2:
            if h1 == h2:
                diff = t1 - t2
                offsets[diff] = offsets.get(diff, 0) + 1

    if not offsets:
        return 0.0

    best_match = max(offsets.values())
    min_len = min(len(fp1), len(fp2)) if fp1 and fp2 else 1
    common_count = len(set(hashes1) & set(hashes2))
    common_ratio = common_count / min_len
    best_match_ratio = best_match / min_len

    return max(best_match_ratio, common_ratio * 0.9)
