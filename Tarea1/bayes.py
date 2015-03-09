# Implements a bayes network
# (C) have to figure this one out
# 2014-28-2
# Instituto Technologico de Costa Rica 

from numpy import *

# Variable inplements a discrete event
class Variable:
    def __init__(self, name='', descr='', domain=['T','F']):
        self.name = name
        self.description = descr
        self.cardinality = len(domain)
        self.domain = domain

    def __str__(self):
        output = ""
        output += "[Variable %s]\n" % self.name
        output += "Description:\t%s\n" % self.description
        output += "Cardinality:\t%s\n" % self.cardinality
        output += "Domain:     \t%s\n" % self.domain
        return output

    def __repr__(self):
        return self.__str__()

    def toString(self):
        output = ""
        output += "{'%s','%s',%s,%s}" % (self.name,self.description,self.cardinality,self.domain)
        return output

# Factor: function from a list of variables to a numeric value
class Factor:
    # __init__ constructor
    #
    # 1. Variables order is relevant
    # 2. Variables are stored in vector named variables
    # 3. Variables cardinality are stored in vector named cardinality
    # 4. Values shall be implemented as a vector (eventually numpy array)
    # 5. A dictionary shall be stored in map, that maps variables names to values indices
    #    map['T'+'Good'] -> value (depending on variables)
    # 6. Values shall be initialized to 0's
    def __init__(self, variables=[], values=[]):
        # save variables
        self.variables = array(variables)
        # initialize variables names array
        self.variable_names = array([v.name for v in variables])
        # initialize cardinality array
        self.cardinality = array([v.cardinality for v in variables])
        card = prod(self.cardinality)
        # implement as numpy array right filled with zeroes
        self.values = zeros(card)
        max_values = min(card, len(values))
        self.values[0:max_values] = array(values[0:max_values])
        # map variable names to variable values
        self.map = self.__map_vars_values__(self.variables)

    # map variables names to values indices
    def __map_vars_values__(self, variables):
        # make sequences values array
        sequences = array([asarray(v.domain) for v in variables])
        # construct an open mesh from sequences
        broadcastable = ix_(*sequences)
        # broadcast arrays against each other
        broadcasted = broadcast_arrays(*broadcastable)
        # rows = product of cardinalities, cols = number of sequences
        rows, cols = reduce(multiply, broadcasted[0].shape), len(broadcasted)
        # empty target array
        out = empty(rows * cols, dtype=broadcasted[0].dtype)
        start, end = 0, rows
        # flatten one sequence at a time
        for a in broadcasted:
            # flatten sequence dimension
            out[start:end] = a.reshape(-1)
            start, end = end, end + rows
        # reshape, transpose and return each product concatenated as a string
        keys = map("".join, out.reshape(cols, rows).T)
        # create map from keys to values indices
        return dict(zip(keys, array(arange(0, rows))))

    def __str__(self):
        output = ""
        output += "[Factor]\n"
        output += "Variables:  \t%s\n" % [v.name for v in self.variables]
        output += "Values:     \t%s\n" % self.values
        output += "Map:        \t%s\n" % self.map
        output += "Cardinality:\t%s\n" % self.cardinality
        return output

    def __repr__(self):
        return self.__str__()

    def toString(self):
        output = ""
        output += "{'%s', '%s', %s, %s}" % ([v.name for v in self.variables], self.values, self.map, self.cardinality)
        return output

    # this function should sum over the variables in varList and
    # return the resulting factor
    def marginalize(self, varList):
        indeces = sort(asarray([nonzero(self.variable_names == idx)[0][0] for idx in varList]))[::-1]
        reshaped_values = self.values.reshape(self.cardinality)
        marginalizedFactor = Factor(delete(self.variables, indeces), map(lambda idx: sum(reshaped_values, axis = idx), indeces)[0].tolist())
        return marginalizedFactor

    # retrieve the value of factor for a given combinations of values 
    # of the variables from the factor array
    def getValue(self, values):
        return 0

    # retrieve the value of factor for a given combination of values
    # of the variables from the factor array using the indexes
    def getValueIdx(self, idxList):
        return 0

    # see setValue
    def setValue(self, values, val):
        return 0

    # see setValueIdx
    def setValueIdx(self, valIdx, val):
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
#   M = marginal(variables, factors, evidence) computes the marginal over variables
#   variables in the distribution induced by the set of factors, given the evidence
#
def marginal(variables, factors, evidence):
    return Factor()

class Net:
    def __init__(self, name='', variables=[], factors=[], JSONfile=''):
        self.name = name
        self.variables = variables
        self.factors = factors
        self.JSONfile = JSONfile

    def setVariables(self, variables):
        self.variables = variables

    def setFactors(self, factors):
        self.factorts = factors

    def marginal(self, variables, evidence):
        return marginal(variables, self.factors, evidence)

    def priorSample(self):
        # algorithm PRIOR-SAMPLE(bn) in chapter 14 of AIMA book
        return []

    def rejectionSampling(self, varNameVector, evidence, numTries):
        # algorithm REJECTION-SAMPLING(X,e,bn,N) in 
        # chapter 14 of AIMA book
        
        return []

    def likelihoodWeighing(self, varNameVector, evidence, numTries):
        # algorithm LIKELIHOOD-WEIGHING(X,e,bn,N) in
        # chapter 14 of AIMA book
        
        return []

    def markovChainMonteCarlo(self, varNameVector, evidence, numTries):
        # algorithm MCMC-ASK(X,e,bn,N) in
        # chapter 14 of AIMA book

        return []

