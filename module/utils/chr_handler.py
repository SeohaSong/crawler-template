
_pre = [
    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ',
    'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ',
    'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ',
    'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]
_mid = [
    'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ',
    'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
    'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ',
    'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
    'ㅣ'
]
_pos = [
    '',
    'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ',
    'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ',
    'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ',
    'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ',
    'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ',
    'ㅍ', 'ㅎ'
]

_chr2typing = {
    'ㅘ': 'ㅗㅏ',
    'ㅙ': 'ㅗㅐ',
    'ㅚ': 'ㅗㅣ',
    'ㅝ': 'ㅜㅓ',
    'ㅞ': 'ㅜㅔ',
    'ㅟ': 'ㅜㅣ',
    'ㅢ': 'ㅡㅣ',
    'ㅒ': '\u21e7ㅐ',
    'ㅖ': '\u21e7ㅔ',
    'ㅃ': '\u21e7ㅂ',
    'ㅉ': '\u21e7ㅈ',
    'ㄸ': '\u21e7ㄷ',
    'ㄲ': '\u21e7ㄱ',
    'ㅆ': '\u21e7ㅅ',
    'ㄳ': 'ㄱㅅ',
    'ㄵ': 'ㄴㅈ',
    'ㄶ': 'ㄴㅎ',
    'ㄺ': 'ㄹㄱ',
    'ㄻ': 'ㄹㅁ',
    'ㄼ': 'ㄹㅂ',
    'ㄽ': 'ㄹㅅ',
    'ㄾ': 'ㄹㅌ',
    'ㄿ': 'ㄹㅍ',
    'ㅀ': 'ㄹㅎ',
    'ㅄ': 'ㅂㅅ'
}

_pre_l, _mid_l, _pos_l = len(_pre), len(_mid), len(_pos)
_pivot = ord("가")
_ja = [chr(i) for i in range(ord('ㄱ'), ord('ㅎ')+1)]
_mo = [chr(i) for i in range(ord('ㅏ'), ord('ㅣ')+1)]
_uc = [chr(i) for i in range(ord("A"), ord("Z")+1)]
_lc = [chr(i) for i in range(ord("a"), ord("z")+1)]
_chr2typing.update({c: "\u21e7"+c.lower() for c in _uc})


def decompose(c):
    
    idx = ord(c)
    if not ord('가') <= idx <= ord('힣'):    
        return c
    
    idx = ord(c)-_pivot
    decomposed_c = (
        _pre[(idx) // _pos_l // _mid_l % _pre_l]
        +_mid[(idx) // _pos_l % _mid_l]
        +_pos[(idx) % _pos_l]
    )
    
    return decomposed_c


def convert2typing(word):
    word = ''.join([decompose(c) for c in word])
    typings = ''.join([_chr2typing[c] if c in _chr2typing
                       else c
                       for c in word])
    return typings