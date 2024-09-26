# imports
import functions as func
import json
from pprint import pprint

# constants
DATE_FORMAT = '%Y-%m-%d'
# vars
goods = {}

func.add(goods, 'Пельмени универсальные', 2, '2024-10-10')
func.add(goods, 'Вода', 0.5)
func.add(goods, 'Вода', 1.6)
func.add(goods, 'Яйца куриные', 20, '2024-09-16')
func.add(goods, 'Яйца куриные', 10, '2024-09-16')
func.add(goods, 'Яйца куриные', 4, '2024-09-17')
func.add(goods, 'Пельмени универсальные', 0.5, '2025-01-10')
func.add(goods, 'Яйца перепелиные', 10, '2024-09-20')
func.add(goods, 'Колбаса', 0.6, '2024-09-24')
func.add(goods, 'Продукт_1', 12, '2024-09-17' )
func.add(goods, 'Продукт_2', 10, '2024-09-19' )
func.add(goods, 'Продукт_3', 3, '2024-09-18' )
func.add(goods, 'Продукт_4', 5, '2024-11-10' )

# print(goods)

# print(func.find(goods,'колб'))
# print(func.amount2(goods,'яйц'))
# print(func.amount(goods,'колб'))
print(func.expire(goods))
print(func.expire(goods,-5  ))
# func.add_by_note({},'Яйца гусиные №1 4 2024-11-10')
# func.add_by_note(goods,'Яйца гусиные №1 1.5')
# print(goods)
# jsondata = json.dumps(goods,ensure_ascii=False, default=str)
# print(jsondata)
# pprint(json.dumps(jsondata, ensure_ascii=False, default=str))
