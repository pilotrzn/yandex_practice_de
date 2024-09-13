def find_pool_capacity(length, num_of_people, width = None):
    
    # Опишите условие, когда передано отрицательное значение длины.
    if length < 0:
        length = -length
    
    # Опишите условие, когда передано отрицательное значение 
    # количества людей.
    if num_of_people < 0:
        num_of_people = -num_of_people

    # Опишите условие, когда ширина бассейна не указана, когда указано
    # отрицательное значение, и когда положительное.
    if width is None:
        width = length
    elif width < 0:
        width = -width
 
    square = width * length
    
    # Опишите условие вывода сообщений и распечатайте эти сообщения.
    if num_of_people / square <= 2 :
        print('Бассейн площадью',str(square),'кв. м.','вмещает',str(num_of_people), 'чел.')
    else:
        print('Бассейн площадью',str(square),'кв. м.','не вмещает',str(num_of_people), 'чел.')

# Проверьте работу функции, можете подставить свои значения.
find_pool_capacity(2, 2)
find_pool_capacity(4, 5, 10)
find_pool_capacity(-10, -5, -2)