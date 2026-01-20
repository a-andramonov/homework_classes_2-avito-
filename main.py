import json
import keyword


class ColorizeMixin:
    """
    Миксин для окрашивания текста.
    Он меняет цвет вывода в консоли.
    """
    def __repr__(self):
        # 1. Спрашиваем у "следующего в очереди" класса текст
        # (в нашем случае это будет BaseAdvert)
        text = super().__repr__()
        # 2. Берем код цвета из атрибута класса
        # self.repr_color_code мы укажем в классе Advert
        color_code = self.repr_color_code
        return f"\033[{color_code}m{text}\033[0m"


class JsonParser:
    def __init__(self, mapping):
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key = key + "_"
            if isinstance(value, dict):
                value = JsonParser(value)
            setattr(self, key, value)


class BaseAdvert(JsonParser):
    def __init__(self, mapping):
        super().__init__(mapping)

        # Проверка заголовка
        if 'title' not in mapping:
            raise ValueError("title is required")
        # Установка цены по умолчанию
        if not hasattr(self, '_price'):
            self._price = 0

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("must be >= 0")
        self._price = value

    # Вот тут мы формируем сам текст.
    def __repr__(self):
        return f"{self.title} | {self.price} ₽"


class Advert(ColorizeMixin, BaseAdvert):
    """
    Финальный класс.
    1. ColorizeMixin — добавляет цвет.
    2. BaseAdvert — дает данные (title, price) и текст.
    """
    repr_color_code = 33  # 33 — это код желтого цвета


# ==========================
# ФИНАЛЬНАЯ ПРОВЕРКА
# ==========================
if __name__ == '__main__':
    print("--- Проверка цвета ---")

    # Создаем корги
    corgi_str = """{
        "title": "Вельш-корги",
        "price": 1000,
        "class": "dogs"
    }"""
    corgi = json.loads(corgi_str)
    corgi_ad = Advert(corgi)

    # Печатаем объект
    # Должно быть: Вельш-корги | 1000 ₽ (ЖЕЛТЫМ ЦВЕТОМ)
    print(corgi_ad)

    print("\n--- Проверка старых функций ---")
    # Проверяем, что точка и address все еще работают
    print("Категория:", corgi_ad.class_)
    print("Цена:", corgi_ad.price)
