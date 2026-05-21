# ♻️ Local RAG System for Waste Classification
> **Local-first RAG system optimized for low VRAM environments, focusing on accurate Korean text processing and waste category classification.**

---

## 🚀 Overview
이 프로젝트는 저사양 로컬 환경(VRAM 4GB 내외)에서도 한국어 지시 이행 능력이 뛰어난 소형 LLM과 정밀한 데이터 전처리를 결합하여 구축한 **쓰레기 분리배출 안내 RAG(Retrieval-Augmented Generation) 시스템**입니다.

## 🛠️ Tech Stack & Environment

### 1. Large Language Model (LLM)
- **Model:** `Qwen/Qwen2.5-1.5B-Instruct` (4-bit Quantized)
- **Selection Reason:** 
  - **Efficiency:** VRAM 사용량을 3~4GB 내외로 억제하면서도 뛰어난 한국어 성능 유지.
  - **Reliability:** 소형 모델임에도 프롬프트 태그(ChatML) 준수 능력이 우수함.
- **Optimization:** Few-Shot Prompting을 통해 출력 형식을 강제하여 헛소리(Hallucination) 방지.

### 2. Embedding Model
- **Model:** `BAAI/bge-m3` (Multi-lingual)
- **Dimension:** 1024-dim
- **Improvement:** 기존 영어 전용 모델(`all-MiniLM-L6-v2`) 대비 한국어 문맥 파악 및 검색 정확도 대폭 향상.

### 3. Vector Database
- **Engine:** `ChromaDB`
- **Data Persistence:** `./chroma_db`

---

## 💡 Key Engineering Points

### 🎯 Data Parsing Strategy (The "Magic" Sauce)
표 구조(Table) 데이터를 기계적으로 자를 때 발생하는 문맥 단절 문제를 해결하기 위해 **초정밀 라인 매칭** 기법을 적용했습니다.

1.  **Line-by-Line Splitting:** `RecursiveCharacterTextSplitter` 대신 줄바꿈(`\n`) 기반 분할.
2.  **Semantic Reconstruction:** 
    - PDF의 `신문지 종이류` 구조를 추출.
    - `"{품목}의 분리배출 카테고리는 {카테고리}입니다."`와 같은 완성형 평서문으로 변환.
3.  **Accuracy:** 문장 형태로 변환하여 저장함으로써 소형 LLM이 검색 결과(Context)를 더 쉽게 이해하도록 최적화.

### 📊 Validation System
"LLM의 지능 문제인가, 검색(Retriever)의 문제인가?"를 판단하기 위한 검증 체계 구축.
- **Retriever:** `k:3` 설정을 통해 연관 문서 3건 추출.
- **Cosine Similarity Score:** 검색된 문서와 질문 간의 유사도를 수치화하여 데이터 오염 여부 모니터링.
- **DB Maintenance:** 오염된 데이터(Cache) 발견 시 `chroma_db` 수동 초기화 및 재빌드를 통한 정제.

---

## 📝 Prompt Template
```markdown
<|im_start|>system
당신은 쓰레기 분리배출 카테고리를 정확하게 안내하는 챗봇입니다.
주어진 컨텍스트 정보만을 바탕으로 질문에 답변하세요.

[출력 규칙]
1. 불필요한 설명, 인사말, 수식어는 전부 제외합니다.
2. 오직 해당하는 카테고리 이름 뒤에 "~입니다" 또는 "~류입니다"만 붙여서 한 줄로 명사형 종결 어미로만 답변하세요.
3. 만약 컨텍스트를 보고 답을 알 수 없다면 오직 "모릅니다"라고만 답변하세요.

[답변 예시]
질문: 신문지는 어디에 버려야 하나요?
답변: 종이류입니다.
<|im_end|>
...
```

---

## 📈 Future Roadmap
- [ ] **중복 제거 로직:** `set()` 또는 `dict`를 이용한 DB 저장 전 중복 텍스트 필터링 적용.
- [ ] **데이터 소스 최적화:** PDF 대신 `.csv`와 `CSVLoader`를 활용한 데이터 정형화 및 관리 효율 증대.
- [ ] **Reranking:** 검색된 결과의 순위를 재조정하여 정확도 극대화.

---
*Created by sjbang (Study Note)*

