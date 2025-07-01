from typing import Any, Optional
from client.mysql import get_mysql_connection
from util_ai.logger import logger as log
def get_txn_from_db(txn_id: str) -> Optional[Any]:
    try:
        connection = get_mysql_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT status, reason from wallet_service.fiat_transaction where id = %s",
                (txn_id,)
            )
            txn = cursor.fetchone()
            log.info(f"Fetched transaction: {txn} for txn_id: {txn_id}")
        return txn
    except Exception as e:
        log.info(f"Error fetching transaction from DB for txn_id {txn_id}: {str(e)}")
        return None