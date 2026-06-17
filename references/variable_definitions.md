# Reference Part 1: Variable and Group Definitions

This document outlines the data processing logic and definitions used for the Project Cycle 4 analysis. It ensures transparency and reproducibility by documenting how raw data from the CDC's Youth Risk Behavior Surveillance System (YRBS 2007) was transformed into analytical variables.

---

## 1. Variable Coding Reference

The source of the data is the YRBS 2007 Codebook. The raw categorical and text responses were systematically recoded into appropriate formats (binary and discrete numeric) to facilitate two-way analysis of variance and stratified trend evaluation.

### 🧠 Core Mental Health Variable: Sad_Or_Hopeless
We transformed the psychological frequency-based code into a binary "Success/Failure" (1/0) format representing the presence of acute depressive symptoms.
* **Recoding Logic:**
  * **Exposed (1):** Code 1. This represents students who responded "Yes" to whether they felt so sad or hopeless almost every day for two weeks or more in a row that they stopped doing some usual activities during the past 12 months.
  * **Unexposed (0):** Code 2. This represents students who responded "No" to the persistent sad or hopeless feelings criteria.
* **Justification:** This transformation allows us to isolate clinical-level depressive affect as a discrete risk threshold rather than a subjective spectrum, establishing a clear independent clinical factor ($X_1$).

### 🧬 Demographics Variable: Sex (Biological Sex)
To operationalize biological sex as the secondary independent variable ($X_2$) and potential moderator, raw demographic categories were mapped directly.
* **Recoding Logic:**
  * **Female:** Code 1. Mapped as the female cohort for stratified comparison.
  * **Male:** Code 2. Mapped as the male cohort for stratified comparison.
* **Justification:** Essential for verifying whether macro-level societal and biological gender differences modulate the effect of depressive states on critical psychological outcomes.

### 🎯 Primary Outcome Variable: Suicide_Score
The response variable ($Y$) capturing acute adolescent suicidal behavioral planning within the past 12 months.
* **Recoding Logic:**
  * **Formulated Plan (1):** Code 1. Students who actively selected "Yes" when asked if they had made a specific plan about how they would attempt suicide.
  * **No Plan (0):** Code 2. Students who selected "No" regarding active planning.
* **Justification:** Acts as a critical behavioral dependent variable to measure the exact point of escalation from psychological pain into structured ideation.

### 🏫 Stratification Variable: Grade (High School Cohort)
* **Recoding Logic:** Raw categorical codes 1, 2, 3, and 4 mapped directly to 9th, 10th, 11th, and 12th grades respectively to observe developmental trajectories across high school groups.
