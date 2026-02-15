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
        assert len(collector.get_books_rating()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()
        # 1. Тесты метода add_new_book

        def test_add_new_book_success(self):
            """Добавляем книгу с корректным названием (≤40 символов)."""
            collector = BooksCollector()
            collector.add_new_book("Война и мир")
            assert "Война и мир" in collector.books_genre
            assert collector.books_genre["Война и мир"] == ""

        def test_add_new_book_duplicate(self):
            """Повторное добавление той же книги — не должно добавиться."""
            collector = BooksCollector()
            collector.add_new_book("1984")
            collector.add_new_book("1984")
            assert len(collector.books_genre) == 1
            assert collector.books_genre["1984"] == ""

        def test_add_new_book_empty_name(self):
            """Попытка добавить книгу с пустым названием — не должно добавиться."""
            collector = BooksCollector()
            collector.add_new_book("")
            assert "" not in collector.books_genre

        def test_add_new_book_long_name(self):
            """Название длиннее 40 символов — не должно добавиться."""
            collector = BooksCollector()
            long_name = "a" * 41
            collector.add_new_book(long_name)
            assert long_name not in collector.books_genre

        def test_add_new_book_max_length(self):
            """Название ровно 40 символов — должно добавиться."""
            collector = BooksCollector()
            max_name = "a" * 40
            collector.add_new_book(max_name)
            assert max_name in collector.books_genre

        # 2. Тесты метода set_book_genre

        def test_set_book_genre_success(self):
            """Устанавливаем жанр для существующей книги из списка genre."""
            collector = BooksCollector()
            collector.add_new_book("Гарри Поттер")
            collector.set_book_genre("Гарри Поттер", "Фантастика")
            assert collector.books_genre["Гарри Поттер"] == "Фантастика"

        def test_set_book_genre_book_not_exists(self):
            """Пытаемся установить жанр для книги, которой нет в словаре."""
            collector = BooksCollector()
            collector.set_book_genre("Неизвестная книга", "Детективы")
            assert "Неизвестная книга" not in collector.books_genre

        def test_set_book_genre_invalid_genre(self):
            """Жанр не входит в список genre — не должен установиться."""
            collector = BooksCollector()
            collector.add_new_book("Дюна")
            collector.set_book_genre("Дюна", "Романтика")  # Романтика не в self.genre
            assert collector.books_genre["Дюна"] == ""

        # 3. Тесты метода get_book_genre

        def test_get_book_genre_existing(self):
            """Получаем жанр существующей книги."""
            collector = BooksCollector()
            collector.add_new_book("Властелин колец")
            collector.set_book_genre("Властелин колец", "Фантастика")
            assert collector.get_book_genre("Властелин колец") == "Фантастика"

        def test_get_book_genre_not_exists(self):
            """Книга не существует — должен вернуться None."""
            collector = BooksCollector()
            assert collector.get_book_genre("Нет такой книги") is None

        # 4. Тесты метода get_books_with_specific_genre

        def test_get_books_with_specific_genre_found(self):
            """Находим книги заданного жанра."""
            collector = BooksCollector()
            collector.add_new_book("Оно")
            collector.add_new_book("Сияние")
            collector.set_book_genre("Оно", "Ужасы")
            collector.set_book_genre("Сияние", "Ужасы")
            result = collector.get_books_with_specific_genre("Ужасы")
            assert "Оно" in result
            assert "Сияние" in result
            assert len(result) == 2

        def test_get_books_with_specific_genre_no_books(self):
            """Жанр существует, но книг с ним нет."""
            collector = BooksCollector()
            result = collector.get_books_with_specific_genre("Комедии")
            assert result == []

        def test_get_books_with_specific_genre_invalid_genre(self):
            """Жанр не входит в self.genre — должен вернуть пустой список."""
            collector = BooksCollector()
            result = collector.get_books_with_specific_genre("Романтика")
            assert result == []

        # 5. Тесты метода get_books_genre

        def test_get_books_genre(self):
            """Проверяем возврат полного словаря books_genre."""
            collector = BooksCollector()
            collector.add_new_book("Шерлок Холмс")
            collector.set_book_genre("Шерлок Холмс", "Детективы")
            expected = {"Шерлок Холмс": "Детективы"}
            assert collector.get_books_genre() == expected

        # 6. Тесты метода get_books_for_children

        def test_get_books_for_children_valid(self):
            """Книги без возрастного рейтинга (не в genre_age_rating)."""
            collector = BooksCollector()
            collector.add_new_book("Винни-Пух")
            collector.set_book_genre("Винни-Пух", "Мультфильмы")
            collector.add_new_book("Алиса в Стране чудес")
            collector.set_book_genre("Алиса в Стране чудес", "Комедии")
            result = collector.get_books_for_children()
            assert "Винни-Пух" in result
            assert "Алиса в Стране чудес" in result

        def test_get_books_for_children_age_rated(self):
            """Книги с возрастным рейтингом (в genre_age_rating) — не должны попасть."""
            collector = BooksCollector()
            collector.add_new_book("Кладбище домашних животных")
            collector.set_book_genre("Кладбище домашних животных", "Ужасы")
            result = collector.get_books_for_children()
            assert "Кладбище домашних животных" not in result

        def test_get_books_for_children_no_genre(self):
            """Книга без жанра — не должна попасть в список для детей."""
            collector = BooksCollector()
            collector.add_new_book("Без жанра")
            result = collector.get_books_for_children()
            assert "Без жанра" not in result

        # 7. Тесты метода add_book_in_favorites

        def test_add_book_in_favorites_success(self):
            """Добавляем книгу в избранное (книга есть в books_genre)."""
            collector = BooksCollector()
            collector.add_new_book("Преступление и наказание")
            collector.add_book_in_favorites("Преступление и наказание")
            assert "Преступление и наказание" in collector.favorites

        def test_add_book_in_favorites_not_in_books_genre(self):
            """Книга отсутствует в books_genre — не должна добавиться в избранное."""
            collector = BooksCollector()
            collector.add_book_in_favorites("Неизвестная книга")
            assert "Неизвестная книга" not in collector.favorites

        def test_add_book_in_favorites_duplicate(self):
            """Повторное добавление в избранное — не должно дублироваться."""
            collector = BooksCollector()
            collector.add_new_book("Мастер и Маргарита")
            collector.add_book_in_favorites("Мастер и Маргарита")
            collector.add_book_in_favorites("Мастер и Маргарита")
            assert collector.favorites.count("Мастер и Маргарита") == 1

        # 8. Тесты метода delete_book_from_favorites

        def test_delete_book_from_favorites_success(self):
            """Удаляем книгу из избранного."""
            collector = BooksCollector()
            collector.add_new_book("Идиот")
            collector.add_book_in_favorites("Идиот")
            collector.delete_book_from_favorites("Идиот")
            assert "Идиот" not in collector.favorites

    # 9. Тесты метода get_list_of_favorites_books

    def test_get_list_of_favorites_books_empty(self):
        """Проверяем, что метод возвращает пустой список, если избранное пусто."""
        collector = BooksCollector()
        result = collector.get_list_of_favorites_books()
        assert result == []
        assert isinstance(result, list)

    def test_get_list_of_favorites_books_one_book(self):
        """Проверяем возврат списка с одной книгой в избранном."""
        collector = BooksCollector()
        collector.add_new_book("Преступление и наказание")
        collector.add_book_in_favorites("Преступление и наказание")

        result = collector.get_list_of_favorites_books()

        assert result == ["Преступление и наказание"]
        assert len(result) == 1

    def test_get_list_of_favorites_books_multiple_books(self):
        """Проверяем возврат списка с несколькими книгами в избранном."""
        collector = BooksCollector()
        # Добавляем книги в словарь
        collector.add_new_book("Мастер и Маргарита")
        collector.add_new_book("Идиот")
        collector.add_new_book("Война и мир")

        # Добавляем в избранное
        collector.add_book_in_favorites("Мастер и Маргарита")
        collector.add_book_in_favorites("Идиот")
        collector.add_book_in_favorites("Война и мир")

        result = collector.get_list_of_favorites_books()

        expected = ["Мастер и Маргарита", "Идиот", "Война и мир"]
        assert result == expected
        assert len(result) == 3

    def test_get_list_of_favorites_books_after_deletion(self):
        """Проверяем список избранного после удаления одной книги."""
        collector = BooksCollector()
        collector.add_new_book("Гарри Поттер")
        collector.add_new_book("Хоббит")

        collector.add_book_in_favorites("Гарри Поттер")
        collector.add_book_in_favorites("Хоббит")

        # Удаляем одну книгу из избранного
        collector.delete_book_from_favorites("Хоббит")

        result = collector.get_list_of_favorites_books()

        assert "Хоббит" not in result
        assert "Гарри Поттер" in result
        assert len(result) == 1

    def test_get_list_of_favorites_books_unchanged_after_adding_non_favorite(self):
        """Проверяем, что список избранного не меняется при добавлении книги, не помеченной как избранное."""
        collector = BooksCollector()
        collector.add_new_book("Анна Каренина")
        collector.add_book_in_favorites("Анна Каренина")

        # Добавляем ещё одну книгу, но не в избранное
        collector.add_new_book("Братья Карамазовы")

        result = collector.get_list_of_favorites_books()

        assert result == ["Анна Каренина"]
        assert "Братья Карамазовы" not in result
