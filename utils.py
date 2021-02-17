import numpy as np


def split_receivers(receivers, senders):
    count_for_sender = int(len(receivers) / len(senders))
    chunk_count = int(len(receivers) / count_for_sender)
    chunked_receivers = np.array_split(receivers, chunk_count)

    return {s: r.tolist() for s, r in zip(senders, chunked_receivers)}

