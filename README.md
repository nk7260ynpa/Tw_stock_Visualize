# Tw stock Visualization

## 啟動redash
```bash
docker compose -f redash.yml  up -d
docker-compose -f redash.yml run --rm server create_db
```

## 安裝Talib
```bash
brew install ta-lib
pip install ta-lib
```

## 啟動 prometheus grafana netdata
```bash
docker compose -f docker-compose.yml up -d
```
1. 進入 http://127.0.0.1:3000
2. 使用帳號 root 密碼 admin 登入
3. 右上角搜尋 import dashboard
4. 輸入 dashboard id 7107
5. 點選 Load
6. 點選 Prometheus
7. 刪除不需要的圖表
8. 點選 Save dashboard  
9. 完成