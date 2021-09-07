# Merkle Tree
 
Реализация структуры данных Merkle Tree на Python 3

Данные хранится в массиве длины 2^h, где h ~ O(n), n - количество сообщений

### Теория

1.	Authenticated Data Structures Roberto Tamassia 2003 https://cs.brown.edu/research/pubs/pdfs/2003/Tamassia-2003-ADS.pdf
2.	Authenticated Data Structures, Generically Andrew Miller, Michael Hicks, Jonathan Katz, and Elaine Shi https://www.cs.umd.edu/~mwh/papers/gpads.pdf 
3.	MerkleTree | Brilliant Math & Science https://brilliant.org/wiki/merkle-tree/

### Методы

Основной функционал находиться в файле impl/MerkleTree.py. MerkleTreeInterface - абстрактный метод, от которого наследуется MerkleTree. Hashing.py - для доступа к функциям хэширования, встроенным в Python.

\_\_str__(self) - строковое представление

hash(self, item) - функция для хеширования

add_message(self, item) - добавить сообщение

update(self, position: int, item) - обновить значение

verify(self, position: int) - подтвердить соответствие корневого хэша из источника данному

get_auth_path(self, position: int) - получить путь для подтверждения по элементу

get_hash_of_leaf(self, position) - получить хэш элемента по позиции

get_digest(self) - получить корневой хэш дерева

### Тесты

Тесты находятся в test/MerkleTreeTest.py
Вместо функции хэширования используется \_\_str__ для легкой проверки результата. В тестах так же проверяется верификация по аутентификационному пути

## Задание
