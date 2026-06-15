import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
input_path = os.path.join(base_dir, 'data', 'processed', 'YRBS_2007_clean.csv') 
figure_dir = os.path.join(base_dir, 'outputs', 'figures')                                  

print("[步驟 3] 開始獨立執行高畫質學術圖表生成流程...")

if not os.path.exists(input_path):
    raise FileNotFoundError(f"❌ 找不到清洗後的檔案：{input_path}。請依序運行 01 與 02！")

df_clean = pd.read_csv(input_path)

# 設定統一的學術風格底色
os.makedirs(figure_dir, exist_ok=True)
sns.set_theme(style="whitegrid")

# 建立中文字體或標籤對照
df_clean['Sad_Label'] = df_clean['Sad_Or_Hopeless'].map({0: 'No Sad/Hopeless\nFeelings', 1: 'Experienced\nSad/Hopeless Feelings'})

# ==============================================================================
# 🎨 圖表 1：人數分佈長條圖（已修正文字重疊問題）
# ==============================================================================
plt.figure(figsize=(7, 4))
ax1 = sns.countplot(x='Sad_Label', data=df_clean, palette=['#2b7bba', '#d64b4b'], order=['No Sad/Hopeless\nFeelings', 'Experienced\nSad/Hopeless Feelings'])

# 🌟 修正點 1：手動拉高 Y 軸的上限，留出 15% 的頂部空間給數字，防止跟標題重疊
current_ylim = ax1.get_ylim()
ax1.set_ylim(current_ylim[0], current_ylim[1] * 1.15)

total_samples = len(df_clean)
for p in ax1.patches:
    height = p.get_height()
    # 🌟 修正點 2：調整 xytext 的垂直偏移量 (從 5 改為 3)，讓文字更貼近長條頂端
    ax1.annotate(f'{int(height):,}\n({(height/total_samples)*100:.1f}%)', 
                 (p.get_x() + p.get_width() / 2., height), 
                 ha='center', va='bottom', fontsize=9, fontweight='bold', 
                 xytext=(0, 3), textcoords='offset points')

# 🌟 修正點 3：增加 pad 參數，把標題往上推一點點
plt.title('Distribution of Depressive Mood Among Students', fontsize=11, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(figure_dir, '01_depressive_mood_distribution.png'), dpi=300)
plt.close()

# ==============================================================================
# 🎨 圖表 2：自殺率對比長條圖
# ==============================================================================
plt.figure(figsize=(7, 4))
sns.barplot(x='Sad_Label', y='Suicide_Score', data=df_clean, palette=['#2b7bba', '#d64b4b'], order=['No Sad/Hopeless\nFeelings', 'Experienced\nSad/Hopeless Feelings'], capsize=0.1, errorbar='ci')
plt.gca().set_yticklabels(['{:,.0f}%'.format(x*100) for x in plt.gca().get_yticks()])
plt.title('Suicide Plan Rates by Mental Health Status', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(figure_dir, '02_suicide_rate_by_depression.png'), dpi=300)
plt.close()

# ==============================================================================
# 🎨 圖表 3：年級交互作用折線圖
# ==============================================================================
plt.figure(figsize=(8, 4))
sns.pointplot(x='Grade', y='Suicide_Score', hue='Sad_Or_Hopeless', data=df_clean, dodge=0.1, capsize=0.05, markers=["o", "s"], linestyles=["-", "--"], palette={0: "#2b7bba", 1: "#d64b4b"})
plt.gca().set_yticklabels(['{:,.0f}%'.format(x*100) for x in plt.gca().get_yticks()])
plt.xticks(ticks=[0, 1, 2, 3], labels=['9th Grade', '10th Grade', '11th Grade', '12th Grade'])
plt.title('Impact of Depressive Mood on Suicide Plans Across Different Grades', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(figure_dir, '03_depression_grade_interaction.png'), dpi=300)
plt.close()

# ==============================================================================
# 🎨 圖表 4：性別與憂鬱比率對比圖
# ==============================================================================
plt.figure(figsize=(7, 4))
ax4 = sns.barplot(x='Sex', y='Sad_Or_Hopeless', data=df_clean, palette=['#e066a3', '#3594cc'], capsize=0.1, errorbar='ci')
plt.gca().set_yticklabels(['{:,.0f}%'.format(x*100) for x in plt.gca().get_yticks()])
plt.title('Prevalence of Depressive Mood (Sad/Hopeless) by Biological Sex', fontsize=11, fontweight='bold')
plt.xlabel('Biological Sex', fontsize=10, fontweight='bold')
plt.ylabel('Percentage Experiencing Depressive Mood (%)', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(figure_dir, '04_depression_by_sex.png'), dpi=300)
plt.close()

# ==============================================================================
# 🎨 圖表 5：性別差異交互作用圖
# ==============================================================================
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
plt.close()

print("\n🎉 成功！5 張高畫質精美圖表已由獨立腳本生成，並安全儲存至 outputs/figures/ 資料夾！")