# Twitter感情分析＆トピック分類

任意のキーワードを含むツイートとプロフィール情報をTwitter上から収集し、各tweetのポジ/ネガを判定します。そしてポジ/ネガtweetをしたアカウントをプロフィール情報をもとにクラスタリングします。

感情分析にはBERT、クラスタリングにはLDAを用いています。


## 事前準備

①Twitter APIの利用申請を行い、APIキー、トークンを取得してください。 <br> https://www.itti.jp/web-direction/how-to-apply-for-twitter-api/

②以下をインストールしてください。（環境によっては漏れがあるかもしれません。エラーで引っかかる場合は適宜インストールしてください）
```python
$pip install wordcloud
$pip install seaborn
$pip install gensim
$pip install pyldavis
$pip install ipython
$pip install requests requests_oauthlib
$brew install mecab
$brew install mecab-ipadic
$brew install swig
$pip install mecab-python3
```
## 使い方

### ①学習データセット作成

BERTの事前学習モデルとしては東北大学の乾研究室が作成したものを用いています。

https://huggingface.co/transformers/pretrained_models.html

このモデルを日本語tweetデータでポジネガ判定できるようfine-tuningするために、以下で公開されているTwitter日本語評判分析データセットを用います。<br>
http://www.db.info.gifu-u.ac.jp/data/Data_5d832973308d57446583ed9f 

利用方法はhttps://github.com/tatHi/tweet_extructor 参考にしてください。

取得したtweetデータとlabelを以下のような形式でcsvファイルにまとめます。

<img width="713" alt="スクリーンショット 2020-08-13 1 52 31" src="https://user-images.githubusercontent.com/62980317/90303682-d9710e00-deea-11ea-84f9-51febc342b14.png">

### <特定のキーワードに特化して判定させる場合>

get_tweet.pyを実行してそのキーワードに関するツイートを取得し、preprocessing.pyを実行してツイートを前処理します。

そして前処理されたデータを自力でラベル付けを行って、作成したcsvファイルに追加してください。

(Twitter日本語評判分析データセットでのみfine-tuningを行った結果の精度は60〜65%、あるキーワードを200件ラベル付けして加えた場合の精度は65〜70%でした。)


### ②学習

作成したcsvファイルをディレクトリ下に置いて、train_model.ipynb（py）を実行してください。(GPU推奨)

テストデータは作成した訓練データを分割するか、任意のツイート情報が入ったデータを上記画像の形式で作成してください。

### ③予測

get_tweet & Analysis.ipynb(Analysis.py)を実行し、表示に従って操作することで感情分析〜クラスタリングまで行うことができます

予測結果はresultフォルダに保存されます。

## 参考にした記事

tweet取得<br>
http://ailaby.com/twitter_api/

BERTによる感情分析<br>
https://qiita.com/namakemono/items/4c779c9898028fc36ff3

LDA<br>
http://www.ie110704.net/2018/12/29/wordcloud%E3%81%A8pyldavis%E3%81%AB%E3%82%88%E3%82%8Blda%E3%81%AE%E5%8F%AF%E8%A6%96%E5%8C%96%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6/
