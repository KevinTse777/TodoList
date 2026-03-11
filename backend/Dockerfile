FROM python:3.11-slim   
WORKDIR /app

# 先装依赖，利用 Docker 层缓存
COPY requirements.txt /app/requirements.txt 
RUN pip install --no-cache-dir -r /app/requirements.txt

# 再复制项目代码
COPY . /app

EXPOSE 8000

RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]
