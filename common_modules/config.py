import os
import configparser
import sys
from dataclasses import dataclass, field

__all__ = ["config"]

CONFIG_FILE_NAME = "config.conf"

PRIORITY_CONFIG_FILE_PATH = os.path.join("/etc/yuanxun", CONFIG_FILE_NAME)

run_path1 = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "etc", CONFIG_FILE_NAME)
run_path2 = os.path.join(os.path.dirname(__file__), "etc", CONFIG_FILE_NAME)

SECONDARY_CONFIG_FILE_PATH = run_path1 if os.path.exists(run_path1) else run_path2

CONFIG_FILE_PATH = PRIORITY_CONFIG_FILE_PATH if os.path.exists(PRIORITY_CONFIG_FILE_PATH) else SECONDARY_CONFIG_FILE_PATH

print(CONFIG_FILE_PATH)

conf = configparser.ConfigParser()
conf.read(CONFIG_FILE_PATH)


# 读取配置文件
def get_option(section, option):
    """
    :return:返回配置信息
    """
    option = conf.get(section, option)
    return option


class Config:
    mysql = None
    kafka = None
    elasticsearch = None
    mqtt = None
    rabbitmq = None
    redis = None
    client = None

    @dataclass()
    class Mysql:
        host: str
        port: int
        username: str
        password: str

    @staticmethod
    def __init_mysql():
        section = "mysql"
        host = get_option(section, "host")
        port = int(get_option(section, "port"))
        username = get_option(section, "username")
        password = get_option(section, "password")
        return Config.Mysql(host, port, username, password)

    @dataclass()
    class Kafka:
        host: str

    @staticmethod
    def __init_kafka():
        section = "kafka"
        host = get_option(section, "host")
        return Config.Kafka(host)

    @dataclass()
    class Elasticsearch:
        hosts: field(default=[])
        port: int
        username: str
        password: str

    @staticmethod
    def __init_elasticsearch():
        section = "elasticsearch"
        hosts = get_option(section, "host").split(",")
        port = int(get_option(section, "port"))
        username = get_option(section, "username")
        password = get_option(section, "password")
        return Config.Elasticsearch(hosts, port, username, password)

    @dataclass()
    class Mqtt:
        host: str
        port: int
        username: str
        password: str

    @staticmethod
    def __init_mqtt():
        section = "mqtt"
        host = get_option(section, "host")
        port = int(get_option(section, "port"))
        username = get_option(section, "username")
        password = get_option(section, "password")
        return Config.Elasticsearch(host, port, username, password)

    @dataclass()
    class Rabbitmq:
        host: str
        port: int
        username: str
        password: str

    @staticmethod
    def __init_rabbitmq():
        section = "rabbitmq"
        host = get_option(section, "host")
        port = int(get_option(section, "port"))
        username = get_option(section, "username")
        password = get_option(section, "password")
        return Config.Rabbitmq(host, port, username, password)

    @dataclass()
    class Redis:
        host: str
        port: int
        password: str

    @staticmethod
    def __init_redis():
        section = "redis"
        host = get_option(section, "host")
        port = int(get_option(section, "port"))
        password = get_option(section, "password")
        return Config.Redis(host, port, password)

    @dataclass()
    class Client:
        logger_level: str
        client_id: str

    @staticmethod
    def __init_client():
        section = "client"
        logger_level = get_option(section, "log")
        client_id = get_option(section, "clientid")

        return Config.Client(logger_level, client_id)

    @dataclass()
    class Nacos:
        host: str
        port: int
        username: str
        password: str
        context_path: str

    @staticmethod
    def __init_nacos():
        section = "nacos"
        host = get_option(section, "host")
        port = int(get_option(section, "port"))
        username = get_option(section, "username")
        password = get_option(section, "password")
        context_path = get_option(section, "context_path")
        return Config.Nacos(host, port, username, password, context_path)

    def __init__(self):
        self.mysql = self.__init_mysql()
        self.kafka = self.__init_kafka()
        self.elasticsearch = self.__init_elasticsearch()
        self.mqtt = self.__init_mqtt()
        self.rabbitmq = self.__init_rabbitmq()
        self.redis = self.__init_redis()
        self.client = self.__init_client()
        self.nacos = self.__init_nacos()


config = Config()
if __name__ == "__main__":
    print(config.__dict__)
