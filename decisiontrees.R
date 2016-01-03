setwd("/Users/XW/Desktop/Titanic")
library(rpart)
train <- read.csv("train.csv", header = TRUE)
test <- read.csv("test.csv", header = TRUE)
test$Age[is.na(test$Age)] = median(test$Age, na.rm = TRUE)
fit <- rpart(Survived ~ Pclass + Sex + Age + SibSp + Parch + Fare + Embarked, data = train, method = "class")
plot(fit)
text(fit, cex = 0.8)
pred = predict(fit, test, type = "class")
#make a submission
submit <- data.frame(PassengerId = test$PassengerId, Survived = pred)
write.table(submit, file = "decisiontree.csv", sep = ",", row.names = FALSE)
#0.78469
