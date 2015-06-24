# Implements a bayes network
# (C) have to figure this one out
# 2014-28-2
# Instituto Technologico de Costa Rica 

import sys
from numpy import *
import simplejson as json

# Variable inplements a discrete event
class Variable:
    def __init__(self, name, descr='', domain=['T','F']):
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

    def for_json(self):
        return {'name':self.name, 'description' : self.description,'cardinality': self.cardinality, 'domain': self.domain}

    @staticmethod
    def dictToVariable(dct):
        """This function creates a Variable from an
        dictionary of Variable of Json Decoding
        """
        if(type(dct) is dict):
            try:
                return Variable(dct['name'],dct['description'], dct['domain'])
            except:
                print('unable to convert the dictionary to variable %s', dct) 

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
        self.name = ''
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

    def for_json(self):
        return {"name": self.name,"variables": [v.name for v in self.variables],"values": [w for w in self.values]}

    # this function should sum over the variables in varList and
    # return the resulting factor
    def marginalize(self, varList):
        # extract the indeces for the variables indicated in varList
        indeces = sort(asarray([nonzero(self.variable_names == varname)[0][0] for varname in varList]))[::-1]
        # add dimensions according to each variable cardinality
        reshaped_values = self.values.reshape(self.cardinality)
        # for each variable and its index: sum out its dimension and delete it from the list
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

    @staticmethod
    def dictToFactor(dct):
        """This function takes the array of factors from json decoding and creates a dictionary of factors
        {'factorName':factorInstance} as seen in test.py
        """
        if(type(dct) is dict):
            try:
                return dict([[f.name, Factor(f.variables,f.values)] for f in dct])
            except:
                print('unable to convert the dictionary to factors %s', dct) 

# factorProd Computes the product of two factors.
#   c = factorProd(f1,f2) computes the product between two factors, A and B,
#   where each factor is defined over a set of variables with given dimension.
def factorProduct(factor1,factor2):
    vars = unique(concatenate([factor1.variables, factor2.variables]))
    varsCard = reduce(lambda x,y: x*y, [v.cardinality for v in vars])
    values = zeros(varsCard)
    return Factor(vars, values)

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

    def for_json(self):
        for key in self.factors:
            self.factors[key].name = key
        return {"name": self.name, "variables": self.variables, "factors": self.factors}

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
        """ Algorithm MCMC-ASK(X,e,bn,N) in chapter 14 of AIMA book
        function GIBBS-ASK(X , e, bn,N ) returns an estimate of P(X|e)
        local variables: N, a vector of counts for each value of X , initially zero
        Z, the nonevidence variables in bn
        x, the current state of the network, initially copied from e
        initialize x with random values for the variables in Z
        for j = 1 to N do
            for each Zi in Z do
                set the value of Zi in x by sampling from P(Zi|mb(Zi))
                N[x] N[x] + 1 where x is the value of X in x
        return NORMALIZE(N)"""
        
        N = zeros(lenght(X))
        Z = self._nonEvidenceVariables(evidence)
        x = self._create_random_x(Z, evidence)

        for i in range(numTries):
            for zi in Z:
                mb = self.markovBlanketSample(zi, x)
                probability = self.rejectionSampling(zi.variable, mb, 50)
                x[zi] = probability

        return normalize(N)
        
    def markovBlanketSample(zi, x):
        mb = _self._markovBlanket(zi)
        return _mbSample(mb, x)
        
    def _markovBlanket(self, node):
        """
        Markov blanket contains node's parent nodes, node's children and node's
        children's parents
        :return list(BayesNetNode): list of nodes that form Markov blanket for a given node
        """
        markovBlanket = []
        return markovBlanket
    
    def _mbSample(self, markovBlanket, x):
        mb = []
        return mb    
        
    def normalize(prob):
        return []

def as_net(dct):
    """converts a dict from json decoder to a Net
    """
    name = ''
    variables = []
    factors = []
    if 'name' in dct:
        name = dct['name']
    if 'variables' in dct:
        variables = map(Variable.dictToVariable, dct['variables'])
    if 'factors' in dct:
        # Pending to replace the array of variables names on each factor with the array of variables instances
        # it needs to lookup in 'variables above for the instances'
        _factors = [] # do the replacement of the varialbles here. dct['factors']
    #factors = map(Factor.dictToFactor, _factors)
    return Net(name,variables,_factors, '') 

def loadNet(JSONfile):
    """Loads an Net object from a JSON file.
    """
    net = {}
    try:
        fd = open(JSONfile, 'r')
        text = fd.read()
        fd.close()
        net = json.loads(text)
        net = as_net(net)
    except:
        print('could not load:', JSONfile)
    return net

def dumpNet(net, filename=''):
    """Dumps a Net object to a JSON file.
    """
    if isinstance(net, Net):
        fn = net.name + '.json'
        if filename != '':
            fn = filename
        elif net.JSONfile != '':
            fn = net.JSONfile
        fp = open(fn, 'w')
        json.dump(net,fp=fp,use_decimal=False, for_json=True, indent=4 * ' ')
        fp.close()
    else:
        raise TypeError(repr(net) + " is not JSON serializable")

if __name__ == '__main__':

    filename = ''
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    elif len(sys.argv) == 3:
        filename = sys.argv[2]
    if filename != '':
        _net = loadNet(filename)
