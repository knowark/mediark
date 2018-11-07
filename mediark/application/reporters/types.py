from typing import Dict, List, Any, Union, Tuple


ImageDict = Dict[str, Any]

ImageDictList = List[ImageDict]

TermTuple = Tuple[str, str, Union[str, int, float, bool, list, tuple]]

SearchDomain = List[Union[str, TermTuple]]
