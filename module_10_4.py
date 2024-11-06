import threading
import time
import random
from queue import Queue


# Класс для представления стола в кафе
class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None  # Изначально стол свободен


# Класс для представления гостя, который является потоком
class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        # Гость ожидает от 3 до 10 секунд
        wait_time = random.randint(3, 10)
        time.sleep(wait_time)


# Класс для представления кафе
class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()  # Очередь для гостей
        self.tables = tables  # Список столов

    def guest_arrival(self, *guests):
        for guest in guests:
            assigned_table = None
            # Находит свободный стол
            for table in self.tables:
                if table.guest is None:
                    table.guest = guest
                    assigned_table = table
                    break

            if assigned_table is not None:
                print(f"{guest.name} сел(-а) за стол номер {assigned_table.number}")
                guest.start()
            else:
                # Если свободных столов нет, помещаем в очередь
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        # Обслуживание гостей, пока очередь не пустая или есть занятые столы
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest is not None:
                    if not table.guest.is_alive():
                        print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                        print(f"Стол номер {table.number} свободен")
                        table.guest = None  # Освобождаем стол

                        # Проверяем очередь на наличие ожидающих гостей
                        if not self.queue.empty():
                            next_guest = self.queue.get()
                            table.guest = next_guest
                            print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
                            next_guest.start()


# Пример использования классов
if __name__ == "__main__":
    # Создаем столы
    table1 = Table(1)
    table2 = Table(2)
    table3 = Table(3)

    # Создаем кафе с тремя столами
    cafe = Cafe(table1, table2, table3)

    # Гости прибывают
    cafe.guest_arrival(Guest('Vasya'), Guest('Petya'), Guest('Masha'),
                       Guest('Sasha'), Guest('Katya'), Guest('Oleg'))

    # Обслуживаем гостей
    # Запускаем в отдельном потоке, чтобы не блокировать основной поток
    while any(table.guest is not None for table in cafe.tables) or not cafe.queue.empty():
        cafe.discuss_guests()
        time.sleep(1)  # Интервал между проверками