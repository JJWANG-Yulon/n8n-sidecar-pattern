# n8n Sidecar Pattern (Production)

這是一個將 **n8n 工作流編排** 與 **Python 邏輯處理 (Sidecar)** 模組化整合的生產級部署架構。

## 架構說明
本專案透過 Sidecar Pattern 解耦 n8n 的沙盒限制，並藉由 Docker Compose 與 Systemd 實現高可用性。

### 目錄結構
- `docker-compose.yml`: 定義 n8n 與 Sidecar 服務。
- `sidecar/`: 核心邏輯處理目錄 (Flask 路由、爬蟲、分析)。
- `data/`, `logs/`, `files/`: 資料持久化目錄。

## 部署 SOP

### 1. 服務啟動
確保 Docker 服務運行後，執行：
```bash
docker compose up -d
```

### 2. 開機自啟 (Systemd)
本專案整合 Systemd 管理，將以下服務配置至 `/etc/systemd/system/n8n-production.service`：
- 自動故障重啟 (`Restart=on-failure`)
- 隨 Docker Engine 自動啟動

### 3. API 調用規範
在 n8n 的 HTTP Request 節點中使用：
- **Analyzer**: `http://sidecar:5000/api/analyzer/analyze` (POST)
- **Scraper**: `http://sidecar:5000/api/scraper/scrape` (GET)

## 維護建議
- **路由擴展**: 新增 `routes/` 檔案並於 `app.py` 中使用 Blueprint 註冊。
- **套件管理**: 修改 `sidecar/requirements.txt` 後，需重新執行 `docker compose up -d --build`。
- **狀態檢查**: 使用 `docker compose logs sidecar` 查看邏輯執行狀況。

---
*Powered by Hermes Architecture - 狀態恢復能力 (State Recovery) 主導設計。*
