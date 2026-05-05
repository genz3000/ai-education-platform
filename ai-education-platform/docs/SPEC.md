# AI Education Platform - Project Specification
# 校本AI教學操作系統 - 項目規格書

## 1. 項目概述

### 1.1 項目背景

基於香港教育局「智啟學教」政策，推動校本 AI 教學改革。

### 1.2 核心定位

**School AI OS** — 不是工具，而是教學基礎設施

### 1.3 目標用戶

- **教師**: 備課、批改、教案生成
- **學生**: 自適應學習、即时答疑
- **學校管理層**: 數據分析、決策支持
- **家長**: 子女學習報告

---

## 2. 系統架構

### 2.1 六層架構

```
Layer 1: AI Services (LLM + RAG + Agent)
Layer 2: Knowledge Base (Vector DB + Graph)
Layer 3: Application Services (Q&A, Assessment, Analytics)
Layer 4: Data Analytics (Learning Analytics)
Layer 5: Platform (Auth, Permissions, API)
Layer 6: Security & Compliance
```

### 2.2 技術架構

```
┌─────────────────────────────────────────────────────────────┐
│  Frontend (Next.js)                                         │
│  ├── Teacher Portal (教案/批改/分析)                         │
│  ├── Student Portal (學習/問答)                              │
│  ├── Admin Portal (管理/設置)                                │
│  └── Parent Portal (報告查看)                               │
├─────────────────────────────────────────────────────────────┤
│  API Gateway (FastAPI + Nginx)                             │
│  ├── /api/v1/auth                                          │
│  ├── /api/v1/knowledge                                     │
│  ├── /api/v1/qa                                            │
│  ├── /api/v1/assessment                                    │
│  ├── /api/v1/analytics                                     │
│  └── /api/v1/lms                                           │
├─────────────────────────────────────────────────────────────┤
│  Backend Services (Python/FastAPI)                         │
│  ├── Auth Service                                          │
│  ├── Knowledge Service (RAG Pipeline)                       │
│  ├── Q&A Service (AI Chatbot)                             │
│  ├── Assessment Service (出題/批改)                         │
│  ├── Analytics Service (學習分析)                          │
│  └── LMS Integration Service                               │
├─────────────────────────────────────────────────────────────┤
│  Data Layer                                                │
│  ├── PostgreSQL (主數據庫)                                  │
│  ├── pgvector (向量數據庫)                                  │
│  ├── Redis (緩存)                                          │
│  └── S3/MinIO (文件存儲)                                    │
├─────────────────────────────────────────────────────────────┤
│  AI Layer                                                  │
│  ├── LLM Gateway (OpenAI/Claude)                          │
│  ├── Embedding Service                                    │
│  ├── RAG Engine                                            │
│  └── Agent Orchestrator                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 功能模組詳細規格

### 3.1 AI 教育知識庫系統

#### 3.1.1 教材管理

| 功能 | 描述 | 優先級 |
|------|------|--------|
| PDF 上傳解析 | 支援教材 PDF 自動拆段 | P0 |
| PPT/Word 支援 | 轉換後向量化 | P1 |
| OCR 圖片教材 | 圖片文字識別 | P1 |
| 章節結構識別 | 自動識別目錄層級 | P1 |
| 知識點抽取 | 從內容提取關鍵概念 | P0 |

#### 3.1.2 向量化與檢索

| 功能 | 描述 | 優先級 |
|------|------|--------|
| 語義向量化 | OpenAI embedding | P0 |
| 混合檢索 | 關鍵詞 + 向量混合 | P0 |
| Reranking | 相關性重排 | P1 |
| 引用追蹤 | 回溯原文位置 | P0 |

#### 3.1.3 知識圖譜

| 功能 | 描述 | 優先級 |
|------|------|--------|
| 知識點關聯 | 概念間關係建立 | P1 |
| 難度分級 | 按 DSE/TSA 分級 | P0 |
| 前置依賴 | 學習路徑推薦 | P1 |

### 3.2 AI 智能問答系統

#### 3.2.1 RAG 問答

| 功能 | 描述 | 優先級 |
|------|------|--------|
| 校本內容優先 | 學校資料優先檢索 | P0 |
| 多輪對話 | Context 記憶 | P0 |
| 引用展示 | 顯示答案來源 | P0 |

#### 3.2.2 角色模式

| 模式 | 應用場景 | 優先級 |
|------|---------|--------|
| 教師模式 | 教學解釋、教案生成 | P0 |
| 學生模式 | 概念解釋、解題引導 | P0 |
| 家長模式 | 子女學習情況查詢 | P2 |

### 3.3 AI 評估與出題系統

#### 3.3.1 AI 出題

| 功能 | 描述 | 優先級 |
|------|------|--------|
| DSE/TSA 對應 | 按考試格式生成 | P0 |
| 難度控制 | 1-5 星難度 | P0 |
| 題型多樣 | 選擇/填空/問答/作文 | P0 |
| 批量生成 | 一鍵生成試卷 | P1 |

#### 3.3.2 AI 批改

| 題型 | 批改方式 | 優先級 |
|------|---------|--------|
| 客觀題 | 100% 自動 | P0 |
| 主觀題 | 語意評分 + 等級 | P0 |
| 作文 | 多維度評分 (內容/組織/語言) | P0 |

#### 3.3.3 回饋生成

| 功能 | 描述 | 優先級 |
|------|------|--------|
| 錯誤原因 | 指出錯因 | P0 |
| 改進建議 | 提供學習方向 | P0 |
| 相似題推薦 | 鞏固練習 | P1 |

### 3.4 學習歷程與分析系統

#### 3.4.1 學習追蹤

| 數據 | 描述 | 優先級 |
|------|------|--------|
| 行為事件 | 查詢/作答/停留時間 | P0 |
| 學習指標 | 正確率/頻率/錯題類型 | P0 |
| 進度追蹤 | 章節完成度 | P0 |

#### 3.4.2 AI 分析

| 功能 | 描述 | 優先級 |
|------|------|--------|
| 強弱項分析 | 知識點掌握度 | P0 |
| 學習預測 | 考試表現預測 | P1 |
| 風險識別 | 學習困難預警 | P1 |

#### 3.4.3 報告系統

| 報告類型 | 受眾 | 優先級 |
|---------|------|--------|
| 個人學習報告 | 學生 | P0 |
| 班級分析報告 | 教師 | P0 |
| 家長通知報告 | 家長 | P1 |

### 3.5 教師支援系統

| 功能 | 描述 | 優先級 |
|------|------|--------|
| AI 教案生成 | 按課題生成教案 | P0 |
| 教學分析 | 班級整體情況 | P1 |
| 班級管理 | 學生分組/標籤 | P1 |
| 教材共編 | 協作編輯教案 | P2 |

---

## 4. 數據模型

### 4.1 核心實體

```
User
├── id (UUID)
├── email
├── role (teacher/student/parent/admin)
├── school_id
└── created_at

