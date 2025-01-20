from datetime import datetime
from decimal import Decimal
from models import Model, Car, CarStatus, Sale


def model_data():
    return [
        Model(id=1, name="Optima", brand="Kia"),
        Model(id=2, name="Sorento", brand="Kia"),
        Model(id=3, name="3", brand="Mazda"),
        Model(id=4, name="Pathfinder", brand="Nissan"),
        Model(id=5, name="Logan", brand="Renault"),
    ]


def car_data():
    return [
        Car(
            vin="KNAGM4A77D5316538",
            model=1,
            price=Decimal("2000"),
            date_start=datetime(2024, 2, 8),
            status=CarStatus.available,
        ),
        Car(
            vin="5XYPH4A10GG021831",
            model=2,
            price=Decimal("2300"),
            date_start=datetime(2024, 2, 20),
            status=CarStatus.reserve,
        ),
        Car(
            vin="KNAGH4A48A5414970",
            model=1,
            price=Decimal("2100"),
            date_start=datetime(2024, 4, 4),
            status=CarStatus.available,
        ),
        Car(
            vin="JM1BL1TFXD1734246",
            model=3,
            price=Decimal("2276.65"),
            date_start=datetime(2024, 5, 17),
            status=CarStatus.available,
        ),
        Car(
            vin="JM1BL1M58C1614725",
            model=3,
            price=Decimal("2549.10"),
            date_start=datetime(2024, 5, 17),
            status=CarStatus.reserve,
        ),
        Car(
            vin="KNAGR4A63D5359556",
            model=1,
            price=Decimal("2376"),
            date_start=datetime(2024, 5, 17),
            status=CarStatus.available,
        ),
        Car(
            vin="5N1CR2MN9EC641864",
            model=4,
            price=Decimal("3100"),
            date_start=datetime(2024, 6, 1),
            status=CarStatus.available,
        ),
        Car(
            vin="JM1BL1L83C1660152",
            model=3,
            price=Decimal("2635.17"),
            date_start=datetime(2024, 6, 1),
            status=CarStatus.available,
        ),
        Car(
            vin="5N1CR2TS0HW037674",
            model=4,
            price=Decimal("3100"),
            date_start=datetime(2024, 6, 1),
            status=CarStatus.available,
        ),
        Car(
            vin="5N1AR2MM4DC605884",
            model=4,
            price=Decimal("3200"),
            date_start=datetime(2024, 7, 15),
            status=CarStatus.available,
        ),
        Car(
            vin="VF1LZL2T4BC242298",
            model=5,
            price=Decimal("2280.76"),
            date_start=datetime(2024, 8, 31),
            status=CarStatus.delivery,
        ),
    ]


def sales_data():
    return [
            Sale(
                sales_number="20240903#KNAGM4A77D5316538",
                car_vin="KNAGM4A77D5316538",
                sales_date=datetime(2024, 9, 3),
                cost=Decimal("1999.09"),
            ),
            Sale(
                sales_number="20240903#KNAGH4A48A5414970",
                car_vin="KNAGH4A48A5414970",
                sales_date=datetime(2024, 9, 4),
                cost=Decimal("2100"),
            ),
            Sale(
                sales_number="20240903#KNAGR4A63D5359556",
                car_vin="KNAGR4A63D5359556",
                sales_date=datetime(2024, 9, 5),
                cost=Decimal("7623"),
            ),
            Sale(
                sales_number="20240903#JM1BL1M58C1614725",
                car_vin="JM1BL1M58C1614725",
                sales_date=datetime(2024, 9, 6),
                cost=Decimal("2334"),
            ),
            Sale(
                sales_number="20240903#JM1BL1L83C1660152",
                car_vin="JM1BL1L83C1660152",
                sales_date=datetime(2024, 9, 7),
                cost=Decimal("451"),
            ),
            Sale(
                sales_number="20240903#5N1CR2TS0HW037674",
                car_vin="5N1CR2TS0HW037674",
                sales_date=datetime(2024, 9, 8),
                cost=Decimal("9876"),
            ),
            Sale(
                sales_number="20240903#5XYPH4A10GG021831",
                car_vin="5XYPH4A10GG021831",
                sales_date=datetime(2024, 9, 9),
                cost=Decimal("1234"),
            ),
        ]
