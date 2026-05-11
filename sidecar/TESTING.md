# Sidecar 測試指南 (Testing Guide)

本文件提供 Sidecar 模組的完整測試驗證流程，分為「API 單元測試」與「n8n 整合測試」。

## 1. API 單元測試 (直接調用 Sidecar)
在不經過 n8n 的情況下，驗證 Python 邏輯是否運作正常。

### 檢查服務健康
```bash
curl -s http://localhost:5000/health
# 預期回應: {"status":"ok"}
```

### 測試 Analyzer 模組
```bash
curl -X POST http://localhost:5000/api/analyzer/analyze   -H "Content-Type: application/json"   -d '{"text":"這是一個測試句子，用來驗證 sidecar 分析功能。"}'
# 預期回應: 包含 "word_count" 與 "status": "success"
```

### 測試 Scraper 模組
```bash
curl -s "http://localhost:5000/api/scraper/scrape?url=https://www.google.com"
# 預期回應: 成功取得頁面相關數據
```

## 2. n8n 整合測試 (E2E)
確保 n8n 的 HTTP Request 節點已正確連結：

1. **啟用工作流**: 確保 n8n 中的 Webhook 工作流已切換為 **Active**。
2. **觸發 Webhook**:
   ```bash
   # 測試 Analyzer 工作流
   curl -X POST http://localhost:5678/webhook/analyze-trigger -d '{"text":"測試內容"}'
   
   # 測試 Scraper 工作流
   curl -X GET "http://localhost:5678/webhook/scrape-trigger?url=https://www.google.com"
   ```

## 3. 除錯檢查
若測試失敗，請依序執行以下步驟：
1. **查看 Sidecar 日誌**: `docker compose logs sidecar -f`
2. **檢查容器狀態**: `docker compose ps` (確認 sidecar 是否為 healthy)
3. **驗證網路**: 確保 n8n 節點網址為 `http://sidecar:5000/api/...`
