# Community Pulse Reporter - GitHub Action Dockerfile
# 基於 Python 3.9 slim 映像，用於生成社群貢獻報告

FROM python:3.9-slim

# 設定工作目錄
WORKDIR /action

# 安裝必要的系統依賴
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 複製依賴文件
COPY requirements.txt /action/requirements.txt

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製 Action 所需的腳本
COPY action_entrypoint.py /action/action_entrypoint.py
COPY scripts/community_reporter/ /action/scripts/community_reporter/

# 設定 Python 路徑
ENV PYTHONPATH=/action:$PYTHONPATH
ENV PYTHONUNBUFFERED=1

# 設定入口點
ENTRYPOINT ["python", "/action/action_entrypoint.py"]

