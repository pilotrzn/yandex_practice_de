class BacteriaProducer:
    def __init__(self, max_bacteria):
        self.max_bacteria = max_bacteria
        self.bacteria_count = 0

    # Допишите метод
    def create_new(self):
        if self.bacteria_count < self.max_bacteria:
            self.bacteria_count += 1
            print(f'Добавлена одна бактерия. '
                  f'Количество бактерий в популяции: {self.bacteria_count}')
        else:
            print('Нет места под новую бактерию')

    # Допишите методl
    def remove_one(self):
        if self.bacteria_count > 0:
            self.bacteria_count -= 1
            print(f'Одна бактерия удалена. '
                  f'Количество бактерий в популяции: {self.bacteria_count}')
        else:
            print('В популяции нет бактерий, удалять нечего')


bacteria_producer = BacteriaProducer(max_bacteria=3)
bacteria_producer.remove_one()
bacteria_producer.create_new()
bacteria_producer.create_new()
bacteria_producer.create_new()
bacteria_producer.create_new()
bacteria_producer.remove_one()
