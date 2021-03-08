# rmse.py
#
# This is a naive root mean squared error (RMSE) calculation, 
# rmse = root(mean((x - y)^2))
#
# If the input vectors differ, it takes the first N elements of each
# so that the size is the same. Error is computed pairwise without regard
# to the timestamps.
#
# Caleb Phillips <caleb.phillips@nrel.gov>
# Joseph Lee <joseph.lee@nrel.gov>


import numpy as np

class rmse:

  def compute(self,x,y):

    print(x)

    print('mean')
    print(x.mean())

    print(x.values[0:3])
    print(np.mean(x.values[0:3]))
    print(np.mean(x.values))

    x1 = x.to_numpy().copy()
    print(type(x1))

    # #print(x.values)
    # #x1 = np.copy(x)
    # x1 = x.copy()
    # y1 = np.copy(y)
    # #a = np.mean(x.values)
    print(x1.flags)
    # x1.setflags(write=1)
    print(np.array(x1))
    print(np.mean(np.array(x1)))

    # # just values (second member of tuple)
    # # note: this isn't time aligning at all, just compares the 
    # #       values as they arrive
    # x = x.to_numpy()[:,0]
    # y = y.to_numpy()[:,0]

    # # naively truncate longer array if one is shorter
    # if len(x) > len(y):
    #   x = x[0:len(y)]
    # if len(y) > len(x):
    #   y = y[0:len(x)]

    # # print(np.array(x))
    # # print(np.array(y))

    # print(np.mean((np.array(x))))
    # print(float(np.sqrt(np.mean((np.array(x))))))
      
    # return float(np.sqrt(np.mean((np.array(x) - np.array(y))**2)))

    return float(np.sqrt(np.mean(x - y)**2))