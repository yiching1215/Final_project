import os
import pandas as pd
import numpy as np

# 自動取得專案根目錄與資料夾路徑
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_path = os.path.join(base_dir, 'data', 'raw', 'YRBS_2007.csv')         
output_dir = os.path.join(base_dir, 'data', 'processed')                  
output_path = os.path.join(output_dir, 'YRBS_2007_clean.csv')

print("[步驟 1] 開始進行『憂鬱情緒、自殺傾向與性別差異』研究數據清洗...")

if not os.path.exists(input_path):
    raise FileNotFoundError(f"❌ 找不到原始檔案：{input_path}")

# 讀取真實資料
df = pd.read_csv(input_path)

# 定義全新研究的四個真實欄位名稱
target_grade = 'InWhatGradeAreYou'
target_sex = 'WhatIsYourSex'         # 新增性別變項 (1=Male, 2=Female)
target_sad = 'SadOrHopeless'       # 自變項 X (1=Yes, 2=No)
target_suicide = 'MadeASuicidePlan' # 依變項 Y   (1=Yes, 2=No)

# 1. 篩選主要欄位並去除缺失值 (NaN)
df_clean = df[[target_grade, target_sex, target_sad, target_suicide]].dropna()

# 2. 強制轉成字串並去除前後空白
df_clean['G_str'] = df_clean[target_grade].astype(str).str.strip()
df_clean['Sex_str'] = df_clean[target_sex].astype(str).str.strip()
df_clean['Sad_str'] = df_clean[target_sad].astype(str).str.strip()
df_clean['S_str'] = df_clean[target_suicide].astype(str).str.strip()

# 3. 建立符合真實世界邏輯與問卷代碼的對照表 (Mapping)
# 年級：1=9th, 2=10th, 3=11th, 4=12th
grade_mapping = {'1': 9, '2': 10, '3': 11, '4': 12, '1.0': 9, '2.0': 10, '3.0': 11, '4.0': 12}

# 性別：根據 CDC Codebook，1=Female (女性), 2=Male (男性)
sex_mapping = {'1': 'Female', '2': 'Male', '1.0': 'Female', '2.0': 'Male'}

# 憂鬱情緒：問卷中 1=Yes (計為1分), 2=No (計為0分)
sad_mapping = {'1': 1, '2': 0, '1.0': 1, '2.0': 0}

# 自殺計畫：問卷中 1=Yes (計為1分), 2=No (計為0分)
suicide_mapping = {'1': 1, '2': 0, '1.0': 1, '2.0': 0}

df_clean['Grade'] = df_clean['G_str'].map(grade_mapping)
df_clean['Sex'] = df_clean['Sex_str'].map(sex_mapping)
df_clean['Sad_Or_Hopeless'] = df_clean['Sad_str'].map(sad_mapping)
df_clean['Suicide_Score'] = df_clean['S_str'].map(suicide_mapping)

# 只留下最終乾淨的統計欄位，並拿掉無效對應
df_final = df_clean[['Grade', 'Sex', 'Sad_Or_Hopeless', 'Suicide_Score']].dropna()

# 確保適當的資料型態
df_final['Grade'] = df_final['Grade'].astype(int)
df_final['Sad_Or_Hopeless'] = df_final['Sad_Or_Hopeless'].astype(int)
df_final['Suicide_Score'] = df_final['Suicide_Score'].astype(int)

# 4. 儲存至 data/processed/
os.makedirs(output_dir, exist_ok=True)
df_final.to_csv(output_path, index=False)

print(f"\n🎉【數據清洗成功】包含性別變項的研究檔案已儲存至：{output_path}")
print(f"📊 最終參與多維度統計的有效學生總樣本數：{len(df_final):,} 筆")
print("\n🔍 前 5 筆清洗後的數據預覽：")
print(df_final.head())