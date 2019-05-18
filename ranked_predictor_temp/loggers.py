import logging
import logging.config
import os
from os import path

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

req_logger = logging.getLogger('requests')

mod_logger = logging.getLogger('modeller')

