1. сырые данные

Создайте схему raw_data и таблицу sales в этой схеме. 

Заполните таблицу sales данными, используя команду COPY в менеджере БД (например, DBeaver) или \copy в psql. Если возникнет ошибка о лишних данных в исходном файле, укажите явно параметр DELIMITER.

Проанализируйте сырые данные. Подумайте:
 - какие данные повторяются и их стоит вынести в отдельные таблицы;
 - какие типы данных должны быть у каждого поля;
 - на какие поля стоит добавить ограничения (CONSTRAINTS);
 - какие поля могут содержать NULL, а где нужно добавить ограничение NOT NULL.

Обратите внимание на атрибут color. Подумайте, как лучше его хранить. У вас будет связь многие-ко-многим, ведь у одного цвета может быть несколько машин, а машина может быть разных цветов.

2. ннормализация
Создайте схему car_shop, а в ней cоздайте нормализованные таблицы (до третьей нормальной формы). Подумайте, какие поля будут выступать первичными ключами, а какие внешними. У всех первичных ключей должен быть автоинкремент. В отдельном файле опишите, почему вы выбрали такую модель данных.

Выберите наиболее подходящий формат данных для каждой колонки
Используя комментарий (/*comment*/) для каждого поля, напишите, почему вы выбрали тот или иной тип данных. Например:
brand_name varchar — в названии бренда могут быть и цифры, и буквы, поэтому выбираем varchar.
price numeric(9, 2) — цена может содержать только сотые и не может быть больше семизначной суммы. У numeric повышенная точность при работе с дробными числами, поэтому при операциях c этим типом данных, дробные числа не потеряются.

Заполните все таблицы данными, c помощью команд INSERT INTO …  SELECT …. Чтобы разбить столбец с маркой, моделью машины и её цветом, можно использовать разные способы — выбирайте любой, удобный для себя.
