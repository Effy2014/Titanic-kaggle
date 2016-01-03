setwd("/Users/XW/Desktop/Titanic")
train <- read.csv("train.csv", header = TRUE)
test <- read.csv("test.csv", header = TRUE)
str(train)
table(train$Survived)
prop.table(table(train$Survived))
#adding Survived column to test dataset
test$Survived = 0
#Gender-Class model 
summary(train$Sex)
prop.table(table(train$Sex, train$Survived), 1)
summary(train$Age)
train$Child <- 0
train$Child[train$Age <  18] <- 1
aggregate(Survived ~ Child + Sex, data = train, FUN = sum)
aggregate(Survived ~ Child + Sex, data = train, FUN =  length)
aggregate(Survived ~ Child + Sex, data = train, FUN = function(x) {sum(x)/length(x)})
#the result show that female is more likely to be survived than male
#fare is another factor to take into consideration
train$Fare2 <- '30+'
train$Fare2[train$Fare < 30 & train$Fare >= 20] <- '20-30'
train$Fare2[train$Fare <20 & train$Fare >= 10] <- '10-20'
train$Fare2[train$Fare < 10] <- '<10'
aggregate(Survived ~ Sex + Fare2 + Pclass, data = train, FUN = function(x) {sum(x)/length(x)})
#19 female   30+      3 0.1250000
#20   male   30+      3 0.2400000
test$Survived <- 0
test$Survived[test$Sex == 'female'] <- 1
test$Survived[test$Sex == 'female' & test$Pclass == '3' & test$Fare >= 20] <- 0

#make a submission
submit <- data.frame(PassengerId = test$PassengerId, Survived = test$Survived)
write.table(submit, file = "basic.csv", sep = ",", row.names = FALSE)
