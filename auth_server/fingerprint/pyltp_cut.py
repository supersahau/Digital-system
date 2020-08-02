from pyltp import Segmentor,Postagger
from fingerprint.common import *
CWS_MODEL_PATH='/home/hiro/ltp_data_v3.4.0/cws.model'
POS_MODEL_PATH='/home/hiro/ltp_data_v3.4.0/pos.model'


segmentor = Segmentor()
segmentor.load(CWS_MODEL_PATH)

postagger = Postagger()
postagger.load(POS_MODEL_PATH)
print("pyltp model loaded.")

def get_real_words(str1):

    words=segmentor.segment(str1)
    postags = postagger.postag(words)
    wordlist=[(words[i],postags[i]) for i in range(0,len(words))]

    punc = open(PUNC_DIR, 'rb')
    pr = punc.read()
    pr = pr.decode('gbk')
    p = pr.split()
    lreal = []

    passlist = ['\\', "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", '/', '-', '$', '#']

    for word in wordlist:
        if word[0] in passlist:
            pass
        elif word[1] in ['n', 'v', 'a'] and word[0] not in p:
            lreal.append(word[0])

    strreal = " ".join(lreal)
    return strreal
