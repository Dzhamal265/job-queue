JOB QUEUE
=========

### Команды

* __Добавление задания__ `ADD <queue> <length> <data>`
    - Параметры
        - _queue_ - имя очереди: строка без пробелов
        - _length_ - длина содержимого задания: целое число не больше 10^6
        - _data_ - содержимое: массив байт длины _length_
    - Ответ
        - _id_ - уникальный идентификатор задания: строка без пробелов не длиннее 128 символов (не равная NONE)
* __Получение задания__ `GET <queue>`
    - Параметры
    - 
        - _queue_ - имя очереди: строка без пробелов
    - Ответ
        - _id_ - уникальный идентификатор задания: строка без пробелов не длиннее 128 символов
        - _length_ - длина содержимого задания: целое число не больше 10^6
        - _data_ - содержимое: массив байт длины _length_
* __Подтверждение выполнения__ `ACK <queue> <id>`
    - Параметры
        - _queue_ - имя очереди: строка без пробелов
        - _id_ - уникальный идентификатор задания: строка без пробелов не длиннее 128 символов
    - Ответ
        - `YES` - если такое задание присутствовало в очереди и было подтверждено его выполнение
        - `NO` - если такое задание отсутсвовало в очереди
* __Проверка__ `IN <queue> <id>`
    - Параметры
        - _queue_ - имя очереди: строка без пробелов
        - _id_ - уникальный идентификатор задания: строка без пробелов не длиннее 128 символов
    - Ответ
        - `YES` - если такое задание присутствует в очереди (не важно выполняется или нет)
        - `NO` - если такого задания в очереди нет
* __Сохранение__ `SAVE`
    - Ответ
        - `OK`
