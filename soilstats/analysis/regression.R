regression <- function(df, formula) {
    model <- lm(formula = formula, data = df)
    print(summary(model))
    rsquared <- summary(model)$r.squared
    intercept <- coef(model)[1]
    slope <- coef(model)[2]
    return(list(rsquared = rsquared, intercept = intercept, slope = slope))
}