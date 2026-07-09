# scripts/evaluate_rag.py
import sys
import types

# ===== 猴子补丁：拦截 ragas 旧导入 =====
fake_module = types.ModuleType('langchain_community.chat_models.vertexai')
class DummyChatVertexAI:
    def __init__(self, *args, **kwargs):
        pass
    def __call__(self, *args, **kwargs):
        return "Dummy response"
fake_module.ChatVertexAI = DummyChatVertexAI
sys.modules['langchain_community.chat_models.vertexai'] = fake_module

# ===== 正常导入 =====
import json
import logging
import os
from pathlib import Path
from datasets import Dataset
from ragas import evaluate

# ===== 导入可用指标（函数形式，不需要 llm 参数） =====
from ragas.metrics import faithfulness, answer_relevancy
metrics = [faithfulness, answer_relevancy]
print("✅ 使用 faithfulness 和 answer_relevancy（函数形式）")

# 本地 LLM 和 Embeddings
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from ragas.llms import LangchainLLMWrapper
from app.rag.vector_store import VectorStore

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_test_data():
    test_file = Path(__file__).parent.parent / "data" / "test_questions.json"
    with open(test_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    logger.info(f"✅ 加载测试集: {len(data)} 个问题")
    return data

def get_ragas_llm():
    model_name = os.getenv("RAGAS_LLM_MODEL", "mistral:7b")
    try:
        llm = Ollama(model=model_name, temperature=0, timeout=180)
        return LangchainLLMWrapper(llm)
    except Exception as e:
        logger.error(f"❌ Ollama LLM 连接失败: {e}")
        raise

def get_ragas_embeddings():
    model_name = os.getenv("RAGAS_EMBEDDING_MODEL", "nomic-embed-text")
    try:
        embeddings = OllamaEmbeddings(model=model_name)
        logger.info(f"✅ 使用 Ollama 嵌入模型: {model_name}")
        return embeddings
    except Exception as e:
        logger.error(f"❌ Ollama 嵌入模型初始化失败: {e}")
        raise

def run_evaluation():
    test_data = load_test_data()
    vs = VectorStore()
    logger.info(f"📊 向量库文档总数: {vs.count()}")

    questions, contexts, answers, ground_truths = [], [], [], []

    for item in test_data:
        q = item["question"]
        gt = item["ground_truth"]
        docs = vs.retrieve(q, top_k=3)
        if docs:
            retrieved_docs = [d["document"] for d in docs]
            answer = docs[0]["document"][:500] if docs[0]["document"] else "无答案"
        else:
            retrieved_docs = []
            answer = "未检索到相关资料"
        questions.append(q)
        ground_truths.append(gt)
        contexts.append(retrieved_docs)
        answers.append(answer)
        logger.info(f"📝 问题: {q[:30]}... -> 检索到 {len(retrieved_docs)} 条")

    dataset = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    })

    ragas_llm = get_ragas_llm()
    ragas_embeddings = get_ragas_embeddings()

    logger.info("🔄 开始 RAGAS 评估...")
    result = evaluate(
        dataset=dataset,
        metrics=metrics,
        llm=ragas_llm,
        embeddings=ragas_embeddings
    )

    if hasattr(result, "_scores_dict"):
        scores_dict = result._scores_dict
    elif hasattr(result, "scores"):
        scores_dict = result.scores
    else:
        scores_dict = {k: v for k, v in result.items() if isinstance(v, list)}

    logger.info("=" * 50)
    logger.info("📊 RAGAS 评估结果：")
    for metric_name, score_list in scores_dict.items():
        if isinstance(score_list, list) and score_list:
            avg_score = sum(score_list) / len(score_list)
            logger.info(f"   {metric_name}: {avg_score:.4f}")
        else:
            logger.info(f"   {metric_name}: {score_list}")

    output_dir = Path(__file__).parent.parent / "docs"
    output_dir.mkdir(exist_ok=True)
    report_file = output_dir / "ragas_report.md"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# RAGAS 评估报告\n\n")
        f.write("| 指标 | 平均分 |\n")
        f.write("| :--- | :--- |\n")
        for metric_name, score_list in scores_dict.items():
            if isinstance(score_list, list) and score_list:
                avg_score = sum(score_list) / len(score_list)
                f.write(f"| {metric_name} | {avg_score:.4f} |\n")
            else:
                f.write(f"| {metric_name} | {score_list} |\n")
        f.write("\n## 备注\n\n")
        f.write("`context_relevancy` 在当前 RAGAS 版本中不可用，因此仅评估 `faithfulness` 和 `answer_relevancy`。\n")
    logger.info(f"✅ 评估报告已保存: {report_file}")
    return result

if __name__ == "__main__":
    run_evaluation()