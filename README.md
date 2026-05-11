# n8n Sidecar Pattern (生產環境部署)

本專案展示如何透過 Docker Compose 建立一個具備 **Sidecar 架構** 的自動化環境，由 **n8n** 進行工作流編排，並調用 **Python 專業 Sidecar 服務** 執行數據處理任務。

## 1. 系統視覺化架構

### 系統資訊流 (Sequence Diagram)
展示請求與響應的時序邏輯：
```mermaid
sequenceDiagram
    participant U as User/外部
    participant N as n8n (指揮官)
    participant S as Python Sidecar (專家)
    participant E as External (外部服務)

    U->>N: Webhook Trigger (GET/POST)
    N->>S: API Request (http://sidecar:5000/api/...)
    S->>E: 執行爬蟲/分析邏輯
    E-->>S: 回傳原始數據
    S-->>N: 回傳處理後結果 (JSON)
    N-->>U: Webhook Response
```

### 物理架構圖 (Component Diagram)
展示容器間的依賴關係與資料流向：
```mermaid
graph LR
    User((使用者/外部)) -->|Webhook Trigger| n8n[n8n指揮官]
    subgraph Docker Network [n8n_net]
        n8n -->|HTTP Request| sidecar[Python Sidecar]
        sidecar -->|Flask API| n8n
    end
    sidecar -->|抓取/分析| External(外部網站/數據)
```

## 2. 架構說明
*   **n8n (指揮官)**: 負責流程編排、接收外部 Webhook 觸發，並透過內部網路調用 Sidecar。
*   **Python Sidecar (專業 Worker)**: 運行 Flask 服務，內建 requests 與 beautifulsoup4，負責執行實際的網頁抓取與邏輯分析任務。
*   **內部通訊**: 使用 Docker 內部網路 n8n_net，n8n 可透過 http://sidecar:5000 直接存取 Python 服務。

## 3. 目錄結構
- /home/user/n8n/ (主目錄)
- /home/user/n8n/sidecar/ (Python 執行環境)

## 4. 系統維運
*   **自動化重啟**: 整合 Systemd 管理 (n8n-production.service)。
*   **更新邏輯**: 修改後執行 docker compose up -d --build。
