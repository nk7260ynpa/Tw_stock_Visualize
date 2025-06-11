# Tw stock Visualization

## 啟動redash
```bash
docker compose -f redash.yml  up -d
docker-compose -f redash.yml run --rm server create_db
```

## 啟動 prometheus grafana netdata
```bash
docker compose -f docker-compose.yml up -d
```