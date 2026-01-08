# Облачные технологии Yandex Cloud

## Описание

Задача данного учебного проекта заключается в построении сервиса, который заполняет данными детальный слой DWH в Postgres. Сбор данных осуществляется из разных источников. Характер данных - транзакционная активность пользователей банковского приложения. При реализации сервиса необходимо использовать технологии Kafka и Kubernetes.

## Цель работы

Реализовать два сервиса, которые заполняют слои DDS и CDM в PostgresSQL. При реализации использовать облачные технологии Yandex Cloud.

## Этапы работы

- Создание сервиса заполнения слоя DDS.
  - Написание кода сервиса.
  - Реализация сервиса в Kubernetes.

- Создание сервиса заполнения слоя CDM.
  - Написание кода сервиса.
  - Реализация сервиса в Kubernetes.

## Описание рабочих файлов

Папка solution/service_dds/src.

- app_config.py - параметры подключения к Kafka.
- app.py - основной файл вызова приложения.

Папка solution/service_dds/src/dds_loader.

- dds_message_processor_job.py - загрузчик dds слоя.

Папка solution/service_dds/src/dds_loader/models:

- models.py - описание классов

Папка solution/service_dds/src/dds_loader/repository:

- dds_loader.py - класс для создания объектов классов
- dds_db_insert.py - класс для выполнения sql-запросов(вставка)

---

Папка solution/service_cdm/src.

- app_config.py - параметры подключения к Kafka.
- app.py - основной файл вызова приложения.

Папка solution/service_cdm/src/cdm_loader.

- cdm_message_processor_job.py - загрузчик dds слоя.

Папка solution/service_cdm/src/cdm_loader/models:

- models.py - описание классов

Папка solution/service_cdm/src/cdm_loader/repository:

- cdm_loader.py - класс для создания объектов классов
- cdm_db_insert.py - класс для выполнения sql-запросов(вставка)