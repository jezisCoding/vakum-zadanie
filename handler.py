# Test data
trademarks = {'a':'brekeke', 'b':'clekeke'}

# Here we define API call handlers
def getByExactName(name):
    return trademarks[name]

def getByApproximateName(name):
    return "nieeee"
    #return trademarks.search(name)

# API call handlers end here

def searchTrademark(name):
    """
    TODO
    :returns: all trademark objects closely matching the name parameter.
    """
    return ""
