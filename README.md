# Tweet の感情分析＆ポジ/ネガによるアカウントのクラスタリング

## 利用方法

#### ※CPU では分析に時間がかかるため GPU の利用を推奨します。<br>そのため簡単に GPU を使える Google Colab の利用を想定して説明をします

### ①Twitter API の利用申請を行い、API キー、トークンを取得

### ② リポジトリをクローン

```
git clone https://github.com/nobuhiroaraki/Twitter_Analysis.git
```

### ③ Twitter_Analysis フォルダを google drive にアップロード

### ④Google Colab で test_notebook.ipynb を開く ➡︎GPU に接続し、drive にマウント

### ⑤test_notebook.ipynb の全てのセルを実行して指示に従って操作をすることで<br>ツイートの収集・前処理・ファインチューニング・感情分析・クラスタリングまで行うことができます。

## ファインチューニング用データセット作成について<br>

train_model()実行の前にファインチューニング用のデータセットを作成する必要があります。そのやり方を解説します。

BERT の事前学習モデルとして、東北大学の乾研究室が作成した Pretrained Japanese BERT models を用いています。<br>
https://github.com/cl-tohoku/bert-japanese

このモデルを日本語 tweet データでポジネガ判定できるようファインチューニングします。<br>

ファインチューニングのためのデータセット作成として以下の 2 種類の方法があります。

#### (1)分析したいキーワードに特化して判定させる場合（300 件のデータでファインチューニングした結果、精度 75%前後）<br>

※デフォルトではこのやり方を想定しています

processed.csv からいくつか(100 以上推奨)を抜き出し、以下の表と同じ形式で csv ファイルを新しく作ります。<br>

また、作成完了した csv ファイルを train_data フォルダに保存してください。

<img width="716" alt="スクリーンショット 2020-08-26 18 57 09" src="https://user-images.githubusercontent.com/62980317/91290065-1fbd4b80-e7ce-11ea-98cd-b5ee06236764.png">

#### (2)どのような話題に対しても汎用的に推測を行う場合（精度 65~70%前後）

様々な話題に対して汎用的に推測を行うには大量のデータが必要です。<br>
しかし自力で大量にラベル付けを行うのは大変なため、以下で公開されている大規模な Twitter 日本語評判分析データセットを用います。<br>
http://www.db.info.gifu-u.ac.jp/data/Data_5d832973308d57446583ed9f

利用方法はhttps://github.com/tatHi/tweet_extructor を参考にしてください。<br>

取得した tweet データと感情判定(ポジティブ=1、ネガティブ=0)を、上記表と同様の形式で csv ファイルにまとめます。

## 結果例

### 「タピオカ」を含むツイートをしたアカウントを、プロフィール情報をもとにクラスタリングした結果(抜粋)

#### ポジティブクラスタ例

![3topics_positive_group1](https://user-images.githubusercontent.com/62980317/91171837-2a1c0e80-e716-11ea-96e2-fb20db7a8b96.png)

<img width="1415" alt="スクリーンショット 2020-08-25 20 32 57" src="https://user-images.githubusercontent.com/62980317/91171854-3738fd80-e716-11ea-80f0-6bad3cab955e.png">

#### ネガティブクラスタ例

![4topics_negative_group2](https://user-images.githubusercontent.com/62980317/91171975-6d767d00-e716-11ea-9ecf-6795a8598813.png)

<img width="1408" alt="スクリーンショット 2020-08-25 20 32 16" src="https://user-images.githubusercontent.com/62980317/91171988-71a29a80-e716-11ea-9e80-6b958f882f02.png">

#### 分析結果の HTML 形式のファイルはダウンロードしてお使いください
