"""
数据工程模块 - 数据清洗、特征工程、探索性数据分析
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

class DataProcessor:
    """数据处理和特征工程"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        
    def load_data(self, file_path):
        """加载数据"""
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                raise ValueError("支持的文件格式: CSV, XLSX")
            
            print(f"✅ 数据加载成功: {df.shape[0]}行, {df.shape[1]}列")
            return df
        except Exception as e:
            print(f"❌ 数据加载失败: {e}")
            return None
    
    def validate_required_fields(self, df):
        """验证必需字段"""
        required_fields = [
            'patient_id', 'age', 'sex', 'chief_complaint',
            'ALT', 'AST', 'AFP', 'imaging_result'
        ]
        
        missing_fields = [field for field in required_fields if field not in df.columns]
        
        if missing_fields:
            print(f"⚠️  缺失必需字段: {missing_fields}")
            return False
        
        print("✅ 必需字段验证通过")
        return True
    
    def clean_data(self, df):
        """数据清洗"""
        print("🧹 开始数据清洗...")
        
        # 1. 处理重复记录
        initial_rows = len(df)
        df = df.drop_duplicates(subset=['patient_id'])
        print(f"   移除重复记录: {initial_rows - len(df)}条")
        
        # 2. 处理异常值
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if col in ['age', 'ALT', 'AST', 'AFP']:
                # 使用IQR方法处理异常值
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
                if outliers > 0:
                    print(f"   {col}: 发现{outliers}个异常值")
                    # 用边界值替换异常值
                    df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
        
        # 3. 处理缺失值
        missing_info = df.isnull().sum()
        if missing_info.sum() > 0:
            print("   缺失值情况:")
            for col, missing_count in missing_info[missing_info > 0].items():
                missing_rate = missing_count / len(df) * 100
                print(f"     {col}: {missing_count}条 ({missing_rate:.1f}%)")
        
        print("✅ 数据清洗完成")
        return df
    
    def feature_engineering(self, df):
        """特征工程"""
        print("🔧 开始特征工程...")
        
        # 1. 创建年龄分组
        df['age_group'] = pd.cut(df['age'], bins=[0, 40, 60, 80, 100], 
                                labels=['青年', '中年', '老年', '高龄'])
        
        # 2. AFP分级
        if 'AFP' in df.columns:
            df['AFP_level'] = pd.cut(df['AFP'], bins=[0, 20, 400, float('inf')], 
                                   labels=['正常', '轻度升高', '显著升高'])
        
        # 3. 肝功能综合评分
        if all(col in df.columns for col in ['ALT', 'AST']):
            df['liver_function_score'] = (df['ALT'] / 40 + df['AST'] / 40) / 2
        
        # 4. 文本特征处理（症状描述）
        if 'chief_complaint' in df.columns:
            # 提取关键症状
            symptoms = ['疼痛', '乏力', '食欲减退', '体重下降', '腹胀', '黄疸']
            for symptom in symptoms:
                df[f'has_{symptom}'] = df['chief_complaint'].str.contains(symptom, na=False).astype(int)
        
        # 5. 影像特征提取
        if 'imaging_result' in df.columns:
            imaging_features = ['占位', '边界不清', '强化', '门静脉', '转移']
            for feature in imaging_features:
                df[f'imaging_{feature}'] = df['imaging_result'].str.contains(feature, na=False).astype(int)
        
        print("✅ 特征工程完成")
        return df
    
    def prepare_ml_data(self, df, target_column):
        """准备机器学习数据"""
        print("📊 准备机器学习数据...")
        
        # 分离特征和目标
        feature_columns = [col for col in df.columns 
                          if col not in ['patient_id', target_column, 'chief_complaint', 'imaging_result']]
        
        X = df[feature_columns].copy()
        y = df[target_column].copy()
        
        # 处理分类变量
        categorical_columns = X.select_dtypes(include=['object', 'category']).columns
        for col in categorical_columns:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                X[col] = self.label_encoders[col].fit_transform(X[col].fillna('unknown'))
            else:
                X[col] = self.label_encoders[col].transform(X[col].fillna('unknown'))
        
        # 处理数值变量缺失值
        numeric_columns = X.select_dtypes(include=[np.number]).columns
        if len(numeric_columns) > 0:
            imputer = SimpleImputer(strategy='median')
            X[numeric_columns] = imputer.fit_transform(X[numeric_columns])
        
        # 标准化数值特征
        X[numeric_columns] = self.scaler.fit_transform(X[numeric_columns])
        
        self.feature_columns = feature_columns
        
        print(f"✅ 数据准备完成: {X.shape[0]}样本, {X.shape[1]}特征")
        return X, y


