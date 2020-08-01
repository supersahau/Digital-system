import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.utils import check_array
import pickle
rng = np.random.RandomState(42)

# vectors for this Account
with open("finalVec.txt", 'rb') as savefile:    
    finalVec = pickle.load(savefile)
# train data
trainData = []
for i in range(1,120,3):
    trainData.append(finalVec[i])
trainData = np.array(trainData)
# data for test
testData = []
for i in range(0,150):
    testData.append(finalVec[i])
testData = np.array(testData)

# fit the model
clf = IsolationForest(max_samples=100, random_state=rng)
clf.fit(trainData)

# calculate score and percentage
test_mid = check_array(testData, accept_sparse='csr')
scores = clf.decision_function(test_mid)
percentage = 1 / (1 + np.exp( (-25) * (scores - clf.threshold_) ) )

print(percentage)




