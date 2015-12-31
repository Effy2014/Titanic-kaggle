
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


# In[129]:

#survived 
train_df.Survived.value_counts().plot(kind = 'barh', alpha = 0.5)
plt.title("Survival Situation, (1 = Survived)")
plt.grid(b=True, which = 'major', axis ='x')
plt.savefig('Survival_Situation.png')


# In[127]:

plt.scatter(train_df.Survived, train_df.Age, alpha = 0.2)
plt.ylabel("Age")
plt.grid(b=True, which = 'major', axis ='y')
plt.title("Survival by Age")
plt.savefig('Survival by Age')


# In[144]:

train_df.Fare[train_df.Pclass == 3].plot(kind = 'kde')
train_df.Fare[train_df.Pclass == 2].plot(kind = 'kde')
train_df.Fare[train_df.Pclass == 1].plot(kind = 'kde')
plt.xlim(-10,600)
plt.grid(b=True,which='major')
plt.xlabel('Fare')
plt.title('Fare distribution within classes')
plt.legend(('Lower', 'Middle', 'Upper'), loc = 'best')
plt.savefig("Fare distribution within classes")


# In[145]:

#embark places
train_df.Embarked.value_counts().plot(kind = 'barh', alpha = 0.55)
plt.grid(b=True, which = 'major')
plt.title("Boarding Location")
plt.savefig("Boarding Location")

