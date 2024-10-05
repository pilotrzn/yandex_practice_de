class Employee:
    vacation_days = 28

    def __init__(self, first_name, second_name, gender) -> None:
        self.first_name = first_name
        self.second_name = second_name
        self.gender = gender
        self.remaining_vacation_days = Employee.vacation_days

    def consume_vacation(self, rest_days):
        self.remaining_vacation_days -= rest_days

    def get_vacation_details(self):
        return (f'Остаток отпускных дней: {self.remaining_vacation_days}.')


class FullTimeEmployee(Employee):

    def get_unpaid_vacation(self, start_date: str, vac_days: int):
        message = (f'Начало неоплачиваемого отпуска: {start_date}, '
                   f'продолжительность: {vac_days} дней.')
        return message


class PartTimeEmployee(Employee):
    vacation_days = 14

    def __init__(self, first_name, second_name, gender) -> None:
        super().__init__(first_name, second_name, gender)
        self.remaining_vacation_days = PartTimeEmployee.vacation_days


full_time_employee = FullTimeEmployee('Роберт', 'Крузо', 'м')
print(full_time_employee.get_unpaid_vacation('2023-07-01', 5))
part_time_employee = PartTimeEmployee('Алёна', 'Пятницкая', 'ж')
print(part_time_employee.get_vacation_details())
