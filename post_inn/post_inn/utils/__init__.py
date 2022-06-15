import logging

from post_inn.settings import IS_DEV_SERVER

logger = logging.getLogger('main_prod') if IS_DEV_SERVER else logging.getLogger('main_local')
