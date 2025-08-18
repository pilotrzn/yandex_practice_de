from typing import Dict, List
from cdm_loader.models import UserProductCounters, UserCategoryCounters


class Loader:
    def __init__(self, dict: Dict) -> None:
        self._dict = dict

    def user_product_counters(self) -> List[UserProductCounters]:
        user_id = self._dict['user_id']
        prod_counter: List[UserProductCounters] = []

        for product in self._dict['products']:
            prod_counter.append(
                UserProductCounters(
                    user_id=user_id,
                    product_id=product['product_id'],
                    product_name=product['product_name'],
                    order_cnt=product['product_cnt']
                )
            )
        return prod_counter

    def user_category_counters(self) -> List[UserCategoryCounters]:
        user_id = self._dict['user_id']
        cat_counter: List[UserCategoryCounters] = []
        for product in self._dict['products']:
            cat_counter.append(
                UserCategoryCounters(
                    user_id=user_id,
                    category_id=product['category_id'],
                    category_name=product['category_id'],
                    order_cnt=product['category_cnt']
                )
            )
        return cat_counter
