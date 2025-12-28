# What this needs to do:
# Read CSV file 
# Take original address and inputted address
# Functions:
# 
# TODO: maybe this should be implemented so that a different method of
#       storing the address data (SQL, etc) can easily be dropped in
#           -replace: where addresses are read in routes
#                     where address is validated in printer.py

# All addresses should be lists formatted as follows:
# [line1, line2, line3]
# Where each line is a string

import csv
from pyap import parse


address_file = "addressData.csv"


def ex_guard(action: str):
    """
    Decorator to wrap function in try/except block
    Returns: (data, err)
    - data: any datatype or None
    - err: string or None
    :param action: Indicates function purpose to include in error message
    :type action: str
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                data = func(*args, **kwargs)
                return data, None
            except Exception as e:
                return None, f"[CSV:{action}] {e}"
        return wrapper
    return decorator


@ex_guard("validate")
def validateAddress(address) -> bool:
    """
    Determines if a given address matches standard US formatting
    
    :param address: String or list containing the address to validate
    :return: True if address matches normal conventions, else False
    :rtype: bool
    """
    if type(address) == list and len(address) == 3:
        address = ' '.join(address)
    if type(address) != str:
        raise "Invalid type; not str or len(list) == 3"
    parsedAddresses = parse(address, country = 'US')

    if parsedAddresses: 
        return True 

    return False


@ex_guard("delete")
def delAddress(address) -> bool:
    tempRows = []
    with open(address_file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row !=address:
                tempRows.append(row)
    
    with open(address_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(tempRows)
    #TODO: make a second file containing all the deleted/edited entries?
    return True


@ex_guard("write")
def writeAddress(newAddress, oldAddress=None) -> bool:
    tempRows = []
    if oldAddress:
        with open(address_file, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row == oldAddress:
                    row = newAddress
                tempRows.append(row)
        with open(address_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(tempRows)
    else:
        with open(address_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(newAddress)
    return True

@ex_guard("read")
def readAddresses() -> list:
    # fileReader = csv.reader(address_file, dialect="excel")
    with open(address_file, newline="") as f:
        rows = [row for row in csv.reader(f, dialect="excel")]
    return rows