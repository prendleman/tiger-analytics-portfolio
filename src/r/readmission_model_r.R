# Simple 30-day readmission model in R (logistic regression).
# Run from repo root: Rscript src/r/readmission_model_r.R
# Demonstrates R for modeling (mirrors Python readmission_model.py).

data_dir <- file.path("data", "raw")
if (!dir.exists(data_dir)) data_dir <- file.path("..", "..", "data", "raw")

patients    <- read.csv(file.path(data_dir, "patients.csv"))
encounters  <- read.csv(file.path(data_dir, "encounters.csv"))
diagnoses   <- read.csv(file.path(data_dir, "diagnoses.csv"))
readmissions <- read.csv(file.path(data_dir, "readmissions.csv"))

encounters$admit_date     <- as.POSIXct(encounters$admit_date)
encounters$discharge_date <- as.POSIXct(encounters$discharge_date)
patients$date_of_birth    <- as.Date(patients$date_of_birth)

# Target
enc_with_readmit <- readmissions$encounter_id[readmissions$is_30_day == 1]
encounters$readmit_30 <- as.integer(encounters$encounter_id %in% enc_with_readmit)

# Features: LOS, age, diagnosis count
encounters$los_days <- as.numeric(difftime(encounters$discharge_date, encounters$admit_date, units = "days"))
encounters$los_days <- pmax(0, encounters$los_days)
encounters <- merge(encounters, patients[, c("patient_id", "date_of_birth")], by = "patient_id")
encounters$age <- as.numeric(difftime(as.Date(encounters$admit_date), encounters$date_of_birth, units = "days")) / 365.25
encounters$age <- pmin(pmax(encounters$age, 0), 120)

diag_count <- aggregate(diagnosis_id ~ encounter_id, data = diagnoses, length)
names(diag_count)[2] <- "diag_count"
encounters <- merge(encounters, diag_count, by = "encounter_id", all.x = TRUE)
encounters$diag_count[is.na(encounters$diag_count)] <- 0

# Train/test split (75/25)
set.seed(42)
n <- nrow(encounters)
idx <- sample(n, floor(0.75 * n))
train <- encounters[idx, ]
test  <- encounters[-idx, ]

model <- glm(readmit_30 ~ los_days + age + diag_count, data = train, family = binomial)
test$pred_prob <- predict(model, newdata = test, type = "response")
test$pred_class <- as.integer(test$pred_prob >= 0.5)

cat("=== R logistic regression: 30-day readmission ===\n")
print(summary(model))
cat("\nTest confusion matrix (predicted vs actual):\n")
print(table(predicted = test$pred_class, actual = test$readmit_30))

if (requireNamespace("pROC", quietly = TRUE)) {
  cat("\nTest AUC:", round(pROC::auc(test$readmit_30, test$pred_prob), 4), "\n")
} else {
  cat("\nInstall 'pROC' for AUC: install.packages('pROC')\n")
}
