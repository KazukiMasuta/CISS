# CISS
CISS(サイス)は都立大生向け情報共有サイトです。
旧サイトは 石池｜ishiike (http://ishiike.matrix.jp) です。

<<<<<<< HEAD
indexに投稿ボタン -> 授業に関することか否か -> (1. 授業ならどの授業化選ぶ画面 -> 投稿ページ) (2. そうでないならそのまま投稿画面)

2/24
detail.htmlの作成
投稿後のページ移動の際のpk値の引き渡し

todo
・投稿ページのフロント実装


## いいねボタン

detail.html -58 jsが反応しない
-vote.jsに問題がある　or detail.htmlのコードが足りない　etc

## デプロイ前に最低限したいこと
・ヘッダーの画像を表示させる 3/15完了
・サイドバーを作る(
    ホーム
    検索
    アカウント
)　 3/15完了
・授業と同じようにサークルのものを作る  3/15完了
・動作確認
・アカウントページの作成
・学校のドメインで登録できるようにする
・投稿にとぶボタンの調整
・レスポンシブ対応

・投稿一覧でいいねの横にコメント数を表示させたい
・tradeの調整

## 4/21
授業投稿のviewsとdetailをtopicsに移した
topics/の後に授業番号（daya_id)をurlに持ってこないとsavewithdata関数が動かない

## 5/11
授業投稿ができるようになった
その他のちょっとした不具合を直した

## 5/20
ーーデバッグーー
ログイン時、アカウントが登録されてない場合にエラーが出る
サインアップのエラー時にエラー警告がでない
同じ名前で登録できない。
登録時の確認画面の修正
物物交換のページが開けなくなった。
授業ページの科目種別が表示されない。
サイトにアクセス時、通信が保護されていない物になっている。
=======
http://tmuciss.com
>>>>>>> 0d87902aeaa785a6bdb2e59a1241c25f5ad62a82
