# Content Service

### Развертывание и запуск проекта

- Прежде всего надо:

1. Удостовериться, что установлена утилита `make`.
2. Удостовериться, что установлен `docker`.
3. Запустить `make bin-deps`.

- Запуск приложения, для продакшена:
#### <command>
    make compose-up-prod
#### </command>

- Остановка контейнеров:

#### <command>
    make compose-down
#### </command>

### Workflow

- Получить информацию по командам:
#### <command>
    make help
#### </command>


- Посмотреть ошибки по PEP8:
#### <command>
    make linter-check
#### </command>
линтер укажет на все ошибки стандарта PEP8

- Просмотр содержимого БД:

1. Находим Container ID у образа image:
#### <command>
    docker ps
#### </command>

2. Вставляем нужный Container ID.
#### <command>
    docker exec -it <container_id> bash
#### </command>

3. Открывает консоль Postgres.
#### <command>
    psql -p 5432 user -d postgres
#### </command>

4. Чтобы выйти из контейнера.
#### <command>
    exit
#### </command>

- Работа с миграция:

- Удалить содержимое БД:
#### <command>
    make docker-rm-volume
#### </command>

- Unit тесты
