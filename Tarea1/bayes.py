# Implements a bayes network
# (C) have to figure this one out
# 2014-28-2
# Instituto Technologico de Costa Rica 

# Variable inplements a discrete event
class Variable:
    def __init__(self, name='', descr='', domain=['T','F']):
        self.name = name
        self.description = descr
        self.cardinality = len(domain)
        self.domain = domain


# Factor: function from a list of variables to a numeric value
class Factor:
    # __init__ constructor
    # pending
    #     if values == [], then create vector with 0's
    #     initialize map, map['T'+'Good'] -> value (depending on variables)
    #
    def __init__(self, vars=[], values=[]):
        self.vars = vars
        self.values = values
        self.map = {}
        self.cardinality = []

    # this function should sum over the variables in varList and
    # return the resulting factor
    def marginalize(self, varList):
        return Factor()

    # retrieve the value of factor for a given combinations of values 
    # of the variables from the factor array
    def getValue(self, values):
        return 0

    # retrieve the value of factor for a given combination of values
    # of the variables from the factor array using the indexes
    def getValueIdx(self, idxList):
        return 0

    # see getValue
    def setValue(self, values,val):
        return 0

    # see getValueIdx
    def setValueIdx(self, valIdx,val):
        return 0


# factorProd Computes the product of two factors.
#   c = factorProd(f1,f2) computes the product between two factors, A and B,
#   where each factor is defined over a set of variables with given dimension.
def factorProduct(factor1,factor2):
    return Factor()

# this function should modify a set of factors given the observed
# values of the variables in mapValues so the assignment not consistent
# with the observed values should be set to 0, the factors need not be
# renormalized
def observeEvidence(mapValues):
    return Factor()

# jointDistribution Computes the joint distribution defined by a set
# of given factors
#
#   joint = jointDistribution(F) computes the joint distribution
#   defined by a set of given factors
#
#   Joint is a factor that encapsulates the joint distribution given by F
#   F is a list of factors containing the factors 
#     defining the distribution
#
def jointDistribution(factors):
    return Factor()

# marginal computes the marginal over a set of given variables
#   M = marginal(vars, factors, evidence) computes the marginal over variables
#   vars in the distribution induced by the set of factors, given the evidence
#
def marginal(vars, factors, evidence):
    return Factor()
