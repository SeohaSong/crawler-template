import sys
import pandas as pd
import numpy as np
import os

from preprocess import get_sentences
from crowler_collection import get_en_docs, get_ko_docs


args = [
    {"novel_id": 673009, "volume_no": 1},
    {"novel_id": 673009, "volume_no": 2},
    {"novel_id": 673009, "volume_no": 3},
    {"novel_id": 673009, "volume_no": 4},
    {"novel_id": 676623, "volume_no": 1},
    {"novel_id": 676623, "volume_no": 2},
    {"novel_id": 676623, "volume_no": 3},
    {"novel_id": 676623, "volume_no": 4},
    {"novel_id": 699566, "volume_no": 1},
    {"novel_id": 699566, "volume_no": 2},
    {"novel_id": 699566, "volume_no": 3},
    {"novel_id": 699566, "volume_no": 4},
    {"novel_id": 693353, "volume_no": 1},
    {"novel_id": 693353, "volume_no": 2},
    {"novel_id": 693353, "volume_no": 3},
    {"novel_id": 693353, "volume_no": 4},
    {"novel_id": 657170, "volume_no": 1},
    {"novel_id": 657170, "volume_no": 2},
    {"novel_id": 657170, "volume_no": 3},
    {"novel_id": 657170, "volume_no": 4}
]


if __name__ == "__main__":


    i = 0
    total_ko_sens = []

    while not os.path.isfile("./data/ko_sens"):

        try:
            docs = get_ko_docs(**args[i])
            i += 1
        except:
            continue
        
        sens = sum([get_sentences(doc, "ko", [160, 180]) for doc in docs], [])
        total_ko_sens += sens

        total_len = len(set(total_ko_sens))
        sys.stdout.write("\r% 4d | % 4d" % (i, total_len))
        
        if total_len >= 1000:
            np.random.seed(1050554145)
            idxs = np.random.choice(total_len, 1000, replace=False)
            total_ko_sens = list(set(total_ko_sens))
            total_ko_sens = np.array(total_ko_sens)[idxs]
            total_ko_sens = total_ko_sens.tolist()
            pd.to_pickle(total_ko_sens, "./data/ko_sens")


    i = 0
    total_en_sens = []

    while not os.path.isfile("./data/en_sens"):

        try:
            docs = get_en_docs()
            i += 1
        except:
            continue
        
        sens = sum([get_sentences(doc, "en", [160, 180]) for doc in docs], [])
        total_en_sens += sens

        total_len = len(set(total_en_sens))
        sys.stdout.write("\r% 4d | % 4d" % (i, total_len))
        
        if total_len >= 1000:
            total_en_sens = list(set(total_en_sens))
            pd.to_pickle(total_en_sens, "./data/en_sens")
