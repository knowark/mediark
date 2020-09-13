from typing import Sequence, Dict, List, Union, Tuple, Any, MutableMapping

TermTuple = Tuple[str, str, Union[str, int, float, bool, list, tuple]]

QueryDomain = Sequence[Union[str, TermTuple]]

DataDict = MutableMapping[str, Any]

RecordList = List[DataDict]

ImageDict = Dict[str, str]

AudioDict = Dict[str, str]

#DataDict = Dict[str, str]

MediaDict = MutableMapping[str, Any]

MediaDictList = List[MediaDict]
