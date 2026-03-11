# Recycle Classification (분리배출 가이드)

이 프로젝트는 사용자로부터 입력받은 품목이 어떤 분리배출 카테고리에 속하는지 분류해주는 애플리케이션입니다.
두 가지 방식(머신러닝 및 LLM/RAG)을 사용하여 분류 기능을 제공합니다.

<div align="center">
  <h3>♻️ AI 기반 분리배출 가이드 ♻️</h3>
</div>

## 주요 기능
- **Machine Learning Classification**: `RandomForestClassifier`를 사용하여 엑셀 데이터(`waste_train.xlsx`) 기반 분류 기능을 제공합니다.
- **LLM/RAG Classification**: `Qwen2.5-1.5B-Instruct` 모델과 PDF 문서(`waste_train.pdf`)를 활용한 RAG(Retrieval-Augmented Generation) 기반 답변을 생성합니다.
- **Modern UI**: React, Tailwind CSS, Motion(Framer Motion)을 활용하여 직관적이고 미려한 웹 인터페이스를 제공합니다.

## 프로젝트 구조
- `app.py`: Flask 백엔드 서버 (API 엔드포인트: `/classify`, `/classify_llm`)
- `LLM.py`: LangChain, ChromaDB, HuggingFace를 활용한 RAG 시스템 구축 로직
- `templates/`: React 프론트엔드 소스코드 (Vite 기반)
- `data/`: 학습 및 참조용 데이터 파일 (`.xlsx`, `.pdf`)
- `base.py`: 기본적인 ML 분류 기능만 포함된 Flask 서버 예제

## 시작하기

### 1. 백엔드 설정 (Python)
필수 라이브러리를 설치하고 서버를 실행합니다.
```bash
# 아나콘다 가상환경 생성 및 활성화
conda create -n venv python=3.10
conda activate venv

# 필수 패키지 설치
pip install flask pandas scikit-learn openpyxl torch transformers langchain langchain-community chromadb sentence-transformers

# cuda 13.0d으로 설치
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu130

pip install transformers accelerate bitsandbytes sentence-transformers langchain-huggingface langchain-community langchain-text-splitters pypdf chromadb nvitop
```
*참고: `LLM.py` 내의 `HUGGINGFACEHUB_API_TOKEN` 설정이 필요할 수 있습니다.*

### 2. 프론트엔드 빌드 (React)
프론트엔드 의존성을 설치하고 정적 파일을 빌드합니다.
```bash
cd templates
npm install
npm run build
```
빌드된 결과물은 `templates/dist`에 생성되며, `app.py`에서 이를 서빙합니다.

### 3. 서버 실행
```bash
python app.py
```
브라우저에서 `http://127.0.0.1:5000`에 접속하여 애플리케이션을 확인하세요.

## 기술 스택
- **Backend**: Python, Flask, Pandas, Scikit-learn
- **Frontend**: React (TypeScript), Vite, Tailwind CSS, Lucide-react, Framer Motion
- **AI/LLM**: LangChain, ChromaDB (Vector DB), HuggingFace (Qwen2.5-1.5B-Instruct)

## 데이터 출처
- `data/waste_train.xlsx`: 품목별 카테고리 매핑 데이터
- `data/waste_train.pdf`: 분리배출 가이드 상세 가이드라인 (RAG 컨텍스트용)

---
Made by **emo**
