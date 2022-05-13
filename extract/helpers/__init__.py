import logging as __logging

__logging.basicConfig(
    level=__logging.INFO,
    format='%(levelname)s: %(asctime)s - %(message)s'
)

log = __logging.getLogger()
