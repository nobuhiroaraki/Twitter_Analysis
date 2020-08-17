# Tweetの感情分析＆ポジ/ネガによるユーザーのクラスタリング

## 目的
#### ➡︎商品やサービスに関するtweetをポジ/ネガ判定し、ポジ/ネガtweetをする人はどんな層の人々なのかを分析する。

サクラレビューやアフィリエイトサイトが乱立する今日で、

・「商品やサービスの真の評判はTwitterに集まるのでは？」<br>
・「Twitterのプロフィール情報はその人の属性をかなり説明するものなのでは？」 

という二つの仮説のもと、真の評判が集まる（はず）tweet情報からをポジ/ネガ分析し、それぞれの感情を抱く潜在的な層をTwitterのプロフィール情報から明らかにしようという試みです。

## 概要
任意のキーワードを含むツイートとプロフィール情報をTwitter上から収集し、各tweetのポジ/ネガを判定します。<br>
そしてポジ/ネガtweetをしたアカウントを、そのプロフィール情報からクラスタリングします。<br>
(例)
①「タピオカ」を含むツイートを収集

②収集したツイートのポジ/ネガを判定

③タピオカについてポジティブ（ネガティブ）なツイートをしたアカウントを、プロフィール文の情報を元にクラスタリング
（ポジティブクラスタ①「k-pop・韓国・JK」、ポジティブクラスタ②「大学・スタバ・バイト」　のようなイメージです）


感情分析にはBERT(transformers)、クラスタリングにはLDA(gensim)を用いています。


## 事前準備

①Twitter APIの利用申請を行い、APIキー、トークンを取得してください。 

②以下をインストールしてください。

（環境によっては漏れがあるかもしれません。エラーが起きる場合は適宜インストールしてください）
```python
#実行環境
python==3.6.10
tensorflow==2.2.0
$pip install wordcloud
$pip install seaborn
$pip install gensim
$pip install transformers
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

BERTの事前学習モデルとして、東北大学の乾研究室が作成したPretrained Japanese BERT modelsを用いています。

https://github.com/cl-tohoku/bert-japanese

このモデルを日本語tweetデータでポジネガ判定できるようfine-tuningします。<br>
そのために以下で公開されているTwitter日本語評判分析データセットを用います。<br>
http://www.db.info.gifu-u.ac.jp/data/Data_5d832973308d57446583ed9f 

利用方法はhttps://github.com/tatHi/tweet_extructor 参考にしてください。

取得したtweetデータとlabelを以下のような形式でcsvファイルにまとめます。

<img width="713" alt="スクリーンショット 2020-08-13 1 52 31" src="https://user-images.githubusercontent.com/62980317/90303682-d9710e00-deea-11ea-84f9-51febc342b14.png">

### <特定のキーワードに特化して判定させる場合>

get_tweet.pyを実行してそのキーワードに関するツイートを取得し、preprocessing.pyを実行してツイートを前処理します。

そして前処理されたデータを上記表のようにラベル付けを行って、作成したcsvファイルに追加してください。

(日本語評判分析データセットのみでfine-tuningを行った結果の精度は60〜65%、特定のキーワードを200件ラベル付けして加えた場合の精度は65〜70%でした。)


### ②学習

作成したcsvファイルをディレクトリ下に置いて、train_model.ipynbを実行してください。(GPU推奨)

テストデータは作成した訓練データを分割するか、任意のツイート情報が入ったデータを上記画像の形式で作成してください。

### ③予測
Analysis.pyを実行し、表示に従って操作することで感情分析〜クラスタリングまで行うことができます

### 学習させた重みを使い回す場合
get_tweet & Analysis.ipynbを実行することで、ツイートの収集〜分析まで一括で行うことができます。

予測結果はresultフォルダに保存されます。

## 参考にした記事

tweet取得<br>
http://ailaby.com/twitter_api/

BERTによる感情分析<br>
https://qiita.com/namakemono/items/4c779c9898028fc36ff3

LDA<br>
http://www.ie110704.net/2018/12/29/wordcloud%E3%81%A8pyldavis%E3%81%AB%E3%82%88%E3%82%8Blda%E3%81%AE%E5%8F%AF%E8%A6%96%E5%8C%96%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6/
