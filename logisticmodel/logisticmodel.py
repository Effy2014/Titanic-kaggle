
# coding: utf-8

# In[102]:

import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.nonparametric.kde import KDEUnivariate
from statsmodels.nonparametric import smoothers_lowess
from pandas import Series, DataFrame
from patsy import dmatrices
from sklearn import datasets, svm


# In[103]:

train_df = pd.read_csv('train.csv', header=0) 
#shape (891, 12)


# In[104]:

# female = 0, Male = 1
train_df['Gender'] = train_df['Sex'].map( {'female': 0, 'male': 1} ).astype(int)


# In[107]:

#get general info
train_df.dtypes


# In[110]:

#train_df


# In[113]:

#delete Ticket and Cabin
train_df = train_df.drop(['Ticket', 'Cabin'], axis = 1)


# In[235]:

formula = 'Survived ~ C(Pclass) + C(Sex) + Age + SibSp + C(Embarked)'
y, x = dmatrices(formula, data = train_df, return_type = 'dataframe')
model = sm.Logit(y,x)
res = model.fit()
result = {}
result['Logit'] = [res, formula]
res.summary()


# In[381]:

ypred = res.predict(x)


# In[399]:

#predictions vs actual
plt.figure(figsize=(18,4));
plt.subplot(121, axisbg = "#DBDBDB")
plt.plot(x.index, ypred, 'bo', x.index, y, 'mo', alpha = 0.25)
plt.grid(color = "white", linestyle = "dashed")
plt.title("Logist predictions in Training dataset")

#residual
ax2 = plt.subplot(122, axisbg = "#DBDBDB")
plt.plot(res.resid_dev, 'r-')
plt.grid(color = "white", linestyle = "dashed")
ax2.set_xlim(-1, len(res.resid_dev))
plt.title("Residuals")

plt.savefig("Logistic Results Analysis")


# In[ ]:




# In[369]:

test_df = pd.read_csv('test.csv', header=0)
ids = test_df[["PassengerId"]]


# In[370]:

test_df['Survived'] = 1.23


# In[371]:

#add missing values in age 
 
test_df.loc[test_df['Age'].isnull()] = 27


# In[372]:

formula = 'Survived ~ C(Pclass) + C(Sex) + Age + SibSp + C(Embarked)'
Y, X = dmatrices(formula, data = test_df, return_type = 'dataframe')


# In[373]:

test = X.drop(X.columns[[3, 4, 7]], axis=1)


# In[374]:

Y = res.predict(test)


# In[375]:

pre = [0 if i <= 0.5 else 1 for i in Y]


# In[376]:

ids["Survived"] = pre


# In[379]:

ids.to_csv("predict.csv",index=False)
#using the logistic model, filling the missing value with median age the score is 0.77512