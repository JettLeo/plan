from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
import logging
import sqlite3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AgentState(TypedDict):
    user_request: str
    steps: list          # 步骤列表，如 ["解析Excel", "校验数据", "生成报告"]
    current_step_index: int   # 当前执行的步骤索引（从 0 开始）
    work_result: str
    final_output: str

def planner_node(state: AgentState) -> dict:
    """根据用户请求生成执行步骤列表"""
    request = state.get("user_request", "")
    logging.info("Planner 收到请求: %s", request)
    # 简单规则：根据关键词生成步骤
    if "解析" in request and "校验" in request:
        steps = ["解析Excel", "校验数据"]
    elif "解析" in request:
        steps = ["解析Excel"]
    elif "校验" in request:
        steps = ["校验数据"]
    else:
        steps = ["解析Excel", "校验数据"]  # 默认全流程

    logging.info("Planner 生成步骤: %s", steps)

    return {
        "steps": steps,
        "current_step_index": 0
    }

def executor_node(state: AgentState) -> dict:
    """执行当前步骤"""
    logging.info("executor_node 收到的 state keys: %s", state.keys())
    # steps = state.get("steps", [])
    steps = state["steps"]
    idx = state.get("current_step_index", 0)

    # 检查是否所有步骤都已完成
    if idx >= len(steps):
        return {"final_output": "所有步骤执行完成"}

    current_step = steps[idx]
    logging.info("执行步骤 %d/%d: %s", idx + 1, len(steps), current_step)

    #根据步骤名称执行对应逻辑
    if current_step == "解析Excel":
        result = "✅ 解析成功：读取了 3 行数据"
    elif current_step == "校验数据":
        result = "✅ 校验通过：3 行数据全部有效"
    else:
        result = f"✅ 执行完成：{current_step}"

    return {
        "work_result": result,
        "current_step_index": idx + 1  # 更新索引，准备执行下一步
    }

def final_aggregator(state: AgentState) -> dict:
    """汇总结果"""
    # return {"final_output": f"【完成】{state['work_result']}"}
    return {"final_output": f"【完成】{state.get('work_result', '无结果')}"}

def route_after_executor(state: AgentState) -> Literal["executor_node", "aggregator"]:
    # steps = state.get("steps", [])
    steps = state["steps"]
    idx = state.get("current_step_index", 0)

    if idx < len(steps):
        logging.info("还有下一步，继续执行 executor_node")
        return "executor_node"
    else:
        logging.info("所有步骤完成，跳转到 aggregator")
        return "aggregator"
    
builder = StateGraph(AgentState)
builder.add_node("planner", planner_node)
builder.add_node("executor_node", executor_node)
builder.add_node("aggregator", final_aggregator)

builder.set_entry_point("planner")
builder.add_edge("planner", "executor_node")
builder.add_conditional_edges("executor_node", route_after_executor)
builder.add_edge("aggregator", END)


conn = sqlite3.connect("plan_execute_checkpoints.db", check_same_thread=False)
memory = SqliteSaver(conn)
graph = builder.compile(checkpointer=memory)

# ========== 8. 运行测试 ==========
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "session_001"}}
    
    # 测试：用户请求包含"解析"和"校验"
    result = graph.invoke(
        {"user_request": "请解析这份Excel并校验数据"},
        config=config
    )
    logging.info("最终结果: %s", result.get("final_output"))
    
    # 查看 State 中的执行记录
    current = graph.get_state(config)
    logging.info("执行步骤: %s", current.values.get("steps"))
    logging.info("当前索引: %d", current.values.get("current_step_index"))
    logging.info("最终结果: %s", current.values.get("final_output"))
