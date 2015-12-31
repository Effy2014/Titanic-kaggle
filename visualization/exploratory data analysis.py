
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


# In[212]:

male = train_df.Survived[train_df.Sex == 'male'].value_counts().sort_index()
female = train_df.Survived[train_df.Sex == 'female'].value_counts().sort_index()
ind = np.arange(2)
bar_width = 0.5
y_pos = [i + (bar_width/2) for i in ind]
plt.barh(ind, male.values, bar_width, label = 'Male', alpha = 0.55, color = 'y')
plt.barh(ind, female.values, bar_width, label = 'Female', left=male.values, alpha = 0.55, color = 'r')
plt.yticks(y_pos, male.index)
plt.ylim(min(y_pos)-bar_width, max(y_pos)+bar_width)
plt.grid(b = True, which = 'major')
plt.title("Survival by gender")
plt.legend(loc= 'best')
plt.savefig('Survival by gender')


# In[213]:

male_per = male/float(male.sum())
female_per = female/float(female.sum())
ind = np.arange(2)
bar_width = 0.5
y_pos = [i + (bar_width/2) for i in ind]
plt.barh(ind, male_per.values, bar_width, label = 'Male', alpha = 0.55, color = 'y')
plt.barh(ind, female_per.values, bar_width, label = 'Female', left=male_per.values, alpha = 0.55, color = 'r')
plt.yticks(y_pos, male_per.index)
plt.xlim(0,1.5)
plt.ylim(min(y_pos)-bar_width, max(y_pos)+bar_width)
plt.grid(b = True, which = 'major')
plt.title("Survival by gender")
plt.legend(loc= 'upper right')
plt.savefig('Survival by gender (percent)')


