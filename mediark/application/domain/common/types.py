from typing import (Sequence, List, Dict, Union, Tuple, Any,
                    TypeVar, MutableMapping)


TermTuple = Tuple[str, str, Union[str, int, float, bool, list, tuple]]

QueryDomain = Sequence[Union[str, TermTuple]]

DataDict = MutableMapping[str, Any]

RecordList = List[DataDict]
