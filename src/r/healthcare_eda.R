# Healthcare Mock Data - EDA and Summary (R)
# Run from repo root: Rscript src/r/healthcare_eda.R

data_dir <- file.path("data", "raw")
if (!dir.exists(data_dir)) data_dir <- file.path("..", "..", "data", "raw")

patients   <- read.csv(file.path(data_dir, "patients.csv"))
encounters <- read.csv(file.path(data_dir, "encounters.csv"))
encounters$admit_date     <- as.POSIXct(encounters$admit_date)
encounters$discharge_date <- as.POSIXct(encounters$discharge_date)
claims     <- read.csv(file.path(data_dir, "claims.csv"))
readmissions <- read.csv(file.path(data_dir, "readmissions.csv"))

cat("=== Encounter type counts ===\n")
print(table(encounters$encounter_type))

encounters$los_days <- as.numeric(difftime(encounters$discharge_date, encounters$admit_date, units = "days"))
inpatient <- encounters[encounters$encounter_type == "inpatient", ]
cat("\n=== Inpatient LOS (days) summary ===\n")
print(summary(inpatient$los_days))

cat("\n=== Claims: total_paid by claim_type (mean) ===\n")
print(aggregate(total_paid ~ claim_type, data = claims, FUN = mean))

cat("\n=== 30-day readmissions ===\n")
n_30 <- sum(readmissions$is_30_day == 1)
cat("Count:", n_30, "of", nrow(readmissions), "index discharges; rate", round(100 * n_30 / nrow(readmissions), 2), "%\n")
