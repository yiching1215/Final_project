import os
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import seaborn as sns

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_path = os.path.join(base_dir, 'data', 'processed', 'YRBS_2007_clean.csv') 
figure_dir = os.path.join(base_dir, 'outputs', 'figures')                                  

print("[步驟 2] 開始讀取清洗後的數據並執行多維度統計分析（含性別差異）...")

if not os.path.exists(input_path):
    raise FileNotFoundError(f"❌ 找不到清洗後的檔案：{input_path}。請先運行 01 檔案！")

df_clean = pd.read_csv(input_path)

# ==============================================================================
# 📊 【性別現況】現場印出男女學生的憂鬱與自殺計畫率對比
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
# 2. 執行雙因子 ANOVA：檢定 性別 與 憂鬱情緒 對 自殺計畫 的交互作用
# ==============================================================================
# 這裡強制將變數用 C() 包起來，確保統計模型正確處理類別變數
model_sex = ols('Suicide_Score ~ C(Sex) * C(Sad_Or_Hopeless)', data=df_clean).fit()
anova_sex_table = sm.stats.anova_lm(model_sex, typ=2)

print("\n" + "="*70)
print("               雙因子 ANOVA 檢定摘要表 (性別 × 憂鬱情緒)")
print("="*70)
print(anova_sex_table)
print("="*70)

# 🌟【終極智慧解讀機制】動態尋找 P 值的欄位名稱，徹底解決 KeyError 'PR(>F)' 錯誤
p_col = None
for col in ['PR(>F)', 'P-value', 'P', 'p']:
    if col in anova_sex_table.columns:
        p_col = col
        break

# 尋找代表交互作用的那一列 (Row) 名稱
row_name = 'C(Sex):C(Sad_Or_Hopeless)'

if p_col and row_name in anova_sex_table.index:
    p_interaction = anova_sex_table.loc[row_name, p_col]
    print(f"\n[進階統計解讀]")
    print(f"👉 核心交互作用 (Sex × Sad_Or_Hopeless) 的 P 值為: {p_interaction:.6f}")
    if p_interaction < 0.05:
        print("結論：交互作用達顯著水準 (P < 0.05)！")
        print("👉 這代表『憂鬱情緒對自殺風險的打擊，在男女高中生之間「有顯著的性別區別」』！")
    else:
        print("結論：交互作用未達顯著水準 (P >= 0.05)。")
        print("👉 這代表不論男生女生，憂鬱情緒造成的自殺計畫風險衝擊是高度相似且同樣巨大的。")
else:
    print("\n⚠️ 統計表結構有變，請直接閱讀上方表格中的 F 檢定與相關顯著性。")


# ==============================================================================
# 3. 繪製並儲存【圖表 1 ~ 5】
# ==============================================================================
print("\n[步驟 3] 正在繪製並儲存 5 張高畫質學術圖表...")
os.makedirs(figure_dir, exist_ok=True)
sns.set_theme(style="whitegrid")

df_clean['Sad_Label'] = df_clean['Sad_Or_Hopeless'].map({0: 'No Sad/Hopeless\nFeelings', 1: 'Experienced\nSad/Hopeless Feelings'})

# 圖表 1：人數分佈
plt.figure(figsize=(7, 4))
ax1 = sns.countplot(x='Sad_Label', data=df_clean, palette=['#2b7bba', '#d64b4b'], order=['No Sad/Hopeless\nFeelings', 'Experienced\nSad/Hopeless Feelings'])
total_samples = len(df_clean)
for p in ax1.patches:
    height = p.get_height()
    ax1.annotate(f'{int(height):,}\n({(height/total_samples)*100:.1f}%)', (p.get_x() + p.get_width() / 2., height), ha='center', va='bottom', fontsize=9, fontweight='bold', xytext=(0, 5), textcoords='offset points')
plt.title('Distribution of Depressive Mood Among Students', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(figure_dir, '01_depressive_mood_distribution.png'), dpi=300)

# 圖表 2：自殺率對比
plt.figure(figsize=(7, 4))
sns.barplot(x='Sad_Label', y='Suicide_Score', data=df_clean, palette=['#2b7bba', '#d64b4b'], order=['No Sad/Hopeless\nFeelings', 'Experienced\nSad/Hopeless Feelings'], capsize=0.1, errorbar='ci')
plt.gca().set_yticklabels(['{:,.0f}%'.format(x*100) for x in plt.gca().get_yticks()])
plt.title('Suicide Plan Rates by Mental Health Status', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(figure_dir, '02_suicide_rate_by_depression.png'), dpi=300)

# 圖表 3：年級交互作用
plt.figure(figsize=(8, 4))
sns.pointplot(x='Grade', y='Suicide_Score', hue='Sad_Or_Hopeless', data=df_clean, dodge=0.1, capsize=0.05, markers=["o", "s"], linestyles=["-", "--"], palette={0: "#2b7bba", 1: "#d64b4b"})
plt.gca().set_yticklabels(['{:,.0f}%'.format(x*100) for x in plt.gca().get_yticks()])
plt.xticks(ticks=[0, 1, 2, 3], labels=['9th Grade', '10th Grade', '11th Grade', '12th Grade'])
plt.title('Impact of Depressive Mood on Suicide Plans Across Different Grades', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(figure_dir, '03_depression_grade_interaction.png'), dpi=300)

# 圖表 4：性別與憂鬱比率
plt.figure(figsize=(7, 4))
ax4 = sns.barplot(x='Sex', y='Sad_Or_Hopeless', data=df_clean, palette=['#e066a3', '#3594cc'], capsize=0.1, errorbar='ci')
plt.gca().set_yticklabels(['{:,.0f}%'.format(x*100) for x in plt.gca().get_yticks()])
plt.title('Prevalence of Depressive Mood (Sad/Hopeless) by Biological Sex', fontsize=11, fontweight='bold')
plt.xlabel('Biological Sex', fontsize=10, fontweight='bold')
plt.ylabel('Percentage Experiencing Depressive Mood (%)', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(figure_dir, '04_depression_by_sex.png'), dpi=300)

# 圖表 5：性別差異交互作用
plt.figure(figsize=(8, 4))
ax5 = sns.pointplot(
    x='Sad_Label', 
    y='Suicide_Score', 
    hue='Sex', 
    data=df_clean,
    dodge=0.1, 
    capsize=0.05, 
    markers=["o", "s"], 
    linestyles=["-", "--"],
    palette={'Female': '#e066a3', 'Male': '#3594cc'}, 
    order=['No Sad/Hopeless\nFeelings', 'Experienced\nSad/Hopeless Feelings']
)
plt.gca().set_yticklabels(['{:,.0f}%'.format(x*100) for x in plt.gca().get_yticks()])
plt.title('Gender Differences in How Depressive Mood Dictates Suicide Plans', fontsize=11, fontweight='bold')
plt.xlabel('Mental Health Status', fontsize=10, fontweight='bold')
plt.ylabel('Suicide Plan Prevalence Rate (%)', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(figure_dir, '05_depression_sex_interaction.png'), dpi=300)

print("\n🎉 排除所有錯誤！5 張精美分析圖表已完美輸出至 outputs/figures/ ！")
plt.show()