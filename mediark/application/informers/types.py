from typing import Dict, List, Any, Union, Tuple, MutableMapping, Sequence

#MediaDict = Dict[str, Any]


TermTuple = Tuple[str, str, Union[str, int, float, bool, list, tuple]]

#QueryDomain = List[Union[str, TermTuple]]

#SearchDomain = List[Union[str, TermTuple]]


QueryDomain = Sequence[Union[str, TermTuple]]

MediaDict = MutableMapping[str, Any]

MediaDictList = List[MediaDict]
