class Employee:
    vacation_days = 28

    def __init__(self, first_name, second_name, gender) -> None:
        self.first_name = first_name
        self.second_name = second_name
        self.gender = gender


employee1 = Employee(
    first_name='Роберт',
    second_name='Крузо',
    gender='m'
    )

employee2 = Employee(
    first_name='Иван',
    second_name='Иванов',
    gender='m'
    )

print(f'Имя: {employee2.first_name}, Фамилия: {employee2.second_name}, '
      f'Пол: {employee2.gender}, '
      f'Отпускных дней в году: {employee2.vacation_days}.')

print(f'Имя: {employee1.first_name}, Фамилия: {employee1.second_name}, '
      f'Пол: {employee1.gender}, '
      f'Отпускных дней в году: {employee1.vacation_days}.')