class EDAAnalyzer:
    """探索性数据分析"""
    
    def __init__(self):
        plt.style.use('seaborn-v0_8')
        
    def basic_info(self, df):
        """基础信息分析"""
        print("📋 数据基础信息:")
        print(f"   数据形状: {df.shape}")
        print(f"   数据类型分布:")
        print(f"     数值型: {len(df.select_dtypes(include=[np.number]).columns)}列")
        print(f"     文本型: {len(df.select_dtypes(include=['object']).columns)}列")
        print(f"     日期型: {len(df.select_dtypes(include=['datetime']).columns)}列")
        
        # 缺失值统计
        missing_stats = df.isnull().sum().sort_values(ascending=False)
        if missing_stats.sum() > 0:
            print("\n   缺失值统计:")
            for col, missing in missing_stats[missing_stats > 0].head(10).items():
                rate = missing / len(df) * 100
                print(f"     {col}: {missing}条 ({rate:.1f}%)")
        
        return {
            'shape': df.shape,
            'missing_stats': missing_stats.to_dict(),
            'dtypes': df.dtypes.to_dict()
        }
    
    def plot_distributions(self, df, save_path=None):
        """绘制数值变量分布图"""
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        n_cols = min(4, len(numeric_columns))
        n_rows = (len(numeric_columns) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 4*n_rows))
        axes = axes.flatten() if n_rows > 1 else [axes]
        
        for i, col in enumerate(numeric_columns):
            if i < len(axes):
                df[col].hist(bins=30, ax=axes[i], alpha=0.7)
                axes[i].set_title(f'{col}分布')
                axes[i].set_xlabel(col)
                axes[i].set_ylabel('频次')
        
        # 隐藏多余的子图
        for i in range(len(numeric_columns), len(axes)):
            axes[i].set_visible(False)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def correlation_analysis(self, df, save_path=None):
        """相关性分析"""
        numeric_df = df.select_dtypes(include=[np.number])
        
        if len(numeric_df.columns) > 1:
            corr_matrix = numeric_df.corr()
            
            plt.figure(figsize=(12, 10))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, fmt='.2f')
            plt.title('特征相关性热力图')
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.show()
            
            return corr_matrix
        
        return None
    
    def survival_analysis_eda(self, df, duration_col='survival_months', event_col='death_event'):
        """生存分析EDA"""
        if duration_col not in df.columns or event_col not in df.columns:
            print(f"⚠️  缺少生存分析必需字段: {duration_col}, {event_col}")
            return None
        
        print("📊 生存分析EDA:")
        
        # 基础统计
        total_patients = len(df)
        events = df[event_col].sum()
        censored = total_patients - events
        
        print(f"   总患者数: {total_patients}")
        print(f"   事件发生: {events} ({events/total_patients*100:.1f}%)")
        print(f"   删失: {censored} ({censored/total_patients*100:.1f}%)")
        
        # 生存时间统计
        print(f"   随访时间: 中位数{df[duration_col].median():.1f}月")
        print(f"   随访范围: {df[duration_col].min():.1f} - {df[duration_col].max():.1f}月")
        
        # 绘制生存时间分布
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        # 生存时间直方图
        df[duration_col].hist(bins=30, ax=axes[0], alpha=0.7)
        axes[0].set_title('生存时间分布')
        axes[0].set_xlabel('生存时间(月)')
        axes[0].set_ylabel('患者数')
        
        # 事件发生时间
        event_times = df[df[event_col] == 1][duration_col]
        if len(event_times) > 0:
            event_times.hist(bins=20, ax=axes[1], alpha=0.7, color='red')
            axes[1].set_title('事件发生时间分布')
            axes[1].set_xlabel('事件时间(月)')
            axes[1].set_ylabel('事件数')
        
        plt.tight_layout()
        plt.show()
        
        return {
            'total_patients': total_patients,
            'events': events,
            'event_rate': events/total_patients,
            'median_followup': df[duration_col].median(),
            'followup_range': (df[duration_col].min(), df[duration_col].max())
        }
    
    def generate_eda_report(self, df, output_path="eda_report.html"):
        """生成EDA报告"""
        print("📈 生成EDA报告...")
        
        basic_stats = self.basic_info(df)
        
        # 创建HTML报告
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>探索性数据分析报告</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .header {{ background-color: #f0f8ff; padding: 20px; border-radius: 10px; }}
                .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #1f77b4; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏥 医疗数据探索性分析报告</h1>
                <p>生成时间: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="section">
                <h2>📊 数据基础信息</h2>
                <p><strong>数据形状:</strong> {df.shape[0]}行 × {df.shape[1]}列</p>
                <p><strong>数值型变量:</strong> {len(df.select_dtypes(include=[np.number]).columns)}个</p>
                <p><strong>文本型变量:</strong> {len(df.select_dtypes(include=['object']).columns)}个</p>
            </div>
            
            <div class="section">
                <h2>📋 变量统计摘要</h2>
                {df.describe().to_html()}
            </div>
            
            <div class="section">
                <h2>🔍 缺失值分析</h2>
                {df.isnull().sum().to_frame('缺失数量').to_html()}
            </div>
        </body>
        </html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ EDA报告已保存: {output_path}")
        return output_path


def create_sample_dataset(n_patients=500, save_path="sample_medical_data.csv"):
    """创建示例医疗数据集"""
    print(f"🔬 创建示例医疗数据集 ({n_patients}个患者)...")
    
    np.random.seed(42)
    
    # 基础信息
    data = {
        'patient_id': [f'P{i:04d}' for i in range(1, n_patients+1)],
        'age': np.random.normal(60, 15, n_patients).clip(20, 90),
        'sex': np.random.choice(['男', '女'], n_patients),
        'weight': np.random.normal(65, 12, n_patients).clip(40, 120),
    }
    
    # 合并疾病
    data['hypertension'] = np.random.choice([0, 1], n_patients, p=[0.7, 0.3])
    data['diabetes'] = np.random.choice([0, 1], n_patients, p=[0.8, 0.2])
    
    # 实验室检查
    data['ALT'] = np.random.lognormal(3.5, 0.8, n_patients).clip(10, 500)
    data['AST'] = np.random.lognormal(3.4, 0.7, n_patients).clip(10, 400)
    data['AFP'] = np.random.lognormal(2.5, 2.0, n_patients).clip(1, 10000)
    data['albumin'] = np.random.normal(40, 8, n_patients).clip(20, 60)
    data['bilirubin'] = np.random.lognormal(2.5, 0.8, n_patients).clip(5, 200)
    
    # 影像特征
    tumor_sizes = np.random.lognormal(1.2, 0.8, n_patients).clip(0.5, 15)
    data['tumor_size_cm'] = tumor_sizes
    data['portal_vein_invasion'] = np.random.choice([0, 1], n_patients, p=[0.75, 0.25])
    data['lymph_node_metastasis'] = np.random.choice([0, 1], n_patients, p=[0.8, 0.2])
    
    # 病理分级（如果有手术）
    data['histologic_grade'] = np.random.choice(['低分化', '中分化', '高分化'], n_patients, p=[0.3, 0.5, 0.2])
    
    # 治疗信息
    data['surgery_type'] = np.random.choice(['肝叶切除', '肝段切除', '局部切除'], n_patients, p=[0.4, 0.4, 0.2])
    data['r0_resection'] = np.random.choice([0, 1], n_patients, p=[0.2, 0.8])
    
    # 生存结局（模拟）
    # 基于风险因素计算生存时间
    risk_score = (
        (data['age'] > 65).astype(int) * 0.3 +
        (tumor_sizes > 5).astype(int) * 0.4 +
        data['portal_vein_invasion'] * 0.5 +
        (data['AFP'] > 400).astype(int) * 0.3 +
        data['lymph_node_metastasis'] * 0.6
    )
    
    # 生成生存时间（月）
    base_survival = 36  # 基础中位生存36个月
    survival_months = np.random.exponential(base_survival * np.exp(-risk_score))
    data['survival_months'] = survival_months.clip(1, 120)
    
    # 生成事件标志（死亡/删失）
    # 高风险患者更可能发生事件
    event_prob = 0.3 + risk_score * 0.4
    data['death_event'] = np.random.binomial(1, event_prob.clip(0, 0.8), n_patients)
    
    # 复发信息
    recurrence_prob = 0.2 + risk_score * 0.3
    data['recurrence'] = np.random.binomial(1, recurrence_prob.clip(0, 0.7), n_patients)
    data['recurrence_months'] = np.where(
        data['recurrence'] == 1,
        np.random.exponential(18) * (1 - risk_score * 0.3),
        np.nan
    ).clip(1, data['survival_months'])
    
    # 症状描述（文本）
    symptoms_templates = [
        "右上腹疼痛{duration}，伴食欲减退",
        "腹胀不适{duration}，体重下降",
        "乏力{duration}，偶有低热",
        "右上腹隐痛{duration}，伴恶心",
        "食欲不振{duration}，腹部不适"
    ]
    
    durations = ["3周", "1月", "2月", "3月", "半年"]
    data['chief_complaint'] = [
        np.random.choice(symptoms_templates).format(duration=np.random.choice(durations))
        for _ in range(n_patients)
    ]
    
    # 影像描述
    imaging_templates = [
        "CT提示肝{location}占位，大小约{size}cm，{enhancement}，{invasion}",
        "MRI显示肝{location}异常信号，{size}cm，{enhancement}，{invasion}",
        "超声发现肝{location}低回声区，{size}cm，{enhancement}，{invasion}"
    ]
    
    locations = ["右叶", "左叶", "左右叶"]
    enhancements = ["不均匀强化", "环形强化", "渐进性强化"]
    invasions = ["门静脉无侵犯", "门静脉受侵", "胆管受侵"]
    
    data['imaging_result'] = [
        np.random.choice(imaging_templates).format(
            location=np.random.choice(locations),
            size=f"{tumor_sizes[i]:.1f}",
            enhancement=np.random.choice(enhancements),
            invasion=np.random.choice(invasions)
        )
        for i in range(n_patients)
    ]
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 保存数据
    df.to_csv(save_path, index=False, encoding='utf-8')
    print(f"✅ 示例数据集已保存: {save_path}")
    
    return df
