import logging
from colorama import init, Fore
from copy import copy
from threading import Lock

class ColoredFormatter(logging.Formatter):
    COLOR_MAP = {
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "DEBUG": Fore.CYAN
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.colored_format = '%(asctime)s.%(msecs)03d - {}%(levelname)s{} - %(message)s'.format(Fore.RESET, Fore.RESET)

    def format(self, record):
        colored_record = copy(record)
        levelname = colored_record.levelname
        color = self.COLOR_MAP.get(levelname, "")
        colored_record.levelname = f"{color}{levelname}{Fore.RESET}"
        return super().format(colored_record)


class HandleLog:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        init(autoreset=True)
        self.logger = logging.getLogger('PlaywrightLogger')
        self.logger.setLevel(logging.DEBUG)
        self.log_file_handlers = {}
        self.logger.propagate = False

        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = ColoredFormatter(
            '%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def add_file_handler(self, log_file_name):
        if log_file_name not in self.log_file_handlers:
            file_handler = logging.FileHandler(log_file_name, mode='w', encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '[%(asctime)s.%(msecs)03d - %(levelname)s] %(message)s',
                datefmt='%H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            self.log_file_handlers[log_file_name] = file_handler

    def remove_file_handler(self, log_file_name):
        if log_file_name in self.log_file_handlers:
            handler = self.log_file_handlers[log_file_name]
            handler.close()
            self.logger.removeHandler(handler)
            del self.log_file_handlers[log_file_name]

    def info_log(self, message):
        try:
            self.logger.info(message)
        except (ValueError, OSError, AttributeError):
            pass
        except Exception:
            pass

    def warning_log(self, message):
        try:
            self.logger.warning(message)
        except (ValueError, OSError, AttributeError):
            pass
        except Exception:
            pass

    def error_log(self, message):
        try:
            self.logger.error(message)
        except (ValueError, OSError, AttributeError):
            pass
        except Exception:
            pass

    def debug_log(self, message):
        try:
            self.logger.debug(message)
        except (ValueError, OSError, AttributeError):
            pass
        except Exception:
            pass
