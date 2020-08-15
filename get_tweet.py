#!/usr/bin/env python
# coding: utf-8







from requests_oauthlib import OAuth1Session
import json
import datetime, time, sys
from abc import ABCMeta, abstractmethod
import pandas as pd
import datetime





class TweetsGetter(object):
    __metaclass__ = ABCMeta
 
    def __init__(self):
        self.session = OAuth1Session(CK, CS, AT, AS)
 
    @abstractmethod
    def specifyUrlAndParams(self, keyword):
        '''
        呼出し先 URL、パラメータを返す
        '''
 
    @abstractmethod
    def pickupTweet(self, res_text, includeRetweet):
        '''
        res_text からツイートを取り出し、配列にセットして返却
        '''
 
    @abstractmethod
    def getLimitContext(self, res_text):
        '''
        回数制限の情報を取得 （起動時）
        '''
 
    def collect(self, total = -1, onlyText = False, includeRetweet = False):
        '''
        ツイート取得を開始する
        '''
 
        #----------------
        # 回数制限を確認
        #----------------
        self.checkLimit()
 
        #----------------
        # URL、パラメータ
        #----------------
        url, params = self.specifyUrlAndParams()
        params['include_rts'] = str(includeRetweet).lower()
        # include_rts は statuses/user_timeline のパラメータ。search/tweets には無効
 
        #----------------
        # ツイート取得
        #----------------
        cnt = 0
        unavailableCnt = 0
        while True:
            res = self.session.get(url, params = params)
            if res.status_code == 503:
                # 503 : Service Unavailable
                if unavailableCnt > 10:
                    raise Exception('Twitter API error %d' % res.status_code)
 
                unavailableCnt += 1
                print ('Service Unavailable 503')
                self.waitUntilReset(time.mktime(datetime.datetime.now().timetuple()) + 30)
                continue
 
            unavailableCnt = 0
 
            if res.status_code != 200:
                raise Exception('Twitter API error %d' % res.status_code)
 
            tweets = self.pickupTweet(json.loads(res.text))
            if len(tweets) == 0:
                # len(tweets) != params['count'] としたいが
                # count は最大値らしいので判定に使えない。
                # ⇒  "== 0" にする
                # https://dev.twitter.com/discussions/7513
                break
 
            for tweet in tweets:
                if (('retweeted_status' in tweet) and (includeRetweet is False)):
                    pass
                else:
                    if onlyText is True:
                        yield tweet['text']
                    else:
                        yield tweet
 
                    cnt += 1
                    if cnt % 1000 == 0:
                        print ('%d件 ' % cnt)
 
                    if total > 0 and cnt >= total:
                        return
 
            params['max_id'] = tweet['id'] - 1
 
            # ヘッダ確認 （回数制限）
            # X-Rate-Limit-Remaining が入ってないことが稀にあるのでチェック
            if ('X-Rate-Limit-Remaining' in res.headers and 'X-Rate-Limit-Reset' in res.headers):
                if (int(res.headers['X-Rate-Limit-Remaining']) == 0):
                    self.waitUntilReset(int(res.headers['X-Rate-Limit-Reset']))
                    self.checkLimit()
            else:
                print ('not found  -  X-Rate-Limit-Remaining or X-Rate-Limit-Reset')
                self.checkLimit()
 
    def checkLimit(self):
        '''
        回数制限を問合せ、アクセス可能になるまで wait する
        '''
        unavailableCnt = 0
        while True:
            url = "https://api.twitter.com/1.1/application/rate_limit_status.json"
            res = self.session.get(url)
 
            if res.status_code == 503:
                # 503 : Service Unavailable
                if unavailableCnt > 10:
                    raise Exception('Twitter API error %d' % res.status_code)
 
                unavailableCnt += 1
                print ('Service Unavailable 503')
                self.waitUntilReset(time.mktime(datetime.datetime.now().timetuple()) + 30)
                continue
 
            unavailableCnt = 0
 
            if res.status_code != 200:
                raise Exception('Twitter API error %d' % res.status_code)
 
            remaining, reset = self.getLimitContext(json.loads(res.text))
            if (remaining == 0):
                self.waitUntilReset(reset)
            else:
                break
 
    def waitUntilReset(self, reset):
        '''
        reset 時刻まで sleep
        '''
        seconds = reset - time.mktime(datetime.datetime.now().timetuple())
        seconds = max(seconds, 0)
        print ('\n     =====================')
        print ('     == waiting %d sec ==' % seconds)
        print ('     =====================')
        sys.stdout.flush()
        time.sleep(seconds + 10)  # 念のため + 10 秒
 
    @staticmethod
    def bySearch(keyword):
        return TweetsGetterBySearch(keyword)
 
    @staticmethod
    def byUser(screen_name):
        return TweetsGetterByUser(screen_name)
 
 





