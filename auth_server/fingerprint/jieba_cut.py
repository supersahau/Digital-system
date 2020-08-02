import jieba.posseg
import csv
import pickle

from fingerprint.common import *



# 这个函数解析上述列表里的CSV文件，并返回一个字典。字典的键为上面列表里的名称，对应的值是每个csv文件的文章列表。
# 其中每一篇文章是一个元组：（num,url,title,content）
def make_original_dataset():
    original_dataset={}

    for acsv in database:
        original_dataset[acsv]=[]

        with open(ROOT_DIR+'data/'+acsv) as csvfile:
            reader=csv.DictReader(csvfile)
            for aline in reader:
                (original_dataset[acsv]).append((aline['num'],aline['url'],aline['title'],aline['content']))

    return original_dataset

#这个函数将哈工大同义词林转换为一个python字典，并返回。
def make_dict():

    wordlist = open(HLP_LL_ADDR, 'rb').readlines()

    decodedwl = []

    dict = {}

    for line in wordlist:
        decodedwl.append(line.decode("GBK"))

    father = ''
    for line in decodedwl:
        if '=' in line:
            line = line.split(" ")[1:]
            line[-1] = line[-1][:-2]
            father = line[0]

            i = 0
            for word in line:
                dict[word] = [word, father, i]

    with open(DICT_PICKLE_ADDR,'wb') as pfile:
        pickle.dump(dict,pfile,2)

    print("Make dict success.")
    return True


#这个函数将传入字符串中的实词提取出，并返回包含这些实词的字符串，词以空格分隔。
def get_real_words(str1):
        seg = jieba.posseg.cut(str1)
        punc = open(PUNC_ADDR, 'rb')
        pr = punc.read()
        pr = pr.decode('gbk')
        p = pr.split()
        lreal = []
        lvir = []
        punclist = ["，", ",", "“", "”", "‘", "’", ".", "。", ":", "：", ";", "；", "！",
                    "!", "？", "?", "（", "）", "(", ")", '、', '——', '《', '》', '…', "……"]
        passlist = ['\\', "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", '/', '-', '$', '#']
        puncreplace = ["逗号", "逗号", "引号", "引号", "引号", "引号", "句号", "句号", "冒号",
                       "冒号", "分号", "分号", "感叹号", "感叹号", "问号", "问号", "括号",
                       "括号", "括号", "括号", '顿号', '破折号', '书名号', '书名号', '省略号', "省略号"]
        for i in seg:
            if i.word in passlist:
                pass
            elif i.word in punclist:
                for j in range(len(punclist)):
                    if i.word == punclist[j]:
                        lvir.append(puncreplace[j])
            elif i.flag in ['n', 'v', 'a'] and i.word not in p:
                lreal.append(i.word)
            # elif i.flag not in ['eng'] and i.word in p:
            #     lvir.append('填充' + i.word)
        strreal = " ".join(lreal)
        return strreal


init=jieba.posseg.cut('')

def prepare():
    make_dict()


#prepare()
