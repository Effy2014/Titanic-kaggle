install.packages('randomForest')
install.packages("party")
library(party)
library(randomForest)
library(rpart)
setwd("/Users/XW/Desktop/Titanic")
train <- read.csv("train.csv", header = TRUE)
test <- read.csv("test.csv", header = TRUE)
test$Survived <- NA
combi = rbind(train, test)
combi$Name <- as.character(combi$Name)
Title <- sapply(combi$Name, FUN = function(x) {strsplit(x, split = '[,.]')[[1]][2]})
combi$Title <- sub(' ', '', Title)
table(combi$Title)
combi$Title[combi$Title %in% c('Mme', 'Mlle')] <- 'Mlle'
combi$Title[combi$Title %in% c('Capt', 'Don', 'Major', 'Sir')] <- 'Sir'
combi$Title[combi$Title %in% c('Dona', 'Lady', 'the Countess', 'Jonkheer')] <- 'Lady'
combi$Title <- as.factor(combi$Title)
combi$Member <- combi$SibSp + combi$Parch + 1
combi$Surname <- sapply(combi$Name, FUN = function(x) {strsplit(x, split = '[.,]')[[1]][1]})
combi$FamilyID <- paste(as.character(combi$Member), combi$Surname, sep="")
combi$FamilyID[combi$Member <= 2] <- 'small'
table(combi$FamilyID)
famIDs <- data.frame(table(combi$FamilyID))
famIDs <- famIDs[famIDs$Freq <= 2, ]
combi$FamilyID[combi$FamilyID %in% famIDs$Var1] <- 'small'
combi$FamilyID <- as.factor(combi$FamilyID)
#using decision trees replacing missing values
Agefit <- rpart(Age ~ Pclass + Sex + SibSp + Fare + Embarked + Title + Member,
                 data = combi[!is.na(combi$Age), ], method = "anova")
combi$Age[is.na(combi$Age)] <- predict(Agefit, combi[is.na(combi$Age), ])
#Embarked
summary(combi$Embarked)
#finding where the missing value is
which(combi$Embarked == '')
#filling in the missing values with S, since majority embarked at S
combi$Embarked[c(62,830)] = "S"
#Fare also has missing value
summary(combi$Fare)
which(is.na(combi$Fare))
combi$Fare[1044] = median(combi[combi$Pclass == 3, ]$Fare, na.rm = TRUE)
train <- combi[1:891, ]
test <- combi[892:1309, ]
##############################################
#fit <- rpart(Survived ~ Pclass + Sex + Age + SibSp + Fare + Embarked + Title + Member + FamilyID,
#             data = train, method = "class")
#plot(fit)
#text(fit)
#pred = predict(fit, test, type = "class")
#make a submission
#submit <- data.frame(PassengerId = test$PassengerId, Survived = pred)
#write.table(submit, file = "newtree.csv", sep = ",", row.names = FALSE)
##############################################
fit <- cforest(as.factor(Survived) ~ Pclass + Sex + Age + SibSp + Parch + Fare + Embarked + Title + Member + FamilyID,
                    data = train, controls = cforest_unbiased(ntree = 2000, mtry = 3))
prediction <- predict(fit, test, OOB = TRUE, type = "response")
#make a submission
submit <- data.frame(PassengerId = test$PassengerId, Survived = prediction)
write.table(submit, file = "cforest.csv", sep = ",", row.names = FALSE)