class TweetsGetterBySearch(TweetsGetter):
    '''
    キーワードでツイートを検索
    '''
    def __init__(self, keyword):
        super(TweetsGetterBySearch, self).__init__()
        self.keyword = keyword
        
    def specifyUrlAndParams(self):
        '''
        呼出し先 URL、パラメータを返す
        '''
        url = 'https://api.twitter.com/1.1/search/tweets.json?tweet_mode=extended'
        params = {'q':self.keyword, 'count':100}
        return url, params
 
    def pickupTweet(self, res_text):
        '''
        res_text からツイートを取り出し、配列にセットして返却
        '''
        results = []
        for tweet in res_text['statuses']:
            results.append(tweet)
 
        return results
 
    def getLimitContext(self, res_text):
        '''
        回数制限の情報を取得 （起動時）
        '''
        remaining = res_text['resources']['search']['/search/tweets']['remaining']
        reset     = res_text['resources']['search']['/search/tweets']['reset']
 
        return int(remaining), int(reset)
    
 





class TweetsGetterByUser(TweetsGetter):
    '''
    ユーザーを指定してツイートを取得
    '''
    def __init__(self, screen_name):
        super(TweetsGetterByUser, self).__init__()
        self.screen_name = screen_name
        
    def specifyUrlAndParams(self):
        '''
        呼出し先 URL、パラメータを返す
        '''
        url = 'https://api.twitter.com/1.1/statuses/user_timeline.json?tweet_mode=extended'
        params = {'screen_name':self.screen_name, 'count':200}
        return url, params
 
    def pickupTweet(self, res_text):
        '''
        res_text からツイートを取り出し、配列にセットして返却
        '''
        results = []
        for tweet in res_text:
            results.append(tweet)
 
        return results
 
    def getLimitContext(self, res_text):
        '''
        回数制限の情報を取得 （起動時）
        '''
        remaining = res_text['resources']['statuses']['/statuses/user_timeline']['remaining']
        reset     = res_text['resources']['statuses']['/statuses/user_timeline']['reset']
 
        return int(remaining), int(reset)





