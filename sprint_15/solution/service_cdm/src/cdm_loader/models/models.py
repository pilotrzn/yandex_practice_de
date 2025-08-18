import uuid
from pydantic import BaseModel


class UserProductCounters(BaseModel):
    user_id: uuid.UUID
    product_id: uuid.UUID
    product_name: str
    order_cnt: int


class UserCategoryCounters(BaseModel):
    user_id: uuid.UUID
    category_id: uuid.UUID
    category_name: str
    order_cnt: int
