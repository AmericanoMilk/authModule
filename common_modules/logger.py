import logging
import sys

# from config import config


class Logger:
    __instance = None
    __logger_names = {}

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @staticmethod
    def get_logger(*, level: str = "DEBUG", logger_name="common_modules") -> logging.RootLogger:
        if logger_name not in Logger.__logger_names:
            # 获取logger实例，如果参数为空则返回root logger
            _logger = logging.getLogger(logger_name)
            # 指定logger输出格式
            formatter = logging.Formatter("%(levelname)s %(pathname)s:%(lineno)d %(asctime)s %(message)s")
            # 控制台日志
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.formatter = formatter  # 也可以直接给formatter赋值
            _logger.addHandler(console_handler)
            # 指定日志的最低输出级别，默认为WARN级别
            _logger.setLevel(getattr(logging, level.upper()))
            Logger.__logger_names[logger_name] = _logger
        return Logger.__logger_names[logger_name]


logger = Logger.get_logger(level="debug")
