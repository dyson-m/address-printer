# This program handles reads & writes to address storage
# In this instance, for simplicity: a csv file

# All addresses should be lists formatted as follows:
# [line1, line2, line3]
# Where each line is a string

address_file = "addressData.csv"
log_file = "address_changelog.log"
do_logging = True # Overriden by AUDIT_ENABLED in env
do_log_file = True # Overridden by AUDIT_TO_FILE in env

import csv
from pyap import parse
from pathlib import Path
import logging
import os
from logging.handlers import RotatingFileHandler


AUDIT_EN = os.getenv("AUDIT_ENABLED", do_logging) == "1" or True
AUDIT_TO_FILE = os.getenv("AUDIT_TO_FILE", do_log_file) == "1" or True

audit = logging.getLogger("address_audit")
audit.setLevel(logging.INFO)
audit.propagate = False

if not audit.handlers:
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    # stdout -> gunicorn captures it
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    audit.addHandler(sh)

    # optional logging to file
    if AUDIT_TO_FILE:
        fh = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
        fh.setFormatter(fmt)
        audit.addHandler(fh)


# Double checking csv file exists at program start/import
p = Path(address_file)
if not p.exists():
    p.parent.mkdir(parents=True, exist_ok=True)
    p.touch()



def ex_guard(action: str):
    """
    Decorator to wrap function in try/except block
    Will log changes if function also returns a log string
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

                audit_log = None
                if isinstance(data, tuple) and len(data) == 2 and isinstance(data[1], str):
                    data, audit_log = data

                if AUDIT_EN and audit_log:
                    audit.info("<CSV> %s", audit_log)

                return data, None
            except Exception as e:
                if AUDIT_EN:
                    audit.exception("!CSV! %s failed", action.upper())
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
        raise TypeError("Invalid type; not str or len(list) == 3")
    parsedAddresses = parse(address, country = 'US')

    if parsedAddresses: 
        return True 

    return False


@ex_guard("delete")
def delAddress(address) -> bool:
    tempRows = []
    log_string = None
    with open(address_file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row !=address:
                tempRows.append(row)
            else:
                log_string = f"DELETED: {addr_to_str(address)}"
    
    with open(address_file, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(tempRows)

    if log_string:
        return True, log_string
    else:
        raise TypeError("Address to be deleted was not found")


@ex_guard("write")
def writeAddress(newAddress, oldAddress=None) -> bool:
    tempRows = []
    if oldAddress:
        if newAddress == oldAddress:
            raise TypeError("Address unchanged")
        with open(address_file, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row == oldAddress:
                    row = newAddress
                tempRows.append(row)
        with open(address_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(tempRows)
        return True, f"EDITED: {addr_to_str(oldAddress)} -> {addr_to_str(newAddress)}"
    else:
        with open(address_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(newAddress)
        return True, f"ADDED: {addr_to_str(newAddress)}"

@ex_guard("read")
def readAddresses() -> list:
    # fileReader = csv.reader(address_file, dialect="excel")
    with open(address_file, newline="") as f:
        rows = [row for row in csv.reader(f, dialect="excel")]
    return rows

def addr_to_str(address: list) -> str:
    """
    Tranforms an address list into a csv/human readable string
    
    :param address: An address, formatted [line1, line2, line3]
    :type address: list containing 3 strings
    :return: CSV-like string
    :rtype: str
    """
    return f'{address[0]},{address[1]},"{address[2]}"'