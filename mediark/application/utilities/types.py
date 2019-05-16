from typing import List, Dict, Union, Tuple, Any, TypeVar

T = TypeVar('T')

TermTuple = Tuple[str, str, Union[str, int, float, bool, list, tuple]]

QueryDomain = List[Union[str, TermTuple]]
