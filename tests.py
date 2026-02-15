import pytest

from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()

        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.books_genre) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()
        # 1. Тесты add_new_book
    @pytest.mark.parametrize(
            "book_name,expected_in_dict",
            [
                ("Война и мир", True),  # корректное имя
                ("", False),  # пустое имя
                ("a" * 41, False),  # >40 символов
                ("a" * 40, True),  # ровно 40 символов
                ("1984", True),  # короткое имя
            ]
        )
    def test_add_new_book_parametrized(self, book_name, expected_in_dict):
            collector = BooksCollector()
            collector.add_new_book(book_name)

            if expected_in_dict:
                assert book_name in collector.books_genre
                assert collector.books_genre[book_name] == ""
            else:
                assert book_name not in collector.books_genre

        # 2. Тесты set_book_genre
    @pytest.mark.parametrize(
            "book_name,genre,expected_genre",
            [
                ("Гарри Поттер", "Фантастика", "Фантастика"),  # валидный жанр
                ("Оно", "Ужасы", "Ужасы"),  # валидный жанр
                ("Шерлок Холмс", "Детективы", "Детективы"),  # валидный жанр
                ("Винни-Пух", "Мультфильмы", "Мультфильмы"),  # валидный жанр
                ("Алиса", "Романтика", ""),  # жанр не в списке genre
                ("Неизвестная книга", "Фантастика", None),  # книги нет в словаре
            ]
        )
    def test_set_book_genre_parametrized(self, book_name, genre, expected_genre):
            collector = BooksCollector()
            # Предварительно добавляем книгу (если она должна быть в словаре)
            if book_name != "Неизвестная книга":
                collector.add_new_book(book_name)

            collector.set_book_genre(book_name, genre)

            if expected_genre is None:
                assert book_name not in collector.books_genre  # книга не добавлена
            else:
                assert collector.get_book_genre(book_name) == expected_genre

        # 3. Тесты get_books_with_specific_genre
    @pytest.mark.parametrize(
            "genre,expected_books",
            [
                ("Фантастика", ["Гарри Поттер", "Дюна"]),
                ("Ужасы", ["Оно", "Сияние"]),
                ("Детективы", ["Шерлок Холмс"]),
                ("Мультфильмы", ["Винни-Пух"]),
                ("Романтика", []),  # жанр не в списке
                ("Комедии", []),  # нет книг в жанре
            ]
        )
    def test_get_books_with_specific_genre_parametrized(self, genre, expected_books):
            collector = BooksCollector()
            # Добавляем книги с разными жанрами
            books_data = [
                ("Гарри Поттер", "Фантастика"),
                ("Дюна", "Фантастика"),
                ("Оно", "Ужасы"),
                ("Сияние", "Ужасы"),
                ("Шерлок Холмс", "Детективы"),
                ("Винни-Пух", "Мультфильмы"),
            ]
            for name, genre_val in books_data:
                collector.add_new_book(name)
                collector.set_book_genre(name, genre_val)

            result = collector.get_books_with_specific_genre(genre)
            assert sorted(result) == sorted(expected_books)

        # 4. Тесты get_books_for_children
    @pytest.mark.parametrize(
            "books_data,expected_children_books",
            [
                (
                        [("Винни-Пух", "Мультфильмы"), ("Алиса", "Комедии")],
                        ["Винни-Пух", "Алиса"]
                ),
                (
                        [("Оно", "Ужасы"), ("Сияние", "Ужасы")],
                        []
                ),
                (
                        [("Дюна", "Фантастика"), ("Шерлок", "Детективы")],
                        ["Дюна"]  # Детективы — с возрастным рейтингом
                ),
                (
                        [("Без жанра", "")],
                        []  # книга без жанра не подходит
                ),
            ]
        )
    def test_get_books_for_children_parametrized(self, books_data, expected_children_books):
            collector = BooksCollector()
            for name, genre in books_data:
                collector.add_new_book(name)
                if genre:  # если жанр указан
                    collector.set_book_genre(name, genre)

            result = collector.get_books_for_children()
            assert sorted(result) == sorted(expected_children_books)

        # 5. Тесты add_book_in_favorites
    @pytest.mark.parametrize(
            "book_name,is_in_books_genre,expected_in_favorites",
            [
                ("Преступление и наказание", True, True),  # книга есть в словаре
                ("Мастер и Маргарита", True, True),  # книга есть в словаре
                ("Неизвестная книга", False, False),  # книги нет в словаре
                ("Преступление и наказание", True, False),  # дубликат (уже в избранном)
            ]
        )
    def test_add_book_in_favorites_parametrized(
                self, book_name, is_in_books_genre, expected_in_favorites
        ):
            collector = BooksCollector()
            # Предварительно добавляем книгу, если нужно
            if is_in_books_genre:
                collector.add_new_book(book_name)
                # Для случая дубликата — сразу добавляем в избранное
                if book_name == "Преступление и наказание":
                    collector.add_book_in_favorites(book_name)

            collector.add_book_in_favorites(book_name)

            if expected_in_favorites:
                assert book_name in collector.favorites
            else:
                assert book_name not in collector.favorites

        # 6. Тесты delete_book_from_favorites
    @pytest.mark.parametrize(
            "book_name,is_in_favorites,expected_removed",
            [
                ("Идиот", True, True),  # книга в избранном
                ("Герой нашего времени", False, False),  # книги нет в избранном
            ]
        )
    def test_delete_book_from_favorites_parametrized(
                self, book_name, is_in_favorites, expected_removed
        ):
            collector = BooksCollector()
            if is_in_favorites:
                collector.add_new_book(book_name)
                collector.add_book_in_favorites(book_name)

            collector.delete_book_from_favorites(book_name)

            if expected_removed:
                assert book_name not in collector.favorites
            else:
                assert book_name not in collector.favorites  # или в словаре, или нигде

        # 7. Тесты get_list_of_favorites_books
    @pytest.mark.parametrize(
            "favorites_data,expected_list",
            [
                ([], []),  # пустое избранное
                (["Преступление и наказание"], ["Преступление и наказание"]),  # одна книга
                (["Мастер и Маргарита", "Идиот"], ["Мастер и Маргарита", "Идиот"]),  # две книги
                (["Война и мир"], ["Война и мир"]),  # одна книга (проверка порядка)
            ]
        )
    def test_get_list_of_favorites_books_parametrized(self, favorites_data, expected_list):
            collector = BooksCollector()
            # Добавляем книги в словарь и в избранное
            for book in favorites_data:
                collector.add_new_book(book)
                collector.add_book_in_favorites(book)

            result = collector.get_list_of_favorites_books()
            assert sorted(result) == sorted(expected_list)

        # 8. Тесты get_books_genre

    @pytest.mark.parametrize(
        "books_data,expected_dict",
        [
            (
                    [],
                    {}  # пустой словарь
            ),
            (
                    [("Война и мир", "Классика"), ("1984", "Фантастика")],
                    {"Война и мир": "Классика", "1984": "Фантастика"}  # две книги с жанрами
            ),
            (
                    [("Без жанра", "")],
                    {"Без жанра": ""}  # книга без жанра
            ),
            (
                    [("Дубровский", "Приключения"), ("Мёртвые души", "Сатира")],
                    {"Дубровский": "Приключения", "Мёртвые души": "Сатира"}  # разные жанры
            ),
        ]
    )
    def test_get_books_genre_parametrized(self, books_data, expected_dict):
        collector = BooksCollector()
        # Добавляем книги и задаём жанры
        for name, genre in books_data:
            collector.add_new_book(name)
            if genre:  # если жанр указан
                collector.set_book_genre(name, genre)

        result = collector.get_books_genre()
        assert result == expected_dict

    # 9. Тесты get_book_genre
    @pytest.mark.parametrize(
        "book_name,books_data,expected_genre",
        [
            ("Война и мир", [("Война и мир", "Классика")], "Классика"),  # книга есть, жанр задан
            ("1984", [("1984", "Фантастика")], "Фантастика"),  # книга есть, жанр задан
            ("Неизвестная книга", [], None),  # книги нет в словаре
            ("Без жанра", [("Без жанра", "")], ""),  # книга есть, но жанр не задан
            ("Дубровский", [("Дубровский", "Приключения")], "Приключения"),  # другой жанр
        ]
    )
    def test_get_book_genre_parametrized(self, book_name, books_data, expected_genre):
        collector = BooksCollector()
        # Предварительно добавляем книги из books_data
        for name, genre in books_data:
            collector.add_new_book(name)
            if genre:
                collector.set_book_genre(name, genre)

        result = collector.get_book_genre(book_name)
        assert result == expected_genre
