
import re

from .chr_handler import convert2typing


def _preprocess_all_pre(text):
    text = re.sub(r'^\s*[.,]', '', text)
    text = re.sub(r'[\u2018\u2019\u201c\u201d\'\"]', '', text)
    text = re.sub(r'.*[0-9].*', '', text)
    text = re.sub(r'.*[^\w,. ].*', '', text)
    return text

def _preprocess_all_pos(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'^ ', '', text)
    text = re.sub(r' $', '', text)
    return text

def _preprocess_ko(text):
    text = _preprocess_all_pre(text)
    text = re.sub(r'.*[a-zA-Zㄱ-ㅎㅏ-ㅣ].*', '', text)
    text = re.sub(r'.*(.+?)\1{2}.*', '', text)
    text = re.sub(r'[^가-힣., ]', '', text)
    text = _preprocess_all_pos(text)
    return text

def _preprocess_en(text):
    text = _preprocess_all_pre(text)
    text = re.sub(r'[^a-zA-Z.,\' ]', '', text)
    text = _preprocess_all_pos(text)
    return text


def get_sentences(doc, language, range_):

    min_, max_ = range_
    if language == 'ko':
        preprocess = _preprocess_ko
    elif language == 'en':
        preprocess = _preprocess_en
    
    sens = doc
    sens = re.compile(r'.*?[.,]').findall(sens)
    sens = [preprocess(text) for text in sens]

    esc_idxs = []
    good_sens = []
    for i in range(len(sens)):
        cum_sen, cum_length = '', 0
        esc_idx_buffer = []
        for i_, sen in enumerate(sens[i:i+3]):
            if not sen:
                esc_idxs.append(i+i_)
            if (i+i_ in esc_idxs) or (cum_length > 180):
                cum_sen = ''
                esc_idx_buffer = []
            cum_sen = cum_sen+sen
            esc_idx_buffer.append(i_)
            cum_sen = re.sub(r'\.', '. ', cum_sen)
            cum_sen = re.sub(r',', ', ', cum_sen)
            cum_sen = re.sub(r'\s+', ' ', cum_sen)
            cum_sen = re.sub(r'^ ', '', cum_sen)
            cum_sen = re.sub(r' $', '', cum_sen)
            cum_length = len(convert2typing(cum_sen))
            if (min_ <= cum_length <= max_) and cum_sen[-1] == ".":
                good_sens.append(cum_sen)
                cum_sen = ''
                for i_ in esc_idx_buffer:
                    esc_idxs.append(i+i_)
    good_sens = list(set(good_sens))
    
    return good_sens