import pickle

ROOT_DIR='fingerprint/'

# CHK_ARTICLE_REPORT_DIR=ROOT_DIR+'data/result/chk_article/'
# CUT_FILE_DIR=ROOT_DIR+'data/cut/'
# CUT_DATASET_FILE=ROOT_DIR+'data/pickle/cut_dataset.pickle'

CHK_ARTICLE_REPORT_DIR=ROOT_DIR+'data/result/chk_article_hit/'
CUT_FILE_DIR=ROOT_DIR+'data/cut_hit/'
CUT_DATASET_FILE=ROOT_DIR+'data/pickle/cut_dataset_hit.pickle'
DICT_PICKLE_ADDR=ROOT_DIR+'data/pickle/dict.pickle'
PASSDICT_PICKLE_ADDR=ROOT_DIR+'data/pickle/pass_dict.pickle'
PCA_MODEL_ADDR=ROOT_DIR+'data/pickle/model.pickle'

HLP_LL_ADDR=ROOT_DIR+'data/knowledge/hlp_ll.txt'
PUNC_ADDR=ROOT_DIR+'data/knowledge/punctuation.txt'
CLASS_RANKING_ADDR=ROOT_DIR+'data/knowledge/classes.txt'

VECTOR_DATABASE_ADDR=ROOT_DIR+'data/knowledge/vectordatabase.txt'
ENCODER_MODEL_ADDR=ROOT_DIR+'data/knowledge/encoderModel.h5'
NEW_ARTICLE_CACHE_DIR=ROOT_DIR+'newArticleCache/'
LDA_MODEL_ADDR=ROOT_DIR+'data/knowledge/ldamodel.txt'
LDA_ORIGIN_VC_ADDR=ROOT_DIR+'data/knowledge/ldaoriginvc.txt'
GLOVE_SAVE_ADDR=ROOT_DIR+'data/knowledge/gloveSave.txt'
TFIDF_VECTO_ADDR=ROOT_DIR+'data/knowledge/tfidf_vecto.txt'
IFIDF_TRANSF_ADDR=ROOT_DIR+"data/knowledge/ifidf_transf.txt"

TARGET_IMG_DIR='static/img/'

ACCOUNT_ICO_DIR='static/ico/'

WORD=0
CLASS=1
NO=2
CLASS_SUM=3

CURRENT_CLASS=0
WORD_COUNTER_DICT=1
SUM_OF_CLASS=2

CLASS_PARTICIPATION=0
DIMENSION=1
MEMBERS=2

Q=0
R=1
S=2

#这个列表存储目标CSV文件的名称。要添加新的文件，只需加在此处。
database=['dsjwz.csv','gkw.csv','jqzx.csv','ktx.csv','mm.csv','xkd.csv','xsx.csv']

#这个函数返回上述被pickle的字典
def get_cut_dataset():
    with open(CUT_DATASET_FILE,'rb') as dumpfile:
        cut_dataset=pickle.load(dumpfile)
    return cut_dataset

def get_dict():
    with open(DICT_PICKLE_ADDR,'rb') as pfile:
        dict=pickle.load(pfile)

    return dict

def get_pass_dict():
    with open(PASSDICT_PICKLE_ADDR,'rb') as pfile:
        dict=pickle.load(pfile)

    return dict

def make_class_dict(dict):
    class_dict={}
    for word in dict:
        current_class=dict[word][CLASS]
        if current_class not in class_dict:
            class_dict[current_class]=[0,1,''] #class_participation, sum_of_class_member
        else:
            class_dict[current_class][DIMENSION]+=1

    return class_dict

def make_class_member_dict(dict):
    class_member_dict={}
    for word in dict:
        current_class=dict[word][CLASS]
        if current_class not in class_member_dict:
            class_member_dict[current_class]=[word]
        else:
            (class_member_dict[current_class]).append(word)
    return class_member_dict


def kanji_to_set(str):
    if str=='机器之心':
        return 'jqzx.csv'
    elif str=='大数据文摘':
        return 'dsjwz.csv'
    elif str=='果壳网':
        return 'gkw.csv'
    elif str== 'Vista看天下':
        return 'ktx.csv'
    elif str=='咪蒙':
        return 'mm.csv'
    elif str=='侠客岛':
        return 'xkd.csv'
    elif str=='新世相':
        return 'xsx.csv'
    else:
        return str

def set_to_kanji(str):
    if str=='jqzx.csv':
        return '机器之心'
    elif str=='dsjwz.csv':
        return '大数据文摘'
    elif str=='gkw.csv':
        return '果壳网'
    elif str== 'ktx.csv':
        return 'Vista看天下'
    elif str=='mm.csv':
        return '咪蒙'
    elif str=='xkd.csv':
        return '侠客岛'
    elif str=='xsx.csv':
        return '新世相'
    else:
        return str

def normalize(vec):
    minimum = 100
    maximum = -100
    for item in vec:
        if item < minimum:
            minimum = item
        if item > maximum:
            maximum = item
    for i in range(len(vec)):
        vec[i] = 0.01 + 0.99 * (vec[i] - minimum) / (maximum - minimum)
    # print(vec)
    return


class OpenURLException(Exception):
    pass
class ParseException(Exception):
    pass

class TODOException(Exception):
    def __init__(self,*args,**kwargs):
        Exception.__init__(self)
        self.args=('ERROR','You forgot to do something.')