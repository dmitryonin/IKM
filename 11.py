class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise ValueError("Попытка извлечь бочку из пустого отсека")
        return self._items.pop()

    def is_empty(self):
        return len(self._items) == 0

    def peek(self):
        if self.is_empty():
            return None
        return self._items[-1]


class Barge:
    def __init__(self, compartments_count, max_barrels):
        if not (1 <= compartments_count <= 100000):
            raise ValueError("Количество отсеков должно быть от 1 до 100,000")
        if not (1 <= max_barrels <= 100000):
            raise ValueError("Максимальное количество бочек должно быть от 1 до 100,000")
        self._compartments = [Stack() for _ in range(compartments_count)]
        self._max_barrels = max_barrels
        self._current_barrels = 0
        self._max_seen_barrels = 0
        self._error = False

    def load_barrel(self, compartment, fuel_type):
        if not (1 <= compartment <= len(self._compartments)):
            self._error = True
            return
        self._compartments[compartment - 1].push(fuel_type)
        self._current_barrels += 1
        if self._current_barrels > self._max_barrels:
            self._error = True
        self._max_seen_barrels = max(self._max_seen_barrels, self._current_barrels)

    def unload_barrel(self, compartment, expected_fuel):
        if not (1 <= compartment <= len(self._compartments)):
            self._error = True
            return
        stack = self._compartments[compartment - 1]
        if stack.is_empty():
            self._error = True
            return
        fuel = stack.pop()
        if fuel != expected_fuel:
            self._error = True
        self._current_barrels -= 1

    def has_error(self):
        return self._error

    def is_empty(self):
        return all(stack.is_empty() for stack in self._compartments)

    def get_max_barrels(self):
        return self._max_seen_barrels


class BargeSimulator:
    def __init__(self):
        self._barge = None

    def run(self):
        print("Введите параметры и операции согласно формату:\n"
              "Первая строка: N K P (кол-во операций, отсеков, макс. бочек)\n"
              "Далее N строк: '+ A B' для погрузки или '- A B' для разгрузки\n"
              "Пример:\n6 1 2\n+ 1 1\n+ 1 2\n- 1 2\n- 1 1\n+ 1 3\n- 1 3")
        # Запрос параметров N, K, P
        while True:
            try:
                input_str = input("Введите N K P(Три целых числа от 1 до 100,000 через пробел): ").strip()
                n, k, p = map(int, input_str.split())
                if not (1 <= n <= 100000 and 1 <= k <= 100000 and 1 <= p <= 100000):
                    raise ValueError("N, K, P должны быть от 1 до 100,000")
                self._barge = Barge(k, p)
                break
            except ValueError:
                print("Ошибка: некорректный ввод. Введите три целых числа от 1 до 100,000 через пробел.")

        # Запрос операций
        operations = []
        for i in range(n):
            while True:
                try:
                    op = input(f"Операция {i + 1}: ").strip().split()
                    if len(op) != 3 or op[0] not in ['+', '-']:
                        raise ValueError("Неверный формат. Используйте '+ A B' или '- A B'")
                    action, a, b = op[0], int(op[1]), int(op[2])
                    operations.append((action, a, b))
                    break
                except ValueError:
                    print("Ошибка: некорректная операция. Введите '+ A B' или '- A B', где A и B — целые числа.")

        # Выполнение операций
        for action, a, b in operations:
            if action == '+':
                self._barge.load_barrel(a, b)
            elif action == '-':
                self._barge.unload_barrel(a, b)

        # Вывод результата
        if self._barge.has_error() or not self._barge.is_empty():
            print("Error")
        else:
            print(f"Максимальное количество бочек на барже: {self._barge.get_max_barrels()}")


if __name__ == "__main__":
    simulator = BargeSimulator()
    simulator.run()