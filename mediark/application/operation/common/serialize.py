def dump(item):
    result = vars(item)
    result["transations"] = {}
    return result
