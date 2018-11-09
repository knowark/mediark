from typing import Dict, List, Any, Union, Tuple


ImageDict = Dict[str, Any]

ImageDictList = List[ImageDict]

AudioDict = Dict[str, Any]

AudioDictList = List[AudioDict]

TermTuple = Tuple[str, str, Union[str, int, float, bool, list, tuple]]

SearchDomain = List[Union[str, TermTuple]]
