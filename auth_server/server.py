import tornado.ioloop,tornado.web,tornado.escape
from queue import Queue
import threading,json
from tornado import gen
from threads import *

from spider import *
from db import *

from fingerprint.clustering import *
from fingerprint.synonyms import *

MAX_EXTHREAD_NUM=4

mainMutex=threading.Lock()
dbMutex=threading.Lock()

articleQueue=Queue()
visualQueue=Queue()


class MainStatus:
    def __init__(self):
        self.request_number=0

    def get_request_id(self):
        self.request_number+=1
        return self.request_number

    def get_request_number(self):
        return self.request_number

mainStatus=MainStatus()
mainDB=Database(1000)

calcThreadPool=[]
for i in range(0,MAX_EXTHREAD_NUM+1):
    new_thread=CalcThread(articleQueue,visualQueue,mainDB,dbMutex)
    new_thread.daemon=True
    calcThreadPool.append(new_thread)

class BaseHandler(tornado.web.RequestHandler):


    def write_error(self, status_code,**kwargs):
        self.finish("<html><title>%(code)d: %(message)s</title>"
                    "<body>%(code)d: %(message)s</body></html>" % {
                        "code": status_code,
                        "message": kwargs['content'] if 'content' in kwargs else '',
                    })

# class PostHandler(BaseHandler):
#     def get(self):
#         raise tornado.web.HTTPError(403)
#
#     def post(self):
#         try:
#             name,url=self.get_body_argument('name'),self.get_body_argument('url')
#             try:
#                 article=runspider(url)
#             except OpenURLError as e:
#                 self.write_error(500,content=e.msg)
#             else:
#                 with mainMutex:
#                     request_id=mainStatus.get_request_id()
#
#                 articleQueue.put((request_id,name,article))
#                 self.write(str(request_id))
#
#         except BaseException as e:
#             self.write_error(500,content=str(e.args))
#
# class GetHandler(BaseHandler):
#     def post(self):
#         self.write_error(403,content='403 Forbidden: \nYou should not post to here.')
#
#     def get(self):
#         if 'id' in self.request.arguments:
#             request_id=int(self.get_argument('id'))
#             with dbMutex:
#                 result=mainDB.get_result(request_id)
#
#             if result:
#                 result=json.dumps(result[ARTICLE_REPORT])
#                 self.write(result)
#             else:
#                 self.write_error(403,content='No Result')
#         else:
#             self.write_error(403,content="403 Forbidden:\nYou should provide an id in url")

class HomeHandler(BaseHandler):
    def get(self):
        self.write('Welcome!')

class PostURLHandler(BaseHandler):
    def get(self):
        self.write_error(403,content='403 Forbidden:\nYou should not get from this address.')

    def post(self, *args, **kwargs):
        try:
            url=self.get_body_argument('url')

            try:
                article=runspider(url)
            except OpenURLException:
                self.write_error(500,content="Failed to open URL.")
            except ParseException:
                self.write_error(500, content="Failed to parse article.")
            else:
                with mainMutex:
                    request_id=mainStatus.get_request_id()

                articleQueue.put((request_id,article))
                self.write(str(request_id))

        except BaseException as e:
            self.write_error(500,content='Not caught by inner except:\n'+str(e))

class IDvsAccountHandler(BaseHandler):
    def get(self):
        raise tornado.web.HTTPError(403)

    def post(self):
        try:
            account,rid=self.get_body_argument('account'),int(self.get_body_argument('id'))

            print('Get account name:',account)
            account=kanji_to_set(account)

            error=False
            fingerprint=None
            with dbMutex:
                record=mainDB.get_result(rid)
                if record==0:
                    title=''
                    url=''
                    wordlist=''
                    error=True
                else:
                    if record.ifFailed:
                        self.write_error(500,content='Request failed. info:'+record.exeInfo)
                        return
                    else:
                        title=record.title
                        url=record.url
                        wordlist=record.wordlist.split()
                        fingerprint = deepcopy(record.fingerprint)
            if error:
                self.write_error(404,content='id not found')
            else:
                similarity = get_sim(fingerprint, account)
                comment=cmp_article(rid,account,title,url,wordlist)

                response_json={'sim':similarity,'symsim':comment['dif'],'support':str(comment['s1'])+'of'+str(comment['s2']),'comment':comment['wordanalysis']}

                self.set_header("Content-Type", "application/json; charset=UTF-8")
                self.write(json.dumps(response_json))
        except WrongLearingSetError:
            self.write_error(404, content='Account not found.')
        except BaseException as e:
            self.write_error(500,content=str(e))

class AnalysisHandler(BaseHandler):
    def post(self):
        self.write_error(403,content='You should not post to this address')

    def get(self):
        try:
            rid,content=int(self.get_argument('id')),self.get_argument('content')
        except BaseException as e:
            self.write_error(403,content='Wrong argument.\n'+str(e))
        else:
            error=False
            errormsg=''

            with dbMutex:
                record=mainDB.get_result(rid)
                if record==0:
                    result=''
                    error=True
                    errormsg='Wrong id or wrong content type'
                elif record.ifFailed:
                    result=''
                    error=True
                    errormsg = 'Get fingerprint vector failed.'
                else:
                    if content == 'stopword':
                        result=record.stopwordPic
                    elif content=='realword':
                        result=record.realwordPic
                    elif content=='lda':
                        result=record.ldaPic
                    elif content=='glove':
                        result=record.glovePic
                    elif content=='sym2':
                        result=record.symVectorPic
                    elif content=='fingerprint':
                        result=record.fingerprintPic
                    else:
                        result=''
                        error=True

            if error:
                self.write_error(404,content=errormsg)
            else:
                if result==None:
                    self.write_error(404,content='Not done yet')
                else:
                    self.write(result)

class RecommendHandler(BaseHandler):
    def post(self):
        self.write_error(403,content='You should not post to this address.')

    def get(self):
        try:
            rid=int(self.get_argument('id'))
        except BaseException as e:
            self.write_error(403,content='Missing argument or wrong id.\n'+str(e))
        else:
            error=False
            with dbMutex:
                record=mainDB.get_result(rid)
                if record==0:
                    result=[]
                    error=True
                else:
                    result=record.recommend

            if error:
                self.write_error(404,content='Wrong id')
            else:
                if result==None:
                    self.write_error(404,content='Not done yet.')
                else:
                    self.set_header("Content-Type", "application/json; charset=UTF-8")
                    self.write(json.dumps(result))


def make_app():
    return tornado.web.Application([
        (r"/", HomeHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static/'}),
        (r"/posturl", PostURLHandler),
        (r"/postaccount", IDvsAccountHandler),
        (r"/analysis", AnalysisHandler),
        (r"/recommend",RecommendHandler),
    ])


if __name__=='__main__':
    app = make_app()
    app.listen(8888)

    for thread in calcThreadPool:
        thread.start()
    print("All threads started.")

    tornado.ioloop.IOLoop.current().start()
