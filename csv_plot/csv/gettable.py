from abc import ABC, abstractmethod
from typing import Any, Iterator, List, Optional, Union


class Gettable(ABC):
    @abstractmethod
    def __len__(self) -> int:
        ...

    @abstractmethod
    def get(self, start: Optional[Any], stop: Optional[Any]) -> Iterator:
        ...

    @abstractmethod
    def __getitem__(self, index_or_slice: Union[Any, slice]) -> Union[Any, List]:
        ...
