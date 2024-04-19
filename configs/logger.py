import logging

FORMAT: str = "%(levelname)s:   %(message)s"

logging.basicConfig(format=FORMAT, level=logging.NOTSET)
logger = logging.getLogger()
