import logging
import os
import pandas as pd
import hashlib
from app.rag.vector_store import VectorStore

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")

def load_faq():
    os.makedirs("data", exist_ok=True)
    excel_path = "data/faq.xlsx"

    print(f"📂 load_faq_data 使用的持久化目录: {os.path.abspath('./chroma_db')}")
    if not os.path.exists(excel_path):
        logger.info("📝 创建样例数据: %s", excel_path)
        data = [
            ["物流政策", "美国仓的发货时效是多久？", "美国仓支持工作日当天下午 2 点前截单，订单会在 24 小时内发出。", "美国仓, 发货时效"],
            ["物流政策", "德国仓支持退货吗？", "德国仓支持退货，需在收到货物后 14 天内发起申请。", "德国仓, 退货"],
            ["价格与折扣", "三年期高性能云服务器有折扣吗？", "三年期高性能云服务器享受 85 折优惠。", "云服务器, 折扣"],
        ]
        df = pd.DataFrame(data, columns=["category", "question", "answer", "keywords"])
        df.to_excel(excel_path, index=False)

    # 读取 Excel
    df = pd.read_excel(excel_path, dtype=str)
    logger.info("📂 读取 Excel: %s, 共 %d 行", excel_path, len(df))

    # 初始化向量库
    vs = VectorStore(persist_dir=CHROMA_DIR, collection_name="faq")

    # 清空旧数据
    all_ids = vs.collection.get()["ids"]
    if all_ids:
        vs.collection.delete(ids=all_ids)
        logger.info("🗑️ 已清空旧数据，共 %d 条", len(all_ids))

    # 插入新数据
    inserted = 0
    for _,row in df.iterrows():
        question = str(row["question"]).strip()
        if not question:
            continue
        answer = str(row["answer"]).strip() if pd.notna(row["answer"]) else "暂无答案" #notna 检索是否包含answer
        doc_text = f"Q: {question}\nA: {answer}"
        doc_id = hashlib.md5(question.encode("utf-8")).hexdigest()
        metadata = {
            "category": str(row["category"]),
            "question": question,
            "keywords": str(row["keywords"]) if pd.notna(row["keywords"]) else "",
            "source": excel_path
        }
        vs.collection.add(
            documents=[doc_text],
            metadatas=[metadata],
            ids=[doc_id]
        )
        print(f"✅ 插入后集合文档数: {vs.count()}")
        inserted += 1

    logger.info("✅ 加载完成: 插入 %d 条文档", inserted)
    logger.info("📊 向量库文档总数: %d", vs.collection.count())

if __name__ == "__main__":
    load_faq()