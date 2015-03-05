# file for testing bayes.py

# operations are in comments
# desired values are put by hand
# uncommenting the operations should give the same result

import bayes

x1 = bayes.Variable(name='X1', domain=['T','F'])
x2 = bayes.Variable(name='X2', domain=['0','1'])
x3 = bayes.Variable(name='X3', domain=['high', 'low'])

factor = {}

# factor contains P[X1]
factor['p(x1)'] = bayes.Factor(vars=[x1], values=[0.11, 0.89])

# factor contains P[X2|X1]
factor['p(x2|x1)'] = bayes.Factor(vars=[x2,x1], values=[0.59, 0.41, 0.22, 0.78])

# factor contains P[X3|X2]
factor['p(x3|x2)'] = bayes.Factor(vars=[x3,x2], values=[0.39, 0.61, 0.06, 0.94])

# factors['product'] = factorProduct(factor['p(x1)'], factor['p(x2|x1)'])
factor['product'] = bayes.Factor([x1,x2], [0.0649, 0.01958, 0.0451, 0.6942])

# factors['marginal1'] = factor['p(x2|x1)'].marginalize(['X2'])
factor['marginal1'] = bayes.Factor(vars=[x1], values=[1.0, 1.0])

# [factor['e1'], factor['e2'], factor['e3']] = 
#              bayes.observeEvidence([factor['p(x1)'], 
#                                     factor['p(x2|x1)'],
#                                     factor['p(x3|x2)']], 
#                                     {'X2':'0', 'X3':'low'})

factor['e1'] = bayes.Factor(vars=[x1], values=[0.11, 0.89])
factor['e2'] = bayes.Factor(vars=[x2,x1], values=[0.59, 0.0, 0.22, 0.0])
factor['e3'] = bayes.Factor(vars=[x3,x2], values=[0.0, 0.61, 0.0, 0.0])

# factor['joint'] = bayes.jointDistribution([factor['p(x1)'], 
#                                            factor['p(x2|x1)'],
#                                            factor['p(x3|x2)']])

factor['joint'] = bayes.Factor(vars= [x1,x2,x3], values=[0.025311, 0.076362, 
                                                         0.002706, 0.041652,
                                                         0.039589, 0.119438,
                                                         0.042394, 0.652548])

# factor['marginal'] = bayes.marginal([x2,x3],
#                                     [factor['p(x1)'], 
#                                      factor['p(x2|x1)'],
#                                      factor['p(x3|x2)']],
#                                      {'X1':'F'})
factor['marginal'] = bayes.Factor([x2,x3], values=[0.0858, 0.0468, 0.1342,
                                                   0.7332])
