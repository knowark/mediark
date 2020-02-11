from typing import Dict, List, Any, Union, Tuple

AudioDict = Dict[str, Any]

AudioDictList = List[AudioDict]

ImageDict = Dict[str, Any]

ImageDictList = List[ImageDict]

TermTuple = Tuple[str, str, Union[str, int, float, bool, list, tuple]]

QueryDomain = List[Union[str, TermTuple]]

SearchDomain = List[Union[str, TermTuple]]
