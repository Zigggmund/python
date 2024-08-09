"""
Модуль содержит классы LinkedList и LinkedListItem
LinkedList реализует операции над связным списком
LinkedListItem является элементом LinkedList
"""


class LinkedListItem:
    """
    Класс содержит в себе
    prev - ссылка на предыдущий элемент
    next - ссылка на следующий элемент
    data - элемент списка
    track - данные элемента в виде экземпляра Composition
    """

    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    @property
    def next_item(self):
        """
        Геттер next
        :return: next
        """
        return self.next

    @next_item.setter
    def next_item(self, item):
        self.next = item
        if item is not None:
            item.prev = self

    @property
    def previous_item(self):
        """
        Геттер prev
        :return: prev
        """
        return self.prev

    @previous_item.setter
    def previous_item(self, item):
        self.prev = item
        if item is not None:
            item.next = self


class LinkedList:
    """
    Класс содержит в себе все операции для
    работы с кольцевыми двусвязными списками
    """

    def __init__(self, first_item=None):
        self.first_item = first_item

    def append_left(self, item):
        """
        Метод добавляет элемент item в начало списка
        :param item: элемент, который необходимо добавить в начало списка
        :return: None
        """
        if not isinstance(item, LinkedListItem):
            item = LinkedListItem(item)

        item.next_item = self.first_item
        item.previous_item = self.last
        if self.first_item is None:
            item.next_item = item
        self.first_item = item

    def append_right(self, item):
        """
        Метод добавляет элемент item в конец списка
        :param item: элемент, который необходимо добавить в конец списка
        :return: None
        """
        if not isinstance(item, LinkedListItem):
            item = LinkedListItem(item)

        if self.first_item is None:
            self.first_item = item
            item.next_item = item
        else:
            elem = self.first_item
            while elem.next_item is not self.first_item:
                elem = elem.next_item
            item.previous_item = elem
            item.next_item = self.first_item

    def append(self, item):
        """
        Метод работает как метод append_right
        :param item: элемент, который необходимо добавить в конец списка
        :return: None
        """
        self.append_right(item)

    def remove(self, item):
        """
        Метод удаляет первый элемент item в списке
        :param item: элемент, который необходимо удалить
        :return: None
        """
        if self.first_item is None:
            raise ValueError("Список пуст")

        elem = self.first_item
        for _ in range(len(self)):
            if elem.data == item:
                if len(self) == 1:
                    self.first_item = None
                else:
                    elem.next_item.previous_item = elem.previous_item
                    if elem == self.first_item:
                        self.first_item = elem.next_item
                return
            elem = elem.next_item

        raise ValueError("Такого элемента нет")

    def insert(self, previous, item):
        """
        Метод добавляет item в LinkedList после элемента previous(data)
        :param previous: значение элемента,
        после  которого необходимо добавить наш
        :param item: элемент, который необходимо добавить после previous
        :return: None
        """
        if not isinstance(item, LinkedListItem):
            item = LinkedListItem(item)

        if previous not in self:
            raise ValueError("Такого элемента нет")
        if self.first_item is None:
            raise ValueError("Список пуст")

        elem = self.first_item
        while elem.data != previous and elem != self.last:
            elem = elem.next_item
        elem.next_item.previous_item = item
        elem.next_item = item

    @property
    def last(self):
        """
        Метод возвращает последний элемент двусвязного
        кольцевого списка в виде экземпляра класса
        :return: LinkedListItem
        """
        elem = self.first_item
        last_elem = None
        for _ in range(len(self)):
            last_elem = elem
            elem = elem.next_item
            if elem == self.first_item:
                break
        return last_elem

    def __iter__(self):
        """
        Метод возвращает итератор
        :return: Iterator
        """
        cur_el = self.first_item
        for _ in range(len(self)):
            yield cur_el
            cur_el = cur_el.next

    def __reversed__(self):
        """
        Метод возвращает итератор в обратном порядке
        :return: Iterator
        """
        elem = self.first_item
        if elem:
            elem = elem.previous_item
            for _ in range(len(self)):
                yield elem.data
                elem = elem.previous_item

    def __next__(self):
        """
        Метод возвращает следующий элемент в итерации
        :return: LinkedListItem
        """
        elem = self.first_item
        if elem:
            return elem.next
        raise StopIteration

    def __getitem__(self, index: int):
        if index >= len(self) or index <= -len(self) - 1:
            raise IndexError("Выходит за диапозон")

        index = index + len(self) if index < 0 else index
        elem = self.first_item
        for _ in range(index):
            elem = elem.next_item
        return elem.data

    def __contains__(self, item):
        """
        Метод, проверяющий содержание item в списке
        :param item: элемент,
        который необходимо проверить на содержание в списке
        :return: boolean
        """
        elem = self.first_item
        for _ in range(len(self)):
            if elem.data == item:
                return True
            elem = elem.next_item
        return False

    def __len__(self):
        """
        Метод возвращает длину списка
        :return: int
        """
        leng = 0
        elem = self.first_item
        while elem:
            leng += 1
            elem = elem.next
            if elem == self.first_item:
                break
        return leng

    def __str__(self):
        """
        Метод возвращает все элементы списка в виде строки
        :return: str
        """
        return f"[{', '.join([str(item) for item in self])}]"
