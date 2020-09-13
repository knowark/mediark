from typing import Dict, List, Any, Union, Tuple

MediaDict = Dict[str, Any]

MediaDictList = List[MediaDict]

TermTuple = Tuple[str, str, Union[str, int, float, bool, list, tuple]]

QueryDomain = List[Union[str, TermTuple]]

SearchDomain = List[Union[str, TermTuple]]
