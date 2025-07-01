from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.runnables import RunnableWithMessageHistory
from client.redis import get_history
from model.llm import llm, rag_llm_chain, txn_status_llm_chain
from template.prompt import  main_chat_prompt
from tools.rag import make_rag_call_tool
from tools.txn_status import make_check_txn_status_tool


def create_chain_with_history(chain):
    return RunnableWithMessageHistory(
        chain,
        get_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )

# create required tools
rag_tool = make_rag_call_tool(rag_llm_chain)
check_txn_status_tool = make_check_txn_status_tool(txn_status_llm_chain)

toools = [rag_tool, check_txn_status_tool]

agent_chain = create_openai_functions_agent(llm, toools,main_chat_prompt)

agent_executor = AgentExecutor(
    agent=agent_chain,
    tools=toools,
    handle_parsing_errors=True,
)

chain_with_history = create_chain_with_history(agent_executor)

# rag_call = make_rag_call_tool(chain_with_history)
# tools = [rag_call]



