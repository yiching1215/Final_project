# Reference Part 2: Methodology and Statistical Assumptions

This document justifies the selection of the statistical methods used in this project and verifies that the necessary mathematical assumptions are satisfied for a valid inference based on the processed dataset ($N = 12,615$).

---

## 1. Method Choice

### Primary Statistical Method: Two-Way Analysis of Variance (Two-Way ANOVA) & Interaction Modeling
To analyze the relationships among biological sex, depressive mood, and adolescent suicide planning, we transition from simple single-variable testing to a robust **Two-Way ANOVA**. This framework allows us to evaluate not only the standalone main effects of our independent factors but also their combined interactive property.

* **Group Variable 1 (Independent Factor $X_1$):** `Sad_Or_Hopeless` (Categorical, 2 levels: 0 = No Sad Feelings, 1 = Experienced Depressive Mood).
* **Group Variable 2 (Independent Factor $X_2$):** `Sex` (Categorical, 2 levels: Male / Female).
* **Response Variable (Dependent $Y$):** `Suicide_Score` (Continuous proxy via cell-mean proportions, 2 levels: 0 = No Plan, 1 = Active Plan).

### Justification:
1. **Simultaneous Evaluation:** Traditional t-tests or Chi-Square tests force the isolation of variables, blinding the model to demographic overlaps. Two-Way ANOVA reveals whether the variance in suicide planning is driven primarily by mood, sex, or a combination of both.
2. **Interaction Detection:** This is the only standard linear framework capable of testing our secondary hypothesis—verifying if biological sex moderates the impact of depression (i.e., whether depression hurts one gender significantly more than the other).

---

## 2. Verification of Statistical Assumptions

To ensure the statistical validity of the F-test results, three fundamental assumptions were evaluated:

1. **Independence of Observations:** Verified by the YRBS 2007 multi-stage cluster sampling methodology. Each data point originates from a separate, independent student questionnaire, minimizing serial correlation.
2. **Normality:** For a sample size of this magnitude ($N > 12,000$), the Central Limit Theorem (CLT) guarantees that the distribution of the sample means approaches normality, rendering the F-statistic highly robust against local non-normality.
3. **Homoscedasticity (Homogeneity of Variance):** Group variances across the four analytical sub-cells (`Male_Sad`, `Male_Healthy`, `Female_Sad`, `Female_Healthy`) were monitored. The stable distribution of error terms confirms that the variance within each factor combination remains balanced, preserving the integrity of the F-test computations.
