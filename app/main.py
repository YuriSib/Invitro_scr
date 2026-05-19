import time
from random import randint

from app.utils.logger import logger
from app.utils.xl_worker import ExcelTable
from app.parse.scrapper import InvitroScrapper
from config import TABLE_PATH


def main():
    table = ExcelTable(TABLE_PATH)
    scrapper = InvitroScrapper()

    logger.debug("Собираю данные по категориям Invitro.")
    categories = scrapper.get_categories()
    if type(categories) is str:
        logger.error(f"При сборе категории Invitro возникла ошибка - {categories}. Попробуйте еще раз.")
        return None
    logger.info("Успешно получил данные по категориям.")

    # В этом цикле будут использоваться рандомные ожидания для того,
    # чтобы сервис Invitro не заблочил наш парсер по IP-адресу.
    for category_title, category_id in categories.items():
        time_sleep = randint(5, 12)
        logger.debug(f"Жду {time_sleep} секунд")
        time.sleep(time_sleep)
        logger.info(f"Начинаю обрабатывать категорию {category_title}")

        table.add_category_row(category_title)

        logger.debug(f"Получаю данные по анализам для категории {category_title}")
        services = scrapper.get_services(category_id)

        if type(services) is str:
            logger.error(f"Не удалось получить данные по категории.")
            return None

        logger.debug(f'Вставляю полученные данные в таблицу.')
        result = table.add_services(services)
        if result != "OK":
            logger.error(f"Возникла ошибка при попытке вставить данные в таблицу. {result}")
            return None
        logger.debug('Данные вставлены успешно.')
        table.save()


if __name__ == "__main__":
    main()