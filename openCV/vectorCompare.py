#Generate two random arrays, shape must be the same
>>> Mt = np.random.rand(2,2)
>>> It = np.random.rand(2,2)
>>> Mt
array([[ 0.47961753,  0.74107574],
       [ 0.94540074,  0.05287875]])
>>> It
array([[ 0.86232671,  0.45408798],
       [ 0.99468912,  0.87005204]])

#Create a mask based on some condition
>>> mask = Mt > It
>>> mask
array([[False,  True],
       [False, False]], dtype=bool)

#Update in place
>>> Mt[mask]+=1
>>> Mt[~mask]-=1  #Numpy logical not
>>> Mt
array([[-0.52038247,  1.74107574],
       [-0.05459926, -0.94712125]])