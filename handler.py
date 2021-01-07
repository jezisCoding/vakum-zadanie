from dbconnector import DBConnector
from dicttoxml import dicttoxml

def get_by_exact_name(name):
    """
    Returns the trademark objects exactly matching the name parameter
    """
    dbc = DBConnector()
    dbc.connect()

    # Search case sensitively
    result = dbc.select_where(name)

    dbc.disconnect()
    return dicttoxml(result).decode("utf-8")

def get_by_approx_name(name):
    """
    Returns the trademark objects closely matching the name parameter
    """
    dbc = DBConnector()
    dbc.connect()

    # Search case insensitively
    result = dbc.select_where(name, False)

    dbc.disconnect()
    return dicttoxml(result).decode("utf-8")

if __name__ == "__main__":
    tm = ("al", "al", "sl", "mf", "mvet")
    print(dicttoxml(tm).decode("utf-8"), flush=True)
    #print(get_by_exact_name("VERIFAI"))
    #print(get_by_exact_name("Verifai"))
    #print(get_by_approx_name("Verifai"))
