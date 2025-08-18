from lib.pg import PgConnect
from datetime import datetime
import json
import logging


class StgRepository:
    def __init__(self, db: PgConnect) -> None:
        self._db = db

    def order_events_insert(self,
                            object_id: int,
                            object_type: str,
                            sent_dttm: datetime,
                            payload: dict) -> None:

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        """
                        INSERT INTO stg.order_events
                            (object_id, payload, object_type, sent_dttm)
                        VALUES (%(object_id)s, %(payload)s::json, %(object_type)s, %(sent_dttm)s)
                        ON CONFLICT (object_id) DO UPDATE
                        SET
                            object_type = EXCLUDED.object_type,
                            sent_dttm = EXCLUDED.sent_dttm,
                            payload = EXCLUDED.payload;
                        """,
                        {
                            'object_id': object_id,
                            'object_type': object_type,
                            'sent_dttm': sent_dttm,
                            'payload': json.dumps(payload, ensure_ascii=False)
                        }
                    )
                except Exception as e:
                    logging.error(f"Database error: {e}")
                    logging.error(f"Problematic payload: {payload}")
                    raise
