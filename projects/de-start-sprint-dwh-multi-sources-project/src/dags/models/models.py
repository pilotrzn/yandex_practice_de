from pydantic import BaseModel
from datetime import datetime, date, time
from decimal import Decimal as dec
from typing import Dict


class CourierObj(BaseModel):
    id: int
    courier_id: str
    courier_name: str


class DeliveryObj(BaseModel):
    id: int
    delivery_id: str
    courier_id: str
    delivery_ts_id: int
    address: str


class EtlSetting(BaseModel):
    id: int
    workflow_key: str
    workflow_settings: Dict


class TimestampObject(BaseModel):
    id: int
    ts: datetime
    year: int
    month: int
    day: int
    date: date
    time: time


class DeliveryFactObj(BaseModel):
    id: int
    delivery_id: int
    order_id: int
    sum: dec
    tip_sum: dec
    rate: int


class CourierLedgerObj(BaseModel):
    courier_id: int
    courier_name: str
    settlement_year: int
    settlement_month: int
    avg_rate: dec
    order_count: int
    total_sum: dec
    order_processing_fee: dec
    courier_tips_sum: dec
    courier_order_sum: dec
    courier_reward_sum: dec
