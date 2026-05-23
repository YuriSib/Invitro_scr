import time
from random import randint

from app.utils.logger import logger
from app.utils.xl_worker import ExcelTable
from app.parse.scrapper import InvitroScrapper
from config import TABLE_PATH


def add_to_table(services: list[dict], table: ExcelTable):
    logger.debug(f'Вставляю полученные данные в таблицу.')
    result = table.add_services(services)
    if result != "OK":
        logger.error(f"Возникла ошибка при попытке вставить данные в таблицу. {result}")
        return None
    logger.debug('Данные вставлены успешно.')
    table.save()


def worker(categories: dict, table: ExcelTable, scrapper: InvitroScrapper, category_type="tests") -> int:
    # В этом цикле будут использоваться рандомные ожидания для того,
    # чтобы сервис Invitro не заблочил наш парсер по IP-адресу.
    crv_cnt = 0
    for category_title, category_id in categories.items():
        time_sleep = randint(1, 3)
        logger.debug(f"Жду {time_sleep} секунды")
        time.sleep(time_sleep)
        logger.info(f"Начинаю обрабатывать категорию {category_title}")

        table.add_category_row(category_title)

        logger.debug(f"Получаю данные по анализам для категории {category_title}")
        services = scrapper.get_services(category_id, category_type)

        if type(services) is str:
            logger.error(f"Не удалось получить данные по категории. причина - {services}")

            logger.info(f'Жду {time_sleep} секунд и пробую еще раз.')
            services = scrapper.get_services(category_id, category_type)
            if type(services) is str:
                logger.critical(f"Опять не удалось получить данные по категории. Причина - {services}")
                continue

        crv_cnt += len(services)

        add_to_table(services, table)
        logger.info(f"Найдено {crv_cnt} услуг")
    return crv_cnt


def main():
    table = ExcelTable(TABLE_PATH)
    scrapper = InvitroScrapper()

    logger.debug("Собираю данные по категориям Invitro.")
    checkups_services = scrapper.get_checkups()
    complexes_categories = scrapper.get_categories_complexes()
    # tests_categories = scrapper.get_categories_tests()
    for i in [checkups_services, complexes_categories]:
        if type(i) is str:
            logger.error(f"При сборе категории Invitro возникла ошибка - {i}. Попробуйте еще раз.")
            return None
    logger.info("Успешно получил данные по категориям.")

    # crv_cnt_1 = worker(tests_categories, table, scrapper)
    crv_cnt_2 = worker(complexes_categories, table, scrapper, "complexes")
    crv_cnt_3 = len(checkups_services)
    add_to_table(checkups_services, table)

    logger.warning(f"Данные по услугам успешно получены. Всего получено {crv_cnt_2+crv_cnt_3} позиций")


if __name__ == "__main__":
    main()