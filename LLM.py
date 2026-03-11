import torch
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import shutil
import os

import os
os.environ["HUGGINGFACEHUB_API_TOKEN"] = ""

# Chroma 캐시 디렉토리 정의
CHROMA_DB_PATH = "./chroma_db"

# 이전 벡터 DB 삭제 (매번 새로 생성하도록)
# if os.path.exists(CHROMA_DB_PATH):
#     print(f"이전 벡터 데이터베이스 삭제: {CHROMA_DB_PATH}")
#     shutil.rmtree(CHROMA_DB_PATH)

# 1. 문서 로드 및 분할
# 'manual.pdf'라는 파일이 있다고 가정합니다.
print("문서를 읽고 분할하는 중...")
loader = PyPDFLoader(r"C:\sjbang\STUDY\Classification\data\waste_train.pdf") # 내 PDF 경로로 수정

documents = loader.load()
print(f"로드된 문서 수: {len(documents)}")

if len(documents) == 0:
    print("경고: 문서를 찾을 수 없습니다. 파일 경로를 확인하세요.")
else:
    # 긴 문서를 모델이 읽기 편하게 적당한 크기(Chunk)로 자릅니다.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    print(f"분할된 텍스트 청크 수: {len(texts)}")

    # 2. 문서를 숫자로 변환 (Embedding)
    # 한국어/영어 모두 지원하는 가벼운 모델을 사용합니다.
    print("임베딩 모델 로드 중...")
    embeddings = HuggingFaceEmbeddings(
        # model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'} # GPU가 있다면 'cuda'로 변경
    )

    # 3. 벡터 데이터베이스 생성 (메모리가 아닌 디스크 기반)
    # 추출된 특징들을 ChromaDB에 저장합니다.
    print("벡터 데이터베이스 생성 중...")
    vector_db = Chroma.from_documents(
        documents=texts, 
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH
    )
    vector_db.persist()  # 디스크에 저장
    print("벡터 데이터베이스 생성 및 저장 완료!")

    # 4. 답변 생성 모델 (LLM) 로드
    # 여기서는 아주 가벼운 'Gemma' 또는 'Qwen' 모델을 추천합니다.
    model_id = "Qwen/Qwen2.5-1.5B-Instruct" # 혹은 "Qwen/Qwen2.5-1.5B-Instruct"
    # model_id = "google/gemma-2-2b-it" # 사용권한 취득 필요
    print(f"생성 모델({model_id}) 로드 중... (시간이 좀 걸릴 수 있습니다)")

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map={"": 0}
    )

    # LangChain과 연결하기 위한 파이프라인 구성
    pipe = pipeline(
        "text-generation", 
        model=model, 
        tokenizer=tokenizer, 
        max_new_tokens=128,
        temperature=0.1, # 답변의 일관성을 위해 낮게 설정
        return_full_text=False  # 생성된 텍스트만 반환 (입력 프롬프트 제외)
    )
    llm = HuggingFacePipeline(pipeline=pipe)

    # 5. 최신 방식의 RAG 체인 구축
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})

    # 프롬프트 템플릿 정의
    prompt = ChatPromptTemplate.from_template(

        """다음 컨텍스트를 바탕으로 질문에 답하세요. 답을 모르면 모른다고 말하세요.

        컨텍스트:
        {context}

        질문: {question}
        답변:"""
            )

    # RAG 체인 구성: retriever -> context 포매팅 -> LLM -> 출력
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    # query  = "계란껍질의 category는 무엇인가요?"
    # print(f"\n질문: {query}")
    # result = rag_chain.invoke(query)

    # # 결과에서 "Assistant:" 이후의 텍스트만 추출
    # if "Assistant:" in result:
    #     answer = result.split("Assistant:", 1)[-1].strip()
    # else:
    #     answer = result.strip()

    # print("\n=== AI 답변 ===")
    # print(answer)
