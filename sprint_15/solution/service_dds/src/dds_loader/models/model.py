import uuid
from datetime import datetime
from pydantic import BaseModel


class HubUser(BaseModel):
    h_user_pk: uuid.UUID
    user_id: str
    load_dt: datetime
    load_src: str


class HubRestaurant(BaseModel):
    h_restaurant_pk: uuid.UUID
    restaurant_id: str
    load_dt: datetime
    load_src: str


class HubProduct(BaseModel):
    h_product_pk: uuid.UUID
    product_id: str
    load_dt: datetime
    load_src: str


class HubCategory(BaseModel):
    h_category_pk: uuid.UUID
    category_name: str
    load_dt: datetime
    load_src: str


class HubOrder(BaseModel):
    h_order_pk: uuid.UUID
    order_id: str
    order_dt: datetime
    load_dt: datetime
    load_src: str


# dds.l_order_product
class LinkOrderProduct(BaseModel):
    hk_order_product_pk: uuid.UUID
    h_order_pk: uuid.UUID
    h_product_pk: uuid.UUID
    load_dt: datetime
    load_src: str


# dds.l_order_user
class LinkOrderUser(BaseModel):
    hk_order_user_pk: uuid.UUID
    h_order_pk: uuid.UUID
    h_user_pk: uuid.UUID
    load_dt: datetime
    load_src: str


# dds.l_product_restaurant
class LinkProductRestaurant(BaseModel):
    hk_product_restaurant_pk: uuid.UUID
    h_restaurant_pk: uuid.UUID
    h_product_pk: uuid.UUID
    load_dt: datetime
    load_src: str


# dds.l_product_category
class LinkProductCategory(BaseModel):
    hk_product_category_pk: uuid.UUID
    h_category_pk: uuid.UUID
    h_product_pk: uuid.UUID
    load_dt: datetime
    load_src: str


# dds.s_product_names
class SatProductNames(BaseModel):
    h_product_pk: uuid.UUID
    name: str
    load_dt: datetime
    load_src: str
    hk_product_names_hashdiff: uuid.UUID


# dds.s_restaurant_names
class SatRestaurantNames(BaseModel):
    h_restaurant_pk: uuid.UUID
    name: str
    load_dt: datetime
    load_src: str
    hk_restaurant_names_hashdiff: uuid.UUID


# dds.s_user_names
class SatUserNames(BaseModel):
    h_user_pk: uuid.UUID
    username: str
    userlogin: str
    load_dt: datetime
    load_src: str
    hk_user_names_hashdiff: uuid.UUID


# dds.s_order_status
class SatOrderStatus(BaseModel):
    h_order_pk: uuid.UUID
    status: str
    load_dt: datetime
    load_src: str
    hk_order_status_hashdiff: uuid.UUID


# dds.s_order_cost
class SatOrderCost(BaseModel):
    h_order_pk: uuid.UUID
    cost: float
    payment: float
    load_dt: datetime
    load_src: str
    hk_order_cost_hashdiff: uuid.UUID