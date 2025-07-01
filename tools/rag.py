# from langchain_community.tools import TavilySearchResults
from pydantic import BaseModel
from client.chroma import get_vector_store
from langchain_core.tools import tool, Tool
from util_ai.logger import logger

class RagCallArgs(BaseModel):
    user_question: str


def make_rag_call_tool(rag_chain):
    def _rag_tool(user_question: str) -> str:
        """Use this tool to answer questions about FOLLOWING TOPICS:
         - FIAT/THB: deposit,transaction
         - FIAT/THB: withdraw,transaction, fee
         - crypto deposit/withdraw,
         - trading,
         - KYC
         - downloading reports.
         Input is the user's message."""
        try:
            log.info("RAG call for message: %s", user_question)
            retrieved_docs = get_vector_store().similarity_search_with_score(
                query=user_question,
                k=1,
            )

            if not retrieved_docs:
             return "Sorry, I couldn't find any relevant documents for your query."

            doc_content = "\n\n".join(
                doc.page_content
                for doc,score in retrieved_docs
                if score >= 0.4)
            log.info(f"RAG content: {doc_content}")

            combined_input = {
                "user_question": user_question,
                "context": doc_content,
            }

            response = rag_chain.invoke(input=combined_input)
            log.info(f"llm response =: {response.content}")
            return str(response.content)
        except Exception as e:
            log.error(f"Error in rag_call: {str(e)}")
            raise

    return  Tool.from_function(
        name="rag_call",
        description="Retrieves information about MaxBit services",
        func=_rag_tool,
        args_schema=RagCallArgs,
        return_direct=True
    )


