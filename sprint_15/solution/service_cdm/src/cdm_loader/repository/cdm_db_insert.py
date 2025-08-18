from lib.pg import PgConnect
from cdm_loader.models import UserProductCounters, UserCategoryCounters


class DbInsert:
    def __init__(self, db: PgConnect) -> None:
        self._db = db

    def user_prod_insert(self, user_prod: UserProductCounters) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO cdm.user_product_counters (user_id, product_id, product_name, order_cnt)
                        VALUES (%(user_id)s, %(product_id)s, %(product_name)s, %(load_src)s)
                        ON CONFLICT (user_id, product_id) DO UPDATE
                        SET
                            order_cnt = order_cnt + EXCLUDED.order_cnt
                    """,
                    {
                        'user_id': user_prod.user_id,
                        'product_id': user_prod.product_id,
                        'product_name': user_prod.product_name,
                        'order_cnt': user_prod.order_cnt
                    }
                )

    def user_cat_insert(self, user_cat: UserCategoryCounters) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO cdm.user_category_counters (user_id, category_id, category_name, order_cnt)
                        VALUES (%(user_id)s, %(category_id)s, %(category_name)s, %(load_src)s)
                        ON CONFLICT (user_id, category_id) DO UPDATE
                        SET
                            order_cnt = order_cnt + EXCLUDED.order_cnt
                    """,
                    {
                        'user_id': user_cat.user_id,
                        'category_id': user_cat.category_id,
                        'category_name': user_cat.category_name,
                    }
                )