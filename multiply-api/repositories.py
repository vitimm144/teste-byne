from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass
class INumber:
    number: int
    timestamp: datetime


class INumberRepository(ABC):
    @abstractmethod
    def save(data: INumber) -> None:
        pass

    @abstractmethod
    def get() -> list:
        pass

    @abstractmethod
    def connect() -> None:
        pass