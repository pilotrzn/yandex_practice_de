from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel


class CarStatus(StrEnum):
    available = "available"
    reserve = "reserve"
    sold = "sold"
    delivery = "delivery"


class Car(BaseModel):
    vin: str
    model: int
    price: Decimal
    date_start: datetime
    status: CarStatus

    def index(self) -> str:
        return self.vin

    def make_string(self):
        return (self.vin, self.model, self.price, self.date_start, self.status)

    @classmethod
    def make_object_from_record(cls, record: str):
        data = record.strip().split(";")
        return cls(
            vin=data[0],
            model=int(data[1]),
            price=Decimal(data[2]),
            date_start=datetime.strptime(data[3], '%Y-%m-%d %X'),
            status=CarStatus(data[4])
        )


class Model(BaseModel):
    id: int
    name: str
    brand: str

    def index(self) -> str:
        return str(self.id)

    def make_string(self):
        return (self.id, self.name, self.brand)

    @classmethod
    def make_object_from_record(cls, record: str):
        data = record.strip().split(";")
        return cls(
            id=int(data[0]),
            name=data[1],
            brand=data[2]
        )


class Sale(BaseModel):
    sales_number: str
    car_vin: str
    sales_date: datetime
    cost: Decimal
    is_deleted: bool = False

    def index(self) -> str:
        return self.car_vin

    def make_string(self):
        return (
            self.sales_number,
            self.car_vin,
            self.sales_date,
            self.cost,
            self.is_deleted
            )

    @classmethod
    def make_object_from_record(cls, record: str):
        data = record.strip().split(";")
        return cls(
            sales_number=data[0],
            car_vin=data[1],
            sales_date=datetime.strptime(data[2], '%Y-%m-%d %X'),
            cost=Decimal(data[3]),
            is_deleted=bool(data[4])
        )


class CarFullInfo(BaseModel):
    vin: str
    car_model_name: str
    car_model_brand: str
    price: Decimal
    date_start: datetime
    status: CarStatus
    sales_date: datetime | None
    sales_cost: Decimal | None


class ModelSaleStats(BaseModel):
    car_model_name: str
    brand: str
    sales_number: int
