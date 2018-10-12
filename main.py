import sys
import pandas as pd
import numpy as np
import os

from module.utils.preprocessor import get_sentences
from module.utils.text_collection import get_korea_sat_nonliteral
from module.utils.crawler_collection import get_naver_web_novel
from module.utils.crawler_collection import Typing_DNA
from module.dic_converter import convert2xml


def set_test(ids):


    def get_experiments(id_, name):

        nonlocal name2type, name2path, name2size

        type_ = name2type[name]
        path = name2path[name]
        size = name2size[name]
        if path:
            datas = np.random.choice(pd.read_pickle(path), size, replace=False)
        else:
            datas = [""]*size
        challenges = [{"challenge type='"+type_+"'": data} for data in datas]
        experiments = [{"experiment name='"+name+"-"+id_+"'": challenges}]

        return experiments


    name2path = {
        "key-ko": "./data/key-ko",
        "key-en": "./data/key-en",
        "sig-ko": None,
        "sig-en": None,
        "sig-fi": None,
    }
    name2type = {
        "key-ko": "keyboard",
        "key-en": "keyboard",
        "sig-ko": "signature",
        "sig-en": "signature",
        "sig-fi": "signature",
    }
    name2size = {
        "key-ko": 30,
        "key-en": 30,
        "sig-ko": 300,
        "sig-en": 300,
        "sig-fi": 300,
    }


    np.random.seed(0)
    experiments = sum(
        [get_experiments(id_, name) for id_ in ids for name in name2path], []
    )
    arrdic = [{"configure": experiments}]
    bs = convert2xml(arrdic)
    
    with open("./data/config.xml", "w") as f:
        f.write(str(bs))


if __name__ == "__main__":

    # # 2005~2010년 비문학 지문 (6월 모평, 9월 모평, 수능)
    # # 구르미 그린 달빛 - 윤이수 (무료 공개본)
    # # 르네 마그리트의 연인 - 유지나 (무료 공개본)

    # args = [
    #     {"novel_id": id_, "volume_no": no+1}
    #     for id_, max_no in [
    #         (126772, 7),
    #         (494460, 9),
    #     ]
    #     for no in range(max_no)
    # ]

    # i = 0
    # total_ko = []
    # while True:
    #     try:
    #         if not i:
    #             docs = get_korea_sat_nonliteral()
    #         else:
    #             docs = get_naver_web_novel(**args[i-1])
    #         i += 1
    #     except:
    #         continue
    #     sens = sum([get_sentences(doc, "ko", [160, 200]) for doc in docs], [])
    #     total_ko += sens
    #     total_len = len(set(total_ko))
    #     sys.stdout.write("\r% 4d | % 4d" % (i, total_len))
    #     if total_len >= 750:
    #         total_ko = list(set(total_ko))[:750]
    #         pd.to_pickle(total_ko, "./data/key-ko")
    #         print()
    #         break


    # i = 0
    # total_en_sens = []
    # site = Typing_DNA()
    # while True:
    #     try:
    #         docs = site.crawl()
    #         i += 1
    #     except:
    #         continue
    #     sens = sum([get_sentences(doc, "en", [160, 200]) for doc in docs], [])
    #     total_en_sens += sens
    #     total_len = len(set(total_en_sens))
    #     sys.stdout.write("\r% 4d | % 4d" % (i, total_len))
        
    #     if total_len >= 750:
    #         total_en_sens = list(set(total_en_sens))[:750]
    #         pd.to_pickle(total_en_sens, "./data/key-en")
    #         print()
    #         break


    ids = [str(i+1) for i in range(50)]
    set_test(ids)


