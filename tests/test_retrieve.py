from app.rag.vector_store import VectorStore
import logging

logger = logging.getLogger(__name__)

vs = VectorStore()

params1 = {
    "query_texts": ["美国仓"],
    "n_results": 2
}

logger.info("场景1 参数: %s", params1)

result1 = vs.collection.query(**params1) #不用输出一大串key=value,**表示key=value **params1

logger.info("场景1 结果条数: %s", len(result1["documents"][0]) if result1["documents"] else 0)
logger.info("-"*40)


# 场景2：带过滤条件的查询
params2 = {
    "query_texts": ["美国仓"],
    "n_results": 2,
    "where": {"category": "物流政策"}
}
logger.info("场景2 参数: %s", params2)
result2 = vs.collection.query(**params2)
logger.info("场景2 结果条数: %s", len(result2["documents"][0]) if result2["documents"] else 0)
logger.info("-" * 40)

# 场景3：含 include（返回元数据）
params3 = {
    "query_texts": ["美国仓"],
    "n_results": 2,
    "include": ["documents", "metadatas", "distances"]
}
logger.info("场景3 参数: %s", params3)
result3 = vs.collection.query(**params3)
if result3["documents"]:
    # 安全地提取日志信息
    if result3 and result3.get("documents") and result3["documents"][0]:
        first_doc = result3["documents"][0][0]
        preview = first_doc[:50] + "..." if len(first_doc) > 50 else first_doc
        logger.info("第一条文档: %s", preview)
    else:
        logger.warning("未检索到文档")

    if result3 and result3.get("metadatas") and result3["metadatas"][0]:
        logger.info("元数据: %s", result3["metadatas"][0][0])

    if result3 and result3.get("distances") and result3["distances"][0]:
        logger.info("相似度分数: %s", result3["distances"][0][0])