School
├── id (UUID)
├── name
├── code (學校編碼)
├── lms_config
└── settings

KnowledgeBase
├── id (UUID)
├── school_id
├── name
├── type (textbook/notes/exam)
└── metadata (課綱對應)

Document
├── id (UUID)
├── kb_id
├── file_path (S3)
├── chunks (Vector[])
└── metadata (title/section/difficulty)

Question
├── id (UUID)
├── kb_id
├── type (mcq/short/essay)
├── content
├── answer
├── difficulty (1-5)
└── dse_topic / tsa_topic

LearningRecord
├── id (UUID)
├── student_id
├── question_id
├── answer
├── correct
├── time_spent
└── timestamp

Assessment
├── id (UUID)
├── student_id
├── topic
├── generated_questions
├── completed_at
├── score
└── feedback
```

### 4.2 向量數據

```sql
-- pgvector for RAG
CREATE TABLE document_chunks (
    id UUID PRIMARY KEY,
    kb_id UUID REFERENCES knowledge_base(id),
    content TEXT,
    embedding VECTOR(1536),
    metadata JSONB
);

CREATE INDEX ON document_chunks USING ivfflat (embedding vector_cosine_ops);
```

---

## 5. API 接口

### 5.1 知識庫 API

```
POST   /api/v1/knowledge/upload      # 上傳教材
GET    /api/v1/knowledge/search     # 搜索知識庫
GET    /api/v1/knowledge/{id}       # 獲取知識項
PUT    /api/v1/knowledge/{id}       # 更新知識項
DELETE /api/v1/knowledge/{id}       # 刪除知識項
GET    /api/v1/knowledge/topics     # 獲取知識圖譜
```

### 5.2 問答 API

```
POST   /api/v1/qa/ask                # 提問
GET    /api/v1/qa/history            # 對話歷史
DELETE /api/v1/qa/history/{id}       # 刪除對話
POST   /api/v1/qa/feedback           # 回饋答案質量
```

### 5.3 評估 API

```
POST   /api/v1/assessment/generate   # AI 出題
POST   /api/v1/assessment/submit     # 提交答案
POST   /api/v1/assessment/grade      # AI 批改
GET    /api/v1/assessment/report     # 學習報告
```

### 5.4 分析 API

```
GET    /api/v1/analytics/student/{id}    # 學生分析
GET    /api/v1/analytics/class/{id}     # 班級分析
GET    /api/v1/analytics/trends          # 學習趨勢
```

---

## 6. 安全與合規

### 6.1 認證與授權

- JWT Token 認證
- RBAC 角色權限 (Teacher/Student/Parent/Admin)
- 學校隔離 (School-level isolation)

### 6.2 數據安全

- TLS 傳輸加密
- AES-256 靜態加密
- PII 脫敏處理

### 6.3 香港私隱合規

- 符合《個人資料（私隱）條例》(Cap. 486)
- 資料保留期限政策
- 學生資料特殊保護

### 6.4 審計日誌

- 操作審計記錄
- 數據訪問日誌
- 合規報告生成

---

## 7. 部署架構

### 7.1 環境配置

| 環境 | 用途 | 配置 |
|------|------|------|
| Dev | 本地開發 | Docker Compose |
| Staging | 測試環境 | k8s (2 nodes) |
| Production | 正式環境 | k8s (HA) |

### 7.2 擴展策略

- 前端: CDN + 靜態資源分離
- API: 水平擴展 + 負載均衡
- DB: 主從複製 + 讀寫分離
- Vector DB: 分片擴展

### 7.3 監控告警

- Prometheus + Grafana
- ELK 日誌收集
- 告警通知 (Email/SMS)

---

## 8. 交付里程碑

| 階段 | 週數 | 交付內容 |
|------|------|----------|
| MVP | 1-4 | 知識庫 + 基礎問答 + 教材上傳 |
| V1.0 | 5-8 | AI 出題 + AI 批改 + 學習分析 |
| V2.0 | 9-12 | 教師工具 + 家長報告 + LMS 整合 |
| Platform | 13-16 | 多校平台 + API 開放 + 出版商整合 |

---

## 9. 團隊分工 (待定)

| 角色 | 負責模組 |
|------|----------|
| 架構師 | 系統架構設計 |
| 後端開發 | API + AI 服務 |
| 前端開發 | 用戶界面 |
| 數據工程 | 知識庫 + 分析 |
| 測試工程 | 質量保障 |
| 運維 | 部署 + 監控 |