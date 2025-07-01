from langchain.chat_models import init_chat_model
from template.prompt import rag_tool_prompt, txn_status_tool_prompt

llm = init_chat_model(model="gpt-4o")

rag_llm_chain = rag_tool_prompt | llm

txn_status_llm_chain = txn_status_tool_prompt | llm
#rag_llm_chain_history= create_chain_with_history(rag_llm_chain)










