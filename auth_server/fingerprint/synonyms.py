import pickle
import numpy as np
from sklearn.decomposition import PCA
from copy import deepcopy

from fingerprint.common import *

ARTICLE_ID=0
LEARN_NAME=1
TITLE=2
URL=3
ARTICLE_WORD_LIST=4


################################init
dict=get_dict()
class_dict0 = make_class_dict(dict)
#pass_dict=get_pass_dict()
class_member_dict=make_class_member_dict(dict)

vector_class=[]

with open(CLASS_RANKING_ADDR, 'r') as f:
    lines = f.readlines()

records = []
for line in lines:
    line = line.split()
    record = [line[0], float(line[1][3:]), int(line[2][4:])]
    records.append(record)

records = sorted(records, key=lambda tuple: tuple[1], reverse=True)

for record in records:
    className=record[0]
    vector_class.append(className)

dataset_dict={}
for learn_set in database:
    with open(CUT_FILE_DIR + learn_set + '.txt') as file1:
        wordlist = file1.read().split()
    dataset_dict[learn_set]=wordlist

with open(PCA_MODEL_ADDR,'rb') as modelfile:
    pca=pickle.loads(modelfile.read())

#######################################

class WrongLearingSetError(BaseException):
    pass




def run(learnlist,checklist):
    counterl={}
    counterc={}
    class_dict=deepcopy(class_dict0)

    for word in learnlist:
        if word not in dict:
            pass
        else:
            record=dict[word]

            current_class=record[CLASS]

            if current_class not in counterl:
                counterl[current_class]=[current_class,{word:1},1]
                continue
            else:
                if word in counterl[current_class][WORD_COUNTER_DICT]:
                    counterl[current_class][WORD_COUNTER_DICT][word] += 1
                else:
                    counterl[current_class][WORD_COUNTER_DICT][word] = 1

                counterl[current_class][SUM_OF_CLASS]+=1

    for word in checklist:
        if word not in dict:
            pass
        else:
            record = dict[word]

            current_class = record[CLASS]

            if current_class not in counterc:
                counterc[current_class] = [current_class, {word: 1}, 1]
                continue
            else:
                if word in counterc[current_class][WORD_COUNTER_DICT]:
                    counterc[current_class][WORD_COUNTER_DICT][word] += 1
                else:
                    counterc[current_class][WORD_COUNTER_DICT][word] = 1

                counterc[current_class][SUM_OF_CLASS] += 1

    common_class={}

    for aClass in counterl:
        if aClass in counterc:
            common_class[aClass]=True

    difference=0
    sum=0

    for aClass in common_class:
        difference_counter={}
        class_record_l=counterl[aClass]
        word_counter_dict_l=class_record_l[WORD_COUNTER_DICT]

        class_record_c = counterc[aClass]
        word_counter_dict_c=class_record_c[WORD_COUNTER_DICT]

        for aWord in word_counter_dict_l:
            difference_counter[aWord]=True

        for aWord in word_counter_dict_c:
            difference_counter[aWord]=True

        for aWord in difference_counter:
            sum+=1

            if aWord in word_counter_dict_l:
                ratio1=word_counter_dict_l[aWord]/class_record_l[SUM_OF_CLASS]
            else:
                ratio1=0

            if aWord in word_counter_dict_c:
                ratio2 = word_counter_dict_c[aWord] / class_record_c[SUM_OF_CLASS]
            else:
                ratio2 = 0

            if not ratio1:
                appear='只有文章中使用了'
            elif not ratio2:
                appear='只有公众号使用了'
            else:
                appear='两者都用了'

            abs=ratio1-ratio2 if ratio1>=ratio2 else ratio2-ratio1

            class_dict[aClass][CLASS_PARTICIPATION]+=abs

            class_dict[aClass][MEMBERS]+=appear+aWord+';'

            difference+=abs

    if sum!=0:
        return difference/sum,sum,len(common_class),class_dict
    else:
        return 0,sum,len(common_class),class_dict


def cmp_article(id,learn_set,title,url,wordlist):

    try:
        list1 = dataset_dict[learn_set]
    except:
        raise WrongLearingSetError
    else:

        list2=wordlist

        index, sum1, sum2, class_dict = run(list1, list2)

        sorted_class = []
        for key in class_dict:
            class_record = class_dict[key]
            sorted_class.append(
                (key, class_record[CLASS_PARTICIPATION], class_record[DIMENSION], class_record[MEMBERS]))

        sorted_class = sorted(sorted_class, key=lambda tuple: tuple[1], reverse=True)

        report={}
        report['learn'],report['check'],report['url']=learn_set,str(id),url
        report['dif'],report['s1'],report['s2']=str(index),str(sum1),str(sum2)

        result = '\tlearn:' + learn_set + ' check '+title+'     \t Result: \t' + str(index) + ' \t' + str(
            sum1) + ' \t' + str(sum2)+'\n   URL: '+url

        print(result)

        wordAnalysis=[]
        l = 0
        for k in sorted_class:
            if l <= 10:
                if k[1]:
                    wordAnalysis.append( {"class":k[0],"d":str(k[2]),"pt":str(k[1]),"diff":k[3]})
                    l += 1
            else:
                break

        report['wordanalysis']=wordAnalysis
        report['error']=False

        return report

def get_vector(dict,class_member_dict,countDict,dimension=1000):
    vector=[]

    i=0
    for className in vector_class:
        try:
            wordCounter=countDict[className][WORD_COUNTER_DICT]
        except:
            class_record=class_member_dict[className]
            for j in range(0,len(class_record)):
                vector.append(0)
                i+=1
                if i >= dimension: break
        else:
            classSum=countDict[className][SUM_OF_CLASS]
            for wordName in class_member_dict[className]:
                try:
                    wordSum=wordCounter[wordName]
                except:
                    wordSum=0

                i+=1
                vector.append(wordSum/classSum)
                if i>=dimension: break

        if i>=dimension: break
    return vector

def run_single(wordList,dict):
    counterl = {}

    for word in wordList:
        if word not in dict:
            pass
        else:
            record = dict[word]

            current_class = record[CLASS]

            if current_class not in counterl:
                counterl[current_class] = [current_class, {word: 1}, 1]
                continue
            else:
                if word in counterl[current_class][WORD_COUNTER_DICT]:
                    counterl[current_class][WORD_COUNTER_DICT][word] += 1
                else:
                    counterl[current_class][WORD_COUNTER_DICT][word] = 1

                counterl[current_class][SUM_OF_CLASS] += 1

    return counterl

def get_fingerprint_slice(reall):
    countDict = run_single(reall, dict)
    vector = get_vector(dict, class_member_dict, countDict, 3000)

    array=np.array(vector)
    ddarray=np.array([array])
    new_vector=pca.transform(ddarray)

    return new_vector[0]