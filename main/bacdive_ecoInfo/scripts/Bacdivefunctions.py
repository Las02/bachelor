import numpy as np

class nandict():
    """Quick class to return nan instead of Keyerror when trying to get a key which is not present
        Used to not crash program when attributes are not present but instead add nans
    """
    def __init__(self, dict):
        self.dict = dict
    def __getitem__(self, index):
        try: 
            return self.dict[index]
        except KeyError:
            return np.nan


def get_bacDat(to_get: list, strain_dat:dict, dat_type) -> dict:
    import statistics
    
    tmp_dict = dict()
    # If strain_dat is not a list then there is only one ref
    # add it to the bacDat dict
    if type(strain_dat) is not list:
        for get in to_get:
            try:
                tmp_dict[get] = strain_dat[get]
            except KeyError:
                pass
        return tmp_dict
    
    
    # Go through each entry
    for entry in strain_dat: 
        # Get the requested info from to_get
        for get in to_get:
            try:
                if get in tmp_dict:
                    tmp_dict[get] = tmp_dict[get] + [entry[get]]
                else:
                    tmp_dict[get] = [entry[get]]
                    
            except KeyError:
                pass
    return tmp_dict
    
def GetPH_or_Temp(to_get: str, strain_dat:dict, dat_type):
    
    opt  = get_bacDat([to_get, "type"], strain_dat, dat_type)
    
    tmp_dict = dict()
    
    try:
        for entry in zip(opt["temperature"],opt["type"]):
            if entry[1] == "growth":
                temp_range = entry[0]
                #temp_range.split("-")
                #tmp_dict["min"] = temp_range[0]
                #tmp_dict["max"] = temp_range[1]
                tmp_dict["range"] = temp_range
            elif entry[1] == "optimum":
                tmp_dict["optimum"] = entry[0]
    except KeyError:
        pass
    
    return tmp_dict
    