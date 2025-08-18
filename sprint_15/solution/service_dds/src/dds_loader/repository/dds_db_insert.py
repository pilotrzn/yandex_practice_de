from lib.pg import PgConnect
from dds_loader.models import (
    HubOrder, HubCategory, HubProduct, HubRestaurant, HubUser,
    LinkOrderProduct, LinkOrderUser, LinkProductCategory,
    LinkProductRestaurant, SatOrderCost, SatOrderStatus, SatProductNames,
    SatRestaurantNames, SatUserNames
    )


class DbInsert:
    def __init__(self, db: PgConnect) -> None:
        self._db = db

    def hub_user_insert(self, hub_user: HubUser) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.h_user
                            (h_user_pk, user_id, load_dt, load_src)
                        VALUES (%(h_user_pk)s, %(user_id)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (h_user_pk) DO UPDATE
                        SET
                            user_id = EXCLUDED.user_id,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'h_user_pk': hub_user.h_user_pk,
                        'user_id': hub_user.user_id,
                        'load_dt': hub_user.load_dt,
                        'load_src': hub_user.load_src
                    }
                )

    def hub_restaurant_insert(self, hub_restaurant: HubRestaurant) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.h_restaurant
                            (h_restaurant_pk, restaurant_id, load_dt, load_src)
                        VALUES (%(h_restaurant_pk)s, %(restaurant_id)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (h_restaurant_pk) DO UPDATE
                        SET
                            restaurant_id = EXCLUDED.restaurant_id,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'h_restaurant_pk': hub_restaurant.h_restaurant_pk,
                        'restaurant_id': hub_restaurant.restaurant_id,
                        'load_dt': hub_restaurant.load_dt,
                        'load_src': hub_restaurant.load_src
                    }
                )

    def hub_product_insert(self, hub_product: HubProduct) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.h_product
                            (h_product_pk, product_id, load_dt, load_src)
                        VALUES (%(h_product_pk)s, %(product_id)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (h_product_pk) DO UPDATE
                        SET
                            product_id = EXCLUDED.product_id,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'h_product_pk': hub_product.h_product_pk,
                        'product_id': hub_product.product_id,
                        'load_dt': hub_product.load_dt,
                        'load_src': hub_product.load_src
                    }
                )

    def hub_category_insert(self, hub_category: HubCategory) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.h_category
                            (h_category_pk, category_id, load_dt, load_src)
                        VALUES (%(h_category_pk)s, %(category_id)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (h_category_pk) DO UPDATE
                        SET
                            category_id = EXCLUDED.category_id,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'h_category_pk': hub_category.h_category_pk,
                        'category_id': hub_category.category_id,
                        'load_dt': hub_category.load_dt,
                        'load_src': hub_category.load_src
                    }
                )

    def hub_order_insert(self, hub_order: HubOrder) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.h_order
                            (h_order_pk, order_id, order_dt, load_dt, load_src)
                        VALUES (%(h_order_pk)s, %(order_id)s, %(order_dt)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (h_order_pk) DO UPDATE
                        SET
                            order_id = EXCLUDED.order_id,
                            order_dt = EXCLUDED.order_dt,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'h_order_pk': hub_order.h_order_pk,
                        'order_id': hub_order.order_id,
                        'order_dt': hub_order.order_dt,
                        'load_dt': hub_order.load_dt,
                        'load_src': hub_order.load_src
                    }
                )

    def link_order_product_insert(self, link_order_product: LinkOrderProduct) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.l_order_proudct
                            (hk_order_product_pk, h_order_pk, h_product_pk, load_dt, load_src)
                        VALUES (%(hk_order_product_pk)s, %(h_order_pk)s, %(h_product_pk)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (hk_order_product_pk) DO UPDATE
                        SET
                            h_order_pk = EXCLUDED.h_order_pk,
                            h_product_pk = EXCLUDED.h_product_pk,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'hk_order_product_pk': link_order_product.hk_order_product_pk,
                        'h_order_pk': link_order_product.h_order_pk,
                        'h_product_pk': link_order_product.h_product_pk,
                        'load_dt': link_order_product.load_dt,
                        'load_src': link_order_product.load_src
                    }
                )

    def link_order_user_insert(self, link_order_user: LinkOrderUser) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.l_order_user
                            (hk_order_user_pk, h_order_pk, h_user_pk, load_dt, load_src)
                        VALUES (%(hk_order_user_pk)s, %(h_order_pk)s, %(h_user_pk)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (hk_order_user_pk) DO UPDATE
                        SET
                            h_order_pk = EXCLUDED.h_order_pk,
                            h_user_pk = EXCLUDED.h_user_pk,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'hk_order_user_pk': link_order_user.hk_order_user_pk,
                        'h_order_pk': link_order_user.h_order_pk,
                        'h_user_pk': link_order_user.h_user_pk,
                        'load_dt': link_order_user.load_dt,
                        'load_src': link_order_user.load_src
                    }
                )

    def link_prod_rest_insert(self, link_prod_rest: LinkProductRestaurant) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.l_proudct_restaurant 
                            (hk_product_restaurant_pk, h_restaurant_pk, h_product_pk, load_dt, load_src)
                        VALUES (%(hk_product_restaurant_pk)s, %(h_restaurant_pk)s, %(h_product_pk)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (hk_product_restaurant_pk) DO UPDATE
                        SET
                            h_restaurant_pk = EXCLUDED.h_restaurant_pk,
                            h_product_pk = EXCLUDED.h_product_pk,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'hk_product_restaurant_pk': link_prod_rest.hk_product_restaurant_pk,
                        'h_restaurant_pk': link_prod_rest.h_restaurant_pk,
                        'h_product_pk': link_prod_rest.h_product_pk,
                        'load_dt': link_prod_rest.load_dt,
                        'load_src': link_prod_rest.load_src
                    }
                )

    def link_prod_category_insert(self, link_prod_category: LinkProductCategory) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.l_proudct_category
                            (hk_product_category_pk, h_category_pk, h_product_pk, load_dt, load_src)
                        VALUES (%(hk_product_category_pk)s, %(h_category_pk)s, %(h_product_pk)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (hk_product_category_pk) DO UPDATE
                        SET
                            h_category_pk = EXCLUDED.h_category_pk,
                            h_product_pk = EXCLUDED.h_product_pk,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src
                    """,
                    {
                        'hk_product_category_pk': link_prod_category.hk_product_category_pk,
                        'h_category_pk': link_prod_category.h_category_pk,
                        'h_product_pk': link_prod_category.h_product_pk,
                        'load_dt': link_prod_category.load_dt,
                        'load_src': link_prod_category.load_src
                    }
                )

    def sat_product_names_insert(self, sat_product_names: SatProductNames) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.s_product_names
                            (h_product_pk, name, load_dt, load_src, hk_product_names_hashdiff)
                        VALUES (%(h_product_pk)s, %(name)s, %(load_dt)s, %(load_src)s, %(hk_product_names_hashdiff)s)
                        ON CONFLICT (h_product_pk) DO UPDATE
                        SET
                            name = EXCLUDED.name,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src,
                            hk_product_names_hashdiff = EXCLUDED.hk_product_names_hashdiff
                    """,
                    {
                        'h_product_pk': sat_product_names.h_product_pk,
                        'name': sat_product_names.name,
                        'load_dt': sat_product_names.load_dt,
                        'load_src': sat_product_names.load_src, 
                        'hk_product_names_hashdiff': sat_product_names.hk_product_names_hashdiff
                    }
                )

    def sat_restaurant_names_insert(self, sat_restaurant_name: SatRestaurantNames) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.s_restaurant_names
                            (h_restaurant_pk, name, load_dt, load_src, hk_restaurant_names_hashdiff)
                        VALUES (%(h_restaurant_pk)s, %(name)s, %(load_dt)s, %(load_src)s, %(hk_restaurant_names_hashdiff)s)
                        ON CONFLICT (h_restaurant_pk) DO UPDATE
                        SET
                            name = EXCLUDED.name,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src,
                            hk_restaurant_names_hashdiff = EXCLUDED.hk_restaurant_names_hashdiff
                    """,
                    {
                        'h_restaurant_pk': sat_restaurant_name.h_restaurant_pk,
                        'name': sat_restaurant_name.name,
                        'load_dt': sat_restaurant_name.load_dt,
                        'load_src': sat_restaurant_name.load_src,
                        'hk_restaurant_names_hashdiff': sat_restaurant_name.hk_restaurant_names_hashdiff
                    }
                )

    def sat_user_names_insert(self, sat_user_name: SatUserNames) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.s_user_names
                            (h_user_pk, username, userlogin, load_dt, load_src, hk_user_names_hashdiff)
                        VALUES (%(h_user_pk)s, %(username)s, %(userlogin)s, %(load_dt)s, %(load_src)s, %(hk_user_names_hashdiff)s)
                        ON CONFLICT (h_user_pk) DO UPDATE
                        SET
                            username = EXCLUDED.username,
                            userlogin = EXCLUDED.userlogin,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src,
                            hk_user_names_hashdiff = EXCLUDED.hk_user_names_hashdiff
                    """,
                    {
                        'h_user_pk': sat_user_name.h_user_pk,
                        'username': sat_user_name.username,
                        'userlogin': sat_user_name.userlogin,
                        'load_dt': sat_user_name.load_dt,
                        'load_src': sat_user_name.load_src, 
                        'hk_user_names_hashdiff': sat_user_name.hk_user_names_hashdiff
                    }
                )

    def sat_order_status_insert(self, sat_order_status: SatOrderStatus) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.s_order_status
                            (h_order_pk, status, load_dt, load_src, hk_order_status_hashdiff)
                        VALUES (%(h_order_pk)s, %(status)s, %(load_dt)s, %(load_src)s, %(hk_order_status_hashdiff)s)
                        ON CONFLICT (h_order_pk) DO UPDATE
                        SET
                            status = EXCLUDED.status,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src,
                            hk_order_status_hashdiff = EXCLUDED.hk_order_status_hashdiff
                    """,
                    {
                        'h_order_pk': sat_order_status.h_order_pk,
                        'status': sat_order_status.status,
                        'load_dt': sat_order_status.load_dt,
                        'load_src': sat_order_status.load_src, 
                        'hk_order_status_hashdiff': sat_order_status.hk_order_status_hashdiff
                    }
                )

    def sat_order_cost_insert(self, sat_order_cost: SatOrderCost) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                        INSERT INTO dds.s_order_cost
                            (h_order_pk, cost, payment, load_dt, load_src, hk_order_cost_hashdiff)
                        VALUES (%(h_order_pk)s, %(cost)s, %(payment)s, %(load_dt)s, %(load_src)s, %(hk_order_cost_hashdiff)s)
                        ON CONFLICT (h_order_pk) DO UPDATE
                        SET
                            cost = EXCLUDED.cost,
                            payment = EXCLUDED.payment,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src,
                            hk_order_cost_hashdiff = EXCLUDED.hk_order_cost_hashdiff
                    """,
                    {
                        'h_order_pk': sat_order_cost.h_order_pk,
                        'cost': sat_order_cost.cost,
                        'payment': sat_order_cost.payment,
                        'load_dt': sat_order_cost.load_dt,
                        'load_src': sat_order_cost.load_src,
                        'hk_order_status_hashdiff': sat_order_cost.hk_order_cost_hashdiff
                    }
                )
