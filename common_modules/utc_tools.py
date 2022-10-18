from datetime import datetime, timedelta

UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def get_utc():
    """

    :return:  str : 2021-10-20T02:17:37.841025Z
    """

    return datetime.utcnow().strftime(UTC_FORMAT)
