trademarks = "NANI"
trademarks = {'a':'brekeke', 'b':'clekeke'}

def getByExactName():
    return "sugondese"
def getByApproximateName():
    return "ligma?"

# Here we define API call handlers

def getByExactName(name):
    """
    :returns: trademark object matching the name parameter.
    """
    return trademarks[name]

def getByApproximateName(name):
    """
    :returns: all trademark objects closely matching the name parameter.
    """
    return "nieeee"
    #return trademarks.search(name)

# API call handlers end here


