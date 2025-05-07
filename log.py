import os

import adafruit_logging as logging

_level = os.getenv('log_level')
_logger = logging.getLogger()
if _level == 'null':
    _logger.addHandler(logging.NullHandler())
if _level != None and _level != 'null':
    _logger.setLevel(_level)
critical = _logger.critical
debug = _logger.debug
error = _logger.error
exception = _logger.exception
info = _logger.info
log = _logger.log
setLevel = _logger.setLevel
warning = _logger.warning
