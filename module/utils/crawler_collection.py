
import re
import requests
from bs4 import BeautifulSoup


class Typing_DNA():

    def __init__(self):
        self._initialize()

    def _initialize(self):    
        self.index_url = "https://www.typingdna.com/demo/anytext/index"
        self.enroll_url = "https://www.typingdna.com/demo/anytext/enroll"
        self.session_id = requests.get(self.index_url).cookies["connect.sid"]

    def crawl(self):

        index_url = self.index_url
        enroll_url = self.enroll_url
        session_id = self.session_id

        cookies = {'connect.sid': session_id}
        response = requests.get(enroll_url, cookies=cookies)

        if response.history:
            self._initialize()
            session_id = self.session_id
            data = {'username': 'fooooo'}
            cookies = {'connect.sid': session_id}
            response = requests.post(index_url, data=data, cookies=cookies)

        bs = BeautifulSoup(response.text, "lxml")
        docs = [re
                .compile(".*currentQuote = '(.+)'.*")
                .findall(bs.select("script")[-1].text)[0]]
        return docs


def get_naver_web_novel(novel_id, volume_no):

    response = requests.get(
        "http://novel.naver.com/webnovel/detail.nhn?novelId=%d&volumeNo=%d"
        % (novel_id, volume_no)
    )

    bs = BeautifulSoup(response.text, "lxml")
    sens = bs.select(".detail_view_content > p")
    sens = [con.text for con in sens]
    doc = ' '.join(sens)
    docs = [doc]

    return docs
