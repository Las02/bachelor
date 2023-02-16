import numpy as np
import random
from statistics import multimode, mean
import re

def divide_chunks(l, n):
    """Divide list into chunks
       source: https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
    """
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def avg_from_interval(interval):
        """Finds the avg of interval, return none if not interval"""
        found = re.search(r"\d+-\d+",interval)
        if found is not None:
            interval = interval.split("-")
            interval = [float(x) for x in interval]
            return mean(interval)
        return found

def HandleMultiVariables(entry, dat_type):
    """Take dict with list of multiple variables and 
        return dict with only one for each. Choose values
        based on various parameters"""
   
    

    # If there is only one value return it
    if type(entry) is not list:
        # Check for intervals and find avg if any
        if dat_type == "continuous":
           found = avg_from_interval(entry)
           if found is not None:
               entry = found
        return entry
    
    # If its cont list of numbers find mean of all non-intervals
    # If all are intervals return mean of them
    # If it cannot be converted to cont, treat it as nominal
    try:
        if dat_type == "continuous":
            tmp_list = list()
            # Add all numbers which are not intervals to list
            for num in entry:
                found = avg_from_interval(num)
                if found is None:
                    tmp_list.append(num)
            # If all numbers are intervals use the intervals
            if len(tmp_list) == 0:
                for num in entry:
                    found = avg_from_interval(num)
                    if found is not None:
                        tmp_list.append(found)
            tmp_list = [float(x) for x in tmp_list]
            return mean(tmp_list)    
    except ValueError:
        dat_type = "nominal"

    
    # If its nominal values return the mode
    # If several have same count return "random"
    if dat_type == "nominal":
        modes = multimode(entry)
        random_mode = random.choice(modes)
        return random_mode
                
# Test for function above
#dic = {"a":["1","2","2","1"], "b":["2","1-2","10"]}
#
#for key, value in dic.items():                
#    a = HandleMultiVariables(value , "continuous")
#    print(a)

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


def get_key_path_value(key_path, obj, default=None):
    """Safely extract several keys for dict
    source: https://stackoverflow.com/questions/45016931/how-to-use-get-multiple-times-pythonically
    """
    if not key_path:
        return obj
    try:
        for key in key_path:
            obj = obj[key]
    except (KeyError, IndexError):
        return default
    return obj

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

     
    # Ignore handeling of several values if set
    if dat_type == "ignore":
        return tmp_dict

    # Handle several values
    new_dict = dict()
    for key, value in tmp_dict.items():
        cleanValue = HandleMultiVariables(value, dat_type)
        new_dict[key] = cleanValue
    
            
    return new_dict
    
 
def GetPH_or_Temp(to_get: str, strain_dat:dict):
    ## NOT WORKING
    opt  = get_bacDat([to_get, "type"], strain_dat, "ignore")

    tmp_dict = dict()
    

    try:
        for temp, type in zip((opt["temperature"],),opt["type"]):
            if type == "growth":
                temp_range = HandleMultiVariables(temp, "continuous")
                #temp_range.split("-")
                #tmp_dict["min"] = temp_range[0]
                #tmp_dict["max"] = temp_range[1]
                tmp_dict["growth"] = temp_range
            elif type == "optimum":
                tmp_dict["optimum"] = HandleMultiVariables(temp, "continuous")
    except KeyError:
        pass

    
    return tmp_dict
    