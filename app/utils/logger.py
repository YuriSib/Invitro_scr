from loguru import logger

from config import LOGS_DIR


logger.add(f'{LOGS_DIR}/log.log', rotation='20 mb', level="DEBUG")
logger.add(f'{LOGS_DIR}/info.log', rotation='20 mb', level="INFO")
logger.add(f'{LOGS_DIR}/warning.log', rotation='10 mb', level="WARNING")
logger.add(f'{LOGS_DIR}/errors.log', rotation='10 mb', level="ERROR")
logger.add(f'{LOGS_DIR}/critical.log', rotation='10 mb', level="CRITICAL")


# load_dotenv()

# params = {
#     "token": CNF.BOT_TOKEN,
#     "chat_id": 000000000,
# }

# tg_handler = NotificationHandler(provider='telegram', defaults=params)
# logger.add(tg_handler, level='INFO')


if __name__ == "__main__":
    logger.debug("Уровень Debug")
    logger.info("Уровень Info")
    logger.warning("Уровень Warning")
    logger.error("Уровень Error")
    logger.critical("Уровень Critical Error")


