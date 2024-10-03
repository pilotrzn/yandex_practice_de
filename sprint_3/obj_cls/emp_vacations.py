class Employee:
    vacation_days = 28

    def __init__(self, first_name, second_name, gender) -> None:
        self.first_name = first_name
        self.second_name = second_name
        self.gender = gender
        self.remaining_vacation_days = self.vacation_days

    def consume_vacation(self, rest_days):
        self.remaining_vacation_days -= rest_days

    def get_vacation_details(self):
        return (f'Остаток отпускных дней: {self.remaining_vacation_days}.')


employee = Employee(
    first_name='Роберт',
    second_name='Крузо',
    gender='m'
    )


employee.consume_vacation(7)
print(employee.get_vacation_details())
