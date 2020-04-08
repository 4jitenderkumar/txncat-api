from flask import Flask, jsonify, request, render_template  
import os
# import joblib
# from sklearn import linear_model
# model = linear_model.LinearRegression()
from sklearn.datasets import load_iris 
iris = load_iris() 
  
X = iris.data 
y = iris.target 
X_train, X_test, y_train, y_test = \ 
    train_test_split(X, y, test_size = 0.3,
     random_state = 2018) 

# from sklearn.externals import joblib 

from sklearn.neighbors import KNeighborsClassifier as KNN 
knn = KNN(n_neighbors = 3) 
  
# train model 
knn.fit(X_train, y_train) 

# joblib.dump(knn, 'cc_pred_cat_L2.joblib') 

model = joblib.load(r'C:\Users\jitenderkumar\Documents\Python WebServices\Transactions Project\cc_pred_cat_L2.joblib')  

print(model)
output = model.predict(X_test)

# LinearRegression(copy_X = True, fit_intercept = True, njobs = 1, normalize = False)

# model.fit()
# app = Flask(__name__)              

# # app.run(port=5000)
# filename = os.path.join("C:/Users/jitenderkumar/Documents/Python WebServices/Transactions Project", 'cc_pred_cat_L2.joblib') 
# model = joblib.load(filename) 
# # C:\Users\jitenderkumar\Documents\Python WebServices\Transactions Project
# print(model)