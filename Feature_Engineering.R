#feature engineering 
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
train <- combi[1:891, ]
test <- combi[892:1309, ]
fit <- rpart(Survived ~ Pclass + Sex + Age + SibSp + Parch + Fare + Embarked + Title + Member + FamilyID,
             data = train, method = "class")
plot(fit)
text(fit)
test$Age[is.na(test$Age)] = median(test$Age, na.rm = TRUE)
pred = predict(fit, test, type = "class")
#make a submission
submit <- data.frame(PassengerId = test$PassengerId, Survived = pred)
write.table(submit, file = "addfeature.csv", sep = ",", row.names = FALSE)