def get_tweet():
        
    while True:    
        key = input("ツイートを取得する条件を指定します。半角で入力してください。キーワードで取得:[1]　ユーザーを指定して取得[2]※2を選択した場合、分析はできません")

        if key =="1":
            keyword = input("取得したいキーワードを入力してください")
            num = int(input("何件取得しますか？※一度に取得できる件数は限られています。連続使用して取得できる件数が少なくなってきたらしばらく時間を空けてください"))
            # キーワードで取得

            getter = TweetsGetter.bySearch(u'{}'.format(keyword))

            #結果を格納するリスト（適宜イジる）
            id_lst = []
            profile_lst = []
            tweet_lst = []

            for tweet in getter.collect(total = num):#ツイート除外用件（適宜イジる）
                try:
                    if '@' in tweet['full_text']:#リプライであるツイート以外をリストに格納
                        continue
                    elif "#"  in tweet['full_text']:#純粋な呟きを集めるために、ハッシュタグ がついてるものは除去（広告等引っかかりやすい）
                        continue
                    elif "https://" in tweet['full_text']:#URLに誘導するものも除去
                        continue
                except:
                    continue
                    """
                    ⬇︎取得したい情報(何を取得したいかによって適宜イジる)
                    """
                id_lst.append(tweet['user']['screen_name'])#user_id
                profile_lst.append(tweet['user']['description'])#プロフィール文
                tweet_lst.append(tweet['full_text'])#ツイート本文

            print("除外条件を適応した結果の取得件数{}/{}".format(len(id_lst),num))
            print("※デフォルトではリプライ・ハッシュタグやURLのついたツイートを除外しています")
            
            #取得したデータでdf作成(適宜イジる)
            result_df = pd.DataFrame(id_lst,columns=['user_id'])
            result_df['profile'] = profile_lst
            result_df['tweet'] = tweet_lst
            #csvとして保存
            file_name = "{}{}".format(keyword,datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
            result_df.to_csv("data/{}.csv".format(file_name))
            print("{}.csvとしてdataフォルダに保存されました".format(file_name))
            break
        
        
        # ユーザーを指定して取得 （screen_name）
        elif key =="2":
            keyword = input("取得したいuserIDを入力してください")
            num = int(input("何件取得しますか？※一度に取得できる件数は限られています。連続使用して取得できる件数が少なくなってきたらしばらく時間を空けてください"))

            getter = TweetsGetter.byUser(keyword)

            #結果を格納するリスト（適宜イジる）
            tweet_lst = []

            for tweet in getter.collect(total = num):
                #try:
                #    if '@' in tweet['full_text']:#リプライであるツイート以外をリストに格納
                #       continue
                #    elif "#"  in tweet['full_text']:#純粋な呟きを集めるために、ハッシュタグ がついてるものは除去（広告等引っかかりやすい）
                #        continue
                #    elif "https://" in tweet['full_text']:#URLに誘導するものも除去
                #        continue
                #except:
                #    continue
                """
                ⬇︎取得したい情報(何を取得したいかによって適宜イジる)
                """
                tweet_lst.append(tweet['full_text'])#ツイート本文

            print("除外条件を適応した結果の取得件数{}/{}".format(len(tweet_lst),num))
            print("※デフォルトでは除外要件は定義されていません")
            #取得したデータでdf作成(適宜イジる)
            result_df = pd.DataFrame(tweet_lst,columns=['tweet'])
           #csvとして保存
            file_name = "{}{}".format(keyword,datetime.datetime.now().strftime("%y-%m-%d-%H-%M"))
            result_df.to_csv("data/{}.csv".format(file_name))
            print("{}.csvとしてdataフォルダ保存されました".format(file_name))
            break
        
        
        else:
            print("1か2を押してください")
            continue

if __name__ == "__main__":
    #TwitterAPIで取得したAPI key(CK)、API key secret(CS)、Access Token(AT)、Access Secret(AS)を入力
    print("TwitterAPIで取得したAPI consumer key/secret　・　Access Token/Secretを入力します")
    CK = input("API consumer key(CK)を入力してください")
    CS = input("API consumer secret(CS)を入力してください")
    AT = input("Access Token(AT)を入力してください") 
    AS = input("Access Secret(AS)を入力してください")
    get_tweet()

else:
    
    #TwitterAPIで取得したAPI key(CK)、API key secret(CS)、Access Token(AT)、Access Secret(AS)を入力
    print("TwitterAPIで取得したAPI consumer key/secret　・　Access Token/Secretを入力します")
    CK = input("API consumer key(CK)を入力してください")
    CS = input("API consumer secret(CS)を入力してください")
    AT = input("Access Token(AT)を入力してください") 
    AS = input("Access Secret(AS)を入力してください")