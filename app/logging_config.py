import logging
import sys

logger = logging.getLogger("backoffice")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
handler.setFormatter(formatter)

logger.addHandler(handler)

