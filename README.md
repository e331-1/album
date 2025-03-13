# 実行方法
## 1 ダウンロードする
git cloneしてダウンロードする
```
$ git clone https://github.com/e331-1/album
```
## 2 設定変更
.envファイル中のsearch_directoryの中にあるファイルを捜索するので、自分の環境に合わせて変更してください。拡張子がjpgのものだけ読み込みます。

## 3 サーバー立てる
docker composeで実行する
```
$ docker compose up -f "docker-compose.yml" --build
```

## 4 データベース構築
http://\[サーバーIP\]:8080/api/registerFromLocal
にアクセスすると、AIでの画像処理が始まる

## 5 完了！
http://\[サーバーIP\]:8080/
にアクセスすると使える