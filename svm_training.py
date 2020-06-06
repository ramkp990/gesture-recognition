#Importing necessary libraries 
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from joblib import dump,load
from sklearn import metrics

#Reading the data
dataset=pd.read_csv("",header=None,sep=',')
dataset=dataset.as_matrix()

#Splitting the data  into target and data
data = dataset[:,:-1] #all columns except the last one
target = dataset[:,len(dataset[0])-1] #only the last column

# Split dataset into training set and test set
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.3,random_state=109)

#Model Training
model=svm.SVC(kernel='rbf')
model.fit(X_train,Y_train)
y_pred=model.predict(X_test)

#Model Evaluation
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Precision:",metrics.precision_score(y_test, y_pred))

#Model Saving


dump(model,'model.joblib')





csvr=csv.reader(open('dataset.csv','r'))
x=list(csvr)
dataset=np.array(x)





