library(stats)

model <- lm(clay + sand + silt ~ ocs, data = dp)

summary(model)