from typing import TypeVar, Generic, List, Type
from psycopg.rows import class_row
from lib import PgConnect


T = TypeVar('T')  # Обобщенный тип


class OriginRepository(Generic[T]):
    def __init__(self, pg: PgConnect, result_class: Type[T]) -> None:
        self._db = pg
        self.return_class = result_class

    def list(self, threshold: int,
             limit: int, query: str, all: bool = False) -> List[T]:
        """
            Функция, возвращающая список указанных классов
            из запроса query при заданных ограничениях threshold и limit
            Отрабатывает если переданном запросе есть конструкция %{value}s
        """
        # возвращаемый кортеж будет преобразован в указанный класс(объект класса)
        with self._db.client().cursor(row_factory=class_row(self.return_class)) as cur:
            if all:
                cur.execute(query)
                objs = cur.fetchall()
            else:
                cur.execute(
                    query,
                    {
                        "threshold": threshold,
                        "limit": limit
                    }
                )
            objs = cur.fetchall()
        return objs

    def get_value(self, query: str) -> int:
        """
            Функция возвращает значение int, например при запросах SELECT MAX
        """
        with self._db.client().cursor() as cur:
            cur.execute(query)
            result = cur.fetchone()
        return result[0] if result and result[0] is not None else 0

    def list_by_str(self, value: str, query: str) -> List[T]:
        with self._db.client().cursor(row_factory=class_row(self.return_class)) as cur:
            cur.execute(
                query,
                {
                    "value": value
                }
            )
            objs = cur.fetchall()
        return objs

    def list_all(self, query: str) -> List[T]:
        with self._db.client().cursor(row_factory=class_row(self.return_class)) as cur:
            cur.execute(query)
            objs = cur.fetchall()
        return objs
