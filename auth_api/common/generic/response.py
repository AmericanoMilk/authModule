from dataclasses import dataclass, field


@dataclass()
class Response:
    code: int = 200
    msg: str = ""
    data: dict = field(default_factory=dict)


@dataclass()
class PageResult:
    totalPage: int = 0
    result: list = field(default_factory=list)
