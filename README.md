# FastAPI Todo (学习版)

## 关闭后如何重新启动后端服务

1. 打开终端并进入项目目录：

```bash
cd /Users/tse/Documents/fastapi
```

2. 激活 conda 环境：

```bash
conda activate fastapi-todo
```

3. 启动 FastAPI（开发模式，热重载）：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --app-dir backend
```

4. 验证服务是否启动成功：

```bash
curl http://127.0.0.1:8000/api/v1/healthz
```

预期返回：

```json
{"status":"ok"}
```

5. 打开文档页面：

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 如何停止服务

- 在运行 `uvicorn` 的终端中按 `Ctrl + C`。

## 用docker 启动mysql

删掉旧的同名容器
启动一个新的
docker run --name todo-mysql \
  -e MYSQL_ROOT_PASSWORD=rootpass \
  -e MYSQL_DATABASE=todo_db \
  -e MYSQL_USER=todo_user \
  -e MYSQL_PASSWORD=todo_pass \
  -p 3306:3306 \
  -d mysql:8.4

  
