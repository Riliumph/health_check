# HealthChecker

## 使い方

```console
$ docker compose up -d
```

### nginxへのアクセス

#### L7 アプリケーション

```console
$ docker compose exec -it health_checker curl -i http://nginx/service-a.html
HTTP/1.1 200 OK
Server: nginx/1.26.3
Date: Mon, 24 Feb 2025 16:14:27 GMT
Content-Type: text/html
Content-Length: 9
Last-Modified: Fri, 21 Feb 2025 17:10:56 GMT
Connection: keep-alive
ETag: "67b8b3a0-9"
Accept-Ranges: bytes

service-a
```

#### L7 ヘルスチェック

```console
$ docker compose exec -it health_checker curl -i http://nginx/health
HTTP/1.1 200 OK
Server: nginx/1.26.3
Date: Mon, 24 Feb 2025 16:14:10 GMT
Content-Type: application/octet-stream
Content-Length: 8
Connection: keep-alive

healthy
```

#### L4 ヘルスチェック

```console
$ docker compose exec -it health_checker nc nginx 8084
healthy
(待ち状態)
```

切断された場合はヘルスチェック異常。  
ただし、春暖の可能性があるので再接続処理をしてつながらないことの確認が必要。

###
