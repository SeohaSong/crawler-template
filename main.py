import sys
import pandas as pd
import numpy as np
import os

from module.utils.preprocessor import get_sentences
from module.utils.crawler_collection import Typing_DNA
from module.utils.crawler_collection import get_naver_web_novel
from module.utils.text_collection import get_korea_sat_nonliteral
from module.dic_converter import convert2xml


def set_test(ids):

    name2path = {
        "ko": "./data/ko-sens",
        "en": "./data/en-sens",
        "sg": None
    }
    name2type = {
        "ko": "keyboard",
        "en": "keyboard",
        "sg": "signature"
    }
    name2size = {
        "ko": 100,
        "en": 100,
        "sg": 600
    }

    def get_experiments(id_, name):
        type_ = name2type[name]
        path = name2path[name]
        size = name2size[name]
        datas = (np.random.choice(pd.read_pickle(path), size) if path 
                 else [""]*size)
        challenges = [{"challenge type='"+type_+"'": data} for data in datas]
        experiments = [{"experiment name='"+name+"-"+id_+"'": challenges}]
        return experiments

    np.random.seed(1050554145)
    experiments = sum(
        [get_experiments(id_, name) for id_ in ids for name in name2path], []
    )
    arrdic = [{"configure": experiments}]
    bs = convert2xml(arrdic)
    
    with open("./data/config.xml", "w") as f:
        f.write(str(bs))


if __name__ == "__main__":


    # 2005~2010년 비문학 지문 (6월 모평, 9월 모평, 수능)
    # 구르미 그린 달빛 - 윤이수 (무료 공개본)
    # 해시의 신루 - 윤이수 (무료 공개본)
    # 저스티스 - 장호 (무료 공개본)
    # 휴거 1992 - 장호 (무료 공개본)
    # 르네 마그리트의 연인 - 유지나 (무료 공개본)

    args = [
        {"novel_id": id_, "volume_no": no+1}
        for id_, max_no in [
            (126772, 7),
            (398090, 4),
            (623314, 7),
            (583903, 5),
            (494460, 9)
        ]
        for no in range(max_no)
    ]

    i = 0
    total_ko_sens = []
    while not os.path.isfile("./data/ko-sens"):

        try:
            if not i:
                docs = get_korea_sat_nonliteral()
            else:
                docs = get_naver_web_novel(**args[i-1])
            i += 1
        except:
            continue
            
        sens = sum([get_sentences(doc, "ko", [160, 180]) for doc in docs], [])
        total_ko_sens += sens
        total_len = len(set(total_ko_sens))
        sys.stdout.write("\r% 4d | % 4d" % (i, total_len))
        
        if total_len >= 1000:
            total_ko_sens = list(set(total_ko_sens))[:1000]
            pd.to_pickle(total_ko_sens, "./data/ko-sens")
            print()


    # TypingDNA

    site = Typing_DNA()

    i = 0
    total_en_sens = []
    while not os.path.isfile("./data/en-sens"):

        try:
            docs = site.crawl()
            i += 1
        except:
            continue
        
        sens = sum([get_sentences(doc, "en", [160, 180]) for doc in docs], [])
        total_en_sens += sens
        total_len = len(set(total_en_sens))
        sys.stdout.write("\r% 4d | % 4d" % (i, total_len))
        
        if total_len >= 1000:
            total_en_sens = list(set(total_en_sens))[:1000]
            pd.to_pickle(total_en_sens, "./data/en-sens")
            print()


    ids = [
        "2017021201", 
        "2016010223",
        "2017020556",
        "2018020528"
    ]
    set_test(ids)
