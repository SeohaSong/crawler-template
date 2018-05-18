
import re

from module.aws_handler import S3


def get_korea_sat_nonliteral():

    s3 = S3("seohasong", "./key/public-key.csv")
    data = s3.get_key("public/korea-sat/non-literal.txt")
    txt = data.decode("utf-8")

    part = r'(\[언어\]|\[사회\]|\[예술\]|\[과학\]|\[기술\]|\[인문\])' 
    groups = re.compile(r'(%(s)s)((.|\n)+?)(%(s)s)'%{"s": part}).findall(txt)
    docs = [g[2] for g in groups]

    return docs

def get_imdb():
    pass