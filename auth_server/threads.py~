#{'learn':name,'check':id,'diff':-1,'s1':-1,'s2':-1,'report':'wrong learing set!','error':False}

import threading,traceback

#from fingerprint.pyltp_cut import *
from fingerprint.jieba_cut import *
from fingerprint.synonyms import *
from fingerprint.clustering import *
from visualization.makefig import *

class CalcThread(threading.Thread):
    def __init__(self,inqueue,visualQueue,db,dbMutex):
        threading.Thread.__init__(self)
        self.inqueue=inqueue
        self.visualQueue=visualQueue
        self.db=db
        self.dbMutex=dbMutex

    def run(self):
        while True:
            try:
                request=self.inqueue.get()
                id,article=request
                try:
                    url,title,content=article['url'],article['title'],article['content']
                    wordlist=get_real_words(content)
                except BaseException as e:
                    with self.dbMutex:
                        self.db.put_result(id)
                        record=self.db.get_result(id)
                        record.ifFailed=True
                        record.exeInfo='Parse article content failed.\n'+str(e)
                        continue

                try:
                    _,_,strvir,ldavec, glovevec, symvec, fingerprint=get_fingerprint_vectors(id,content)
                except BaseException as e:
                    print('Get fingerprint failed.\n'+str(e))
                    traceback.print_exc()
                    with self.dbMutex:
                        self.db.put_result(id)
                        record=self.db.get_result(id)
                        record.ifFailed=True
                        record.exeInfo='Get fingerprint failed.\n'+str(e)
                        continue

                with self.dbMutex:
                    self.db.put_result(id,title,url,content,wordlist,fingerprint)

                recommend=get_recommend(fingerprint)
                with self.dbMutex:
                    (self.db.get_result(id)).recommend=recommend

                stopwordPAddr=TARGET_IMG_DIR+str(id)+'stopword.jpg'
                stopwordImgResult=create_wordcloud(strvir,stopwordPAddr)

                realwordPAddr=TARGET_IMG_DIR+str(id)+'realword.jpg'
                realwordImgResult=create_wordcloud(wordlist,realwordPAddr)

                ldaPAddr=TARGET_IMG_DIR+str(id)+'lda.jpg'
                ldaImgReuslt=create_vector_graph(ldavec,ldaPAddr)

                glovePAddr=TARGET_IMG_DIR+str(id)+'glove.jpg'
                gloveImgResult=create_vector_graph(glovevec,glovePAddr)

                sym2PAddr=TARGET_IMG_DIR+str(id)+'sym2.jpg'
                sym2ImgResult=create_vector_graph(symvec,sym2PAddr)

                fingerprintPAddr=TARGET_IMG_DIR+str(id)+'fingerprint.jpg'

                fingerprint2=deepcopy(fingerprint)
                normalize(fingerprint2)

                fingerprintImgResult=create_vector_graph(fingerprint2,fingerprintPAddr)

                with self.dbMutex:
                    record=self.db.get_result(id)
                    if stopwordImgResult==0:
                        record.stopwordPic=stopwordPAddr
                    if realwordImgResult == 0:
                        record.realwordPic=realwordPAddr
                    if ldaImgReuslt==0:
                        record.ldaPic=ldaPAddr
                    if gloveImgResult == 0:
                        record.glovePic=glovePAddr
                    if sym2ImgResult == 0:
                        record.symVectorPic=sym2PAddr
                    if fingerprintImgResult == 0:
                        record.fingerprintPic=fingerprintPAddr

            except BaseException as e:
                print('ERROR: Something went wrong in thread, info: ',str(e))



