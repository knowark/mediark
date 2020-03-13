from typing import Dict, List, Any, Union, Tuple

MediaDict = Dict[str, Any]

AudioDict = Dict[str, Any]

AudioDictList = List[AudioDict]

ImageDict = Dict[str, Any]

ImageDictList = List[ImageDict]

MediaDictList = List[MediaDict]

TermTuple = Tuple[str, str, Union[str, int, float, bool, list, tuple]]

QueryDomain = List[Union[str, TermTuple]]

SearchDomain = List[Union[str, TermTuple]]
