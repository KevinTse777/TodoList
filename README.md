# FastAPI Todo (学习版)

一个轻量的 Todo 学习项目：后端是 FastAPI + MySQL + Alembic，前端是 Vue 3（极简浅色 iOS 质感）。

## Quickstart（Docker Compose）

1. 进入项目目录

```bash
cd /Users/tse/Documents/fastapi
```

2. 一键构建并启动（前后端 + 数据库）

```bash
docker compose up -d --build
```

3. 查看服务状态

```bash
docker compose ps
```

4. 访问地址

- 前端：http://127.0.0.1:5173
- 后端健康检查：http://127.0.0.1:8000/api/v1/healthz
- Swagger UI：http://127.0.0.1:8000/docs

5. 停止服务

```bash
docker compose down
```

## 常用命令

查看后端日志：

```bash
docker compose logs -f backend
```

查看前端日志：

```bash
docker compose logs -f frontend
```

仅重建前端：

```bash
docker compose up -d --build frontend
```

## 说明

- `backend/start.sh` 已包含 `alembic upgrade head`，容器启动会自动迁移数据库。
- 前端默认请求 `http://localhost:8000` 的 API，无需修改后端代码。
