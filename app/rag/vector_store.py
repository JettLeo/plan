import chromadb
from chromadb.utils import embedding_functions
import logging
from typing import List, Dict, Any, Optional
from app.core.config import settings
import hashlib

logger = logging.getLogger(__name__)

class VectorStore: #向量检索

    def __init__( #理解为初始化一个对象，然后将字段的默认值赋值
        self,
        persist_dir: Optional[str] = None,
        collection_name: Optional[str] = None,
        embedding_function=None
    ):
        """
        初始化向量库客户端

        Args:
            persist_dir: 持久化目录，默认从 settings 读取
            collection_name: 集合名称，默认从 settings 读取
            embedding_function: 嵌入函数，默认使用 DefaultEmbeddingFunction
        """
        self.persist_dir = persist_dir or settings.CHROMA_PERSIST_DIR
        self.collection_name = collection_name or settings.CHROMA_COLLECTION

        self.client = chromadb.PersistentClient(path=self.persist_dir)

        if embedding_function is None:
            self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        else:
            self.embedding_function = embedding_function

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            embedding_function=self.embedding_function
        )
        logger.info(f"✅ 向量库已初始化: {self.persist_dir} / {self.collection_name}")

    def add_documents(
            self,
            documents: List[str],
            metadatas: Optional[List[Dict]] = None,
            ids: Optional[List[str]] = None
    ) -> List[str]:
        """插入文档（支持批量）"""
        if not documents:
            logger.warning("⚠️ 文档列表为空，跳过插入")
            return []
        
        if ids is None:
            ids = [hashlib.md5(doc.encode("utf-8")).hexdigest for doc in documents]

        if metadatas is None:
            metadatas = [{} for _ in documents]

        try:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            logger.info(f"✅ 成功插入 {len(documents)} 条文档")
            return ids
        except Exception as e:
            logger.error(f"❌ 插入文档失败: {e}")
            raise

    def retrieve(
    self,
    query: str,
    top_k: int=3,
    filter_metadata: Optional[Dict] = None      
    ) -> List[Dict[str, Any]]:
        try:
            query_param = {
                "query_texts": [query],
                "n_results": top_k,
                "include": ["documents", "metadatas", "distances"]
            }
            if filter_metadata: #新增一个字段默认值
                query_param["where"] = filter_metadata
            # 见test_retrieve.py 理解**的用法
            results = self.collection.query(**query_param)

            if not results["documents"] or not results["documents"][0]:
                return []
            
            formatted = []
            for i, doc in enumerate(results["documents"][0]):
                formatted.append({
                    "document": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "score": results["distances"][0][i] if results["distances"] else None
                })
            return formatted    
                    
        except Exception as e:
                logger.error(f"❌ 检索失败: {e}")
                return []    
        
    def count(self) -> int:
        """获取集合中文档总数"""
        try:
            return self.collection.count()
        except Exception as e:
            logger.error(f"❌ 获取数量失败: {e}")
            return 0    