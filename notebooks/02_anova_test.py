import os
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_path = os.path.join(base_dir, 'data', 'processed', 'YRBS_2007_clean.csv') 
output_dir = os.path.join(base_dir, 'data', 'processed')

print("[步驟 2] 執行雙因子 ANOVA 核心統計檢定...")

if not os.path.exists(input_path):
    raise FileNotFoundError(f"❌ 找不到清洗後的檔案：{input_path}。請先運行 01 檔案！")

df_clean = pd.read_csv(input_path)

# ==============================================================================
# 📊 1. 輸出終端機數據現況描述
# ==============================================================================
print("\n" + "="*50)
print("       【性別現況】男女性別之心理健康指標對比")
print("="*50)
sex_sad = df_clean.groupby('Sex')['Sad_Or_Hopeless'].mean() * 100
sex_suicide = df_clean.groupby('Sex')['Suicide_Score'].mean() * 100

for gender in ['Female', 'Male']:
    print(f"👉 {gender} 學生:")
    print(f"   - 過去一年內感到悲傷/絕望比例: {sex_sad[gender]:.2f}%")
    print(f"   - 具有自殺計畫之盛行率: {sex_suicide[gender]:.2f}%")
print("="*50)

# ==============================================================================
# ⚖️ 2. 執行雙因子 ANOVA 模型
# ==============================================================================
model_sex = ols('Suicide_Score ~ C(Sex) * C(Sad_Or_Hopeless)', data=df_clean).fit()
anova_sex_table = sm.stats.anova_lm(model_sex, typ=2)

print("\n--- 雙因子 ANOVA 檢定摘要表 (性別 × 憂鬱情緒) ---")
print(anova_sex_table)
print("="*70)

try:
    p_interaction = anova_sex_table.iloc[-2, -1]
    print(f"\n[進階統計解讀]")
    print(f"👉 核心交互作用 (Sex × Sad_Or_Hopeless) 的 P 值為: {p_interaction:.6f}")
    if p_interaction < 0.05:
        print("結論：交互作用達顯著水準 (P < 0.05)！有顯著性別差異。")
    else:
        print("結論：交互作用未達顯著水準 (P >= 0.05)。")
except Exception as e:
    pass

# ==============================================================================
# 💾 3. 匯出統計摘要表（已修正路徑：移至 outputs/table/）
# ==============================================================================
# 重新定義輸出路徑到 outputs/table
output_table_dir = os.path.join(base_dir, 'outputs', 'table')
os.makedirs(output_table_dir, exist_ok=True) # 如果 outputs/table 資料夾不存在，自動建立

summary_df = df_clean.groupby(['Grade', 'Sex', 'Sad_Or_Hopeless'])['Suicide_Score'].agg(['count', 'mean']).reset_index()
output_table_path = os.path.join(output_table_dir, 'summary_table.csv')
summary_df.to_csv(output_table_path, index=False)

print(f"\n🎉【統計完成】ANOVA 模型計算完畢，摘要數據已成功移動並儲存至：\n👉 {output_table_path}")