from langchain_core.tools import Tool
from pydantic import BaseModel
from util_ai.logger import logger as log
from service.mysql_service import get_txn_from_db

class TxnStatusCallArgs(BaseModel):
    txn_id: str

def make_check_txn_status_tool(txn_chain):
    def _txn_status_tool(txn_id: str) -> str:

        """
        Check txn status or status of a transaction by its ID.
        Args:
            txn_id (str): The ID of the transaction to check status.
        Returns:
            str: The status of the transaction or an error message if not found.
        """
        try:
            log.info(f"Checking transaction status for ID: {txn_id}")
            txn = get_txn_from_db(txn_id)
            if txn is None:
                return "Transaction not found"

            status, reason = txn
            log.info(f"status: {status} and reason: {reason}")

            response = txn_chain.invoke(input={"status": status})
            log.info(f"llm response =: {response.content}")
            return str(response.content)
        except Exception as e:
            log.error(f"Error in check_txn_status: {str(e)}")
            raise

    return  Tool.from_function(
        name="check_txn_status",
        description="check the status of a transaction by its ID",
        func=_txn_status_tool,
        args_schema=TxnStatusCallArgs,
        return_direct=True
    )