from typing import TypedDict
from typing_extensions import Literal
from langgraph.graph import StateGraph, END

#定义状态 一个全局的map集合
class MyState(TypedDict):
    user_input: str
    processed:str
    final_answer:str

#定义节点
def node_parse(state: MyState):
    # 处理用户输入
    return {"result": f"解析了: {state['user_input']}"}

def node_validate(state: MyState):
    # 验证处理结果
    return {"result": f"验证了: {state['processed']}"}

def node_generate(state: MyState):
    # 生成最终答案
    return {"result": f"生成了: {state['final_answer']}"}

def route_by_task(state: MyState) -> Literal["parse", "validate", "generate"]:
    task = state.get("processed","解析")
    if task == "解析":
        return "parse"
    elif task == "验证":
        return "validate"
    else:
        return "generate"
    
builder = StateGraph(MyState)

# 告诉框架从哪个节点开始执行
builder.set_entry_point("parse")   # ✅ 这就是“开始指令”

builder.add_node("parse", node_parse)
builder.add_node("validate", node_validate)
builder.add_node("generate", node_generate)

# 从 parse 节点出发，走条件路由
builder.add_conditional_edges("parse", route_by_task)

builder.add_edge("parse", END)
builder.add_edge("validate", END)
builder.add_edge("generate", END)

graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({"user_input": "Excel数据", "processed": "校验", "final_answer": "最终结果"})
    print(result)