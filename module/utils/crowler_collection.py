
import re
import requests
from bs4 import BeautifulSoup


def get_en_docs():

    p = re.compile(".*currentQuote = '(.+)'.*")
    cookies = {
        "connect.sid":
        "s%3A5cEqMXHV4H_lFDKD4g6QUIJKTlvxgsUJ.VFLCj0jDxwzL9aVHZ50fvGV5eMp2vtA6j9NDGWD0Hds"
    }

    response = requests.get(
        "https://www.typingdna.com/demo/anytext/enroll",
         cookies=cookies
    )

    bs = BeautifulSoup(response.text, "lxml")
    doc = p.findall(bs.select("script")[-1].text)[0]
    docs = [doc]

    return docs


def get_ko_docs(novel_id, volume_no):

    response = requests.get(
        "http://novel.naver.com/webnovel/detail.nhn?novelId={}&volumeNo={}"
        .format(novel_id, volume_no)
    )

    bs = BeautifulSoup(response.text, "lxml")
    sens = bs.select(".detail_view_content > p")
    sens = [con.text for con in sens]
    sens = ' '.join(sens)
    doc = re.sub(r'\s+', ' ', sens)
    docs = [doc]

    return docs