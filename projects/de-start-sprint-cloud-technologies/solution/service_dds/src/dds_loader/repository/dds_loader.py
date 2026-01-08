from typing import Dict, Any, List
from datetime import datetime
import uuid
from dds_loader.models import (
    HubOrder, HubCategory, HubProduct, HubRestaurant, HubUser,
    LinkOrderProduct, LinkOrderUser, LinkProductCategory,
    LinkProductRestaurant, SatOrderCost, SatOrderStatus, SatProductNames,
    SatRestaurantNames, SatUserNames
    )


class Loader:
    def __init__(self, dict: Dict, source_system: str) -> None:
        self._dict = dict
        self.source_system = source_system
        self.order_ns_uuid = uuid.UUID('')

    def _uuid_generator(self, obj: Any) -> uuid.UUID:
        return uuid.uuid5(self.order_ns_uuid, name=str(obj))

    def hub_user(self) -> HubUser:
        user_id = self._dict['user']['id']
        return HubUser(
            h_user_pk=self._uuid_generator(user_id),
            user_id=user_id,
            load_dt=datetime.now(),
            load_src=self.source_system
        )

    def hub_restaurant(self) -> HubRestaurant:
        rest_id = self._dict['restaurant']['id']
        return HubRestaurant(
            h_restaurant_pk=self._uuid_generator(rest_id),
            restaurant_id=rest_id,
            load_dt=datetime.now(),
            load_src=self.source_system
        )

    def hub_product(self) -> List[HubProduct]:
        products: List[HubProduct] = []
        for product in self._dict['products']:
            product_id = product['id']
            products.append(
                HubProduct(
                    h_product_pk=self._uuid_generator(product_id),
                    product_id=product_id,
                    load_dt=datetime.now(),
                    load_src=self.source_system
                )
            )
        return products

    def hub_category(self) -> List[HubCategory]:
        categories: List[HubCategory] = []
        for product in self._dict['products']:
            category_name = product['category']
            categories.append(
                HubCategory(
                    h_category_pk=self._uuid_generator(category_name),
                    category_name=category_name,
                    load_dt=datetime.now(),
                    load_src=self.source_system
                )
            )
        return categories

    def hub_order(self) -> HubOrder:
        order_id = self._dict['object_id']
        return HubOrder(
            h_order_pk=self._uuid_generator(order_id),
            order_id=order_id,
            order_dt=self._dict['date'],
            load_dt=datetime.now(),
            load_src=self.source_system
        )

    def link_order_user(self) -> LinkOrderUser:
        h_order_pk = self._uuid_generator(self._dict['object_id'])
        h_user_pk = self._uuid_generator(self._dict['user']['id'])
        return LinkOrderUser(
            hk_order_user_pk=self._uuid_generator([h_order_pk, h_user_pk]),
            h_order_pk=h_order_pk,
            h_user_pk=h_user_pk,
            load_dt=datetime.now(),
            load_src=self.source_system
        )

    def link_order_product(self) -> List[LinkOrderProduct]:
        h_order_pk = self._uuid_generator(self._dict['object_id'])
        order_products: List[LinkOrderProduct] = []
        for product in self._dict['products']:
            h_product_pk = self._uuid_generator(product['id'])
            order_products.append(
                LinkOrderProduct(
                    hk_order_product_pk=self._uuid_generator(
                        [h_order_pk, h_product_pk]),
                    h_order_pk=h_order_pk,
                    h_product_pk=h_product_pk,
                    load_dt=datetime.now(),
                    load_src=self.source_system
                )
            )
        return order_products

    def link_product_restaurant(self) -> List[LinkProductRestaurant]:
        h_restaurant_pk = self._uuid_generator(self._dict['restaurant']['id'])
        product_restaurants: List[LinkProductRestaurant] = []
        for product in self._dict['products']:
            h_product_pk = self._uuid_generator(product['id'])
            product_restaurants.append(
                LinkProductRestaurant(
                    hk_product_restaurant_pk=self._uuid_generator(
                        [h_restaurant_pk, h_product_pk]),
                    h_restaurant_pk=h_restaurant_pk,
                    h_product_pk=h_product_pk,
                    load_dt=datetime.now(),
                    load_src=self.source_system
                )
            )
        return product_restaurants

    def link_product_category(self) -> List[LinkProductCategory]:
        products_categories: List[LinkProductCategory] = []
        for product in self._dict['products']:
            h_category_pk = self._uuid_generator(product['category'])
            h_product_pk = self._uuid_generator(product['id'])
            products_categories.append(
                LinkProductCategory(
                    hk_product_category_pk=self._uuid_generator(
                        [h_category_pk, h_product_pk]),
                    h_category_pk=h_category_pk,
                    h_product_pk=h_product_pk,
                    load_dt=datetime.now(),
                    load_src=self.source_system
                )
            )
        return products_categories

    def sat_product_names(self) -> List[SatProductNames]:
        product_names: List[SatProductNames] = []
        for product in self._dict['products']:
            h_product_pk = self._uuid_generator(product['id'])
            product_names.append(
                SatProductNames(
                    h_product_pk=h_product_pk,
                    name=product['name'],
                    load_dt=datetime.now(),
                    load_src=self.source_system,
                    hk_product_names_hashdiff=self._uuid_generator(
                        product['name'])
                )
            )
        return product_names

    def sat_restaurant_names(self) -> SatRestaurantNames:
        h_restaurant_pk = self._uuid_generator(self._dict['restaurant']['id'])
        rest_name = self._dict['restaurant']['name']
        return SatRestaurantNames(
            h_restaurant_pk=h_restaurant_pk,
            name=rest_name,
            load_dt=datetime.now(),
            load_src=self.source_system,
            hk_restaurant_names_hashdiff=self._uuid_generator(rest_name)
        )

    def sat_user_names(self) -> SatUserNames:
        h_user_pk = self._uuid_generator(self._dict['user']['id'])
        username = self._dict['user']['name']
        userlogin = self._dict['user']['login']
        return SatUserNames(
            h_user_pk=h_user_pk,
            username=username,
            userlogin=userlogin,
            load_dt=datetime.now(),
            load_src=self.source_system,
            hk_user_names_hashdiff=self._uuid_generator(
                [username, userlogin])
        )

    def sat_order_status(self) -> SatOrderStatus:
        h_order_pk = self._uuid_generator(self._dict['object_id'])
        status = self._dict['status']
        return SatOrderStatus(
            h_order_pk=h_order_pk,
            status=status,
            load_dt=datetime.now(),
            load_src=self.source_system,
            hk_order_status_hashdiff=self._uuid_generator(status)
        )

    def sat_order_cost(self) -> SatOrderCost:
        h_order_pk = self._uuid_generator(self._dict['object_id'])
        cost = self._dict['cost']
        payment = self._dict['payment']
        return SatOrderCost(
            h_order_pk=h_order_pk,
            cost=cost,
            payment=payment,
            load_dt=datetime.now(),
            load_src=self.source_system,
            hk_order_cost_hashdiff=self._uuid_generator([cost, payment])
        )

    def gen_output_message(self) -> Dict:
        h_user_pk = self._uuid_generator(self._dict['user']['id'])

        products_data = []

        for product in self._dict['products']:
            h_product_pk = self._uuid_generator(product['id'])
            h_category_pk = self._uuid_generator(product['category'])
            products_data.append(
                {
                    'product_id': h_product_pk,
                    'product_name': product['name'],
                    'product_cnt': int(product['quantity']),
                    'category_id': h_category_pk,
                    'category_name': product['category'],
                    'category_cnt': 1
                    }
                    )

        output_message = {
            'object_id': self._dict['object_id'],
            'payload': {
                'user_id': h_user_pk,
                'products': products_data
            }
        }

        return output_message
