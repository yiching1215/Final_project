# 2026-Spring-Stat2-Cycle-4

## 👥 Student Information
* **Name:** (請填寫你的姓名)
* **Student ID:** (請填寫你的學號)

## 🔗 Project Repository
* [https://github.com/yiching1215/Final_project](https://github.com/yiching1215/Final_project)

## 🎥 Presentation Video
* [請在此處貼上你的 YouTube 影片連結]

---

## ❓ Selected Research Question (Adolescent Crisis Framework)

### 📌 Core Question (Primary Objective)
**Does the manifestation of a clinical depressive mood (persistent feelings of sadness or hopelessness) significantly alter the probability of a student formulating an active suicide plan?**

* **Context:** We initially aimed to evaluate whether adolescent suicidal behaviors vary fundamentally based on current mental health markers, or if the observed sample differences are simply random variations.

### 🚀 Cycle 4 Expansion (Advanced Multi-Variable Inquiry)
While addressing the macro-level psychological effect, we discovered that looking at depression in isolation obscures demographic variations. To break this analytical bottleneck, we intentionally expanded our analytical framework by introducing two core demographic covariates: `Sex` and `Grade`. This allows us to investigate a more profound, stratified question:
* Does biological sex act as a moderator on this relationship, and how does the risk profile evolve chronologically across high school grade cohorts?

---

## 📊 Core Analytical Variable Definitions

* **Primary Independent Variable ($X_1$):** `Sad_Or_Hopeless` (Binary 0/1)
  * `0` = No Sad/Hopeless Feelings ($n = 9,619$, 70.2%)
  * `1` = Experienced Sad/Hopeless Feelings ($n = 4,077$, 29.8%)
* **Secondary Independent Variable / Moderator ($X_2$):** `Sex` (Categorical String)
  * `Male` ($n = 6,213$) vs `Female` ($n = 6,402$)
* **Dependent Variable ($Y$):** `Suicide_Score` (Binary 0/1)
  * `0` = No Suicide Plan Formulated | `1` = Formulated an Active Suicide Plan
* **Covariate / Control Variable:** `Grade` (9th, 10th, 11th, and 12th Grade)

---

## 🔬 Two-Way ANOVA Test Results & Metrics

| Source of Variation | Sum of Squares (`sum_sq`) | df | F-Statistic | PR(>F) | Significance |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Depressive Mood (`Sad_Or_Hopeless`)** | 148.2288 | 1.0 | 1591.4703 | 0.000000 | *** Extremely Significant ($P < 0.001$) |
| **Biological Sex (`Sex`)** | 0.5278 | 1.0 | 5.6668 | 0.017303 | * Statistically Significant ($P < 0.05$) |
| **Interaction Effect (`Sex` × `Sad_Or_Hopeless`)** | 0.0481 | 1.0 | 0.5160 | 0.472573 | NS [Not Significant] |

---

## 🎯 Final Academic Conclusions

### 🚨 Core Finding: Catastrophic Main Effect of Depressive Mood ($X_1 \rightarrow Y$)
The Two-Way ANOVA model demonstrates an overwhelmingly significant main effect for `Sad_Or_Hopeless` ($F = 1591.47, P < 0.001$). Depressive mood is the single most dominant predictor of adolescent suicide planning. Free of depression, the baseline suicide plan rate is minimal (~3%). Upon onset of persistent sadness, the rate violently explodes to over 30%, multiplying psychological crisis risks by more than **8.2 times**.

### 🧠 Extension Finding: The Gender 'Universal Injury' Principle ($X_2 \times X_1 \rightarrow Y$)
While female students exhibit a significantly higher baseline prevalence of entering depressive states (37.03%) than males (22.56%), the Interaction Term is strictly **not significant** ($P = 0.473$). 

**Academic Interpretation:** The psychological mechanism converting depression into suicide planning operates with identical, lethal velocity across BOTH genders. A depressive mood inflicts a "universal injury"