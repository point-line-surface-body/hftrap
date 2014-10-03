import sys
import numpy
from sklearn.linear_model import LinearRegression 

USAGE = 'USAGE: EXEC REG_DATA_FILE REG_OUT_FILE'
if (len(sys.argv) < 3):
    print USAGE
    exit(0)
    
model = LinearRegression(fit_intercept=False, normalize=False)

reg_data_numpy = numpy.loadtxt(sys.argv[1])
X = reg_data_numpy[:, 1:]  # select columns 1 through end
y =  reg_data_numpy[:, 0]   # select column 0
model.fit(X, y)
coefficients = model.coef_ 

reg_out = open(sys.argv[2], 'w')

for i in range(0, len(coefficients)):
    if (coefficients[i] != 0):
        reg_out.write(str(i+1)+' '+str(coefficients[i])+'\n')

reg_out.close()