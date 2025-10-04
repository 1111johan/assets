"""
生存分析模块 - Cox回归、生存预测、风险分层
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.utils import concordance_index
from lifelines.statistics import logrank_test
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class SurvivalAnalyzer:
    """生存分析器"""
    
    def __init__(self):
        self.cox_model = None
        self.km_fitter = None
        self.feature_names = None
        self.training_results = {}
        
    def prepare_survival_data(self, df, duration_col='survival_months', event_col='death_event'):
        """准备生存分析数据"""
        print("📊 准备生存分析数据...")
        
        # 验证必需列
        if duration_col not in df.columns:
            raise ValueError(f"缺少生存时间列: {duration_col}")
        if event_col not in df.columns:
            raise ValueError(f"缺少事件列: {event_col}")
        
        # 数据验证
        if df[duration_col].isnull().any():
            print("⚠️  生存时间存在缺失值，将被移除")
            df = df.dropna(subset=[duration_col])
        
        if df[event_col].isnull().any():
            print("⚠️  事件标志存在缺失值，将被移除")
            df = df.dropna(subset=[event_col])
        
        # 确保时间为正数
        if (df[duration_col] <= 0).any():
            print("⚠️  发现非正数生存时间，将被修正")
            df = df[df[duration_col] > 0]
        
        # 确保事件为0/1
        unique_events = df[event_col].unique()
        if not set(unique_events).issubset({0, 1}):
            print(f"⚠️  事件列包含非0/1值: {unique_events}")
            df[event_col] = df[event_col].astype(int)
        
        print(f"✅ 生存数据准备完成: {len(df)}个样本")
        print(f"   事件发生率: {df[event_col].mean():.2%}")
        print(f"   中位随访时间: {df[duration_col].median():.1f}月")
        
        return df
    
    def kaplan_meier_analysis(self, df, duration_col='survival_months', event_col='death_event', 
                            group_col=None, save_plot=None):
        """Kaplan-Meier生存分析"""
        print("📈 进行Kaplan-Meier生存分析...")
        
        self.km_fitter = KaplanMeierFitter()
        
        plt.figure(figsize=(12, 6))
        
        if group_col and group_col in df.columns:
            # 分组生存分析
            groups = df[group_col].unique()
            
            for group in groups:
                group_data = df[df[group_col] == group]
                self.km_fitter.fit(
                    group_data[duration_col],
                    group_data[event_col],
                    label=f'{group_col}={group}'
                )
                self.km_fitter.plot_survival_function()
            
            # 进行log-rank检验
            if len(groups) == 2:
                group1 = df[df[group_col] == groups[0]]
                group2 = df[df[group_col] == groups[1]]
                
                logrank_result = logrank_test(
                    group1[duration_col], group2[duration_col],
                    group1[event_col], group2[event_col]
                )
                
                plt.title(f'Kaplan-Meier生存曲线\nLog-rank p值: {logrank_result.p_value:.4f}')
            else:
                plt.title('Kaplan-Meier生存曲线（分组比较）')
        else:
            # 整体生存分析
            self.km_fitter.fit(df[duration_col], df[event_col], label='整体人群')
            self.km_fitter.plot_survival_function()
            
            median_survival = self.km_fitter.median_survival_time_
            plt.title(f'Kaplan-Meier生存曲线\n中位生存时间: {median_survival:.1f}月')
        
        plt.xlabel('时间 (月)')
        plt.ylabel('生存概率')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        if save_plot:
            plt.savefig(save_plot, dpi=300, bbox_inches='tight')
        plt.show()
        
        return self.km_fitter
    
    def cox_regression(self, df, duration_col='survival_months', event_col='death_event', 
                      exclude_cols=None):
        """Cox比例风险回归"""
        print("🔬 进行Cox比例风险回归分析...")
        
        # 准备数据
        exclude_cols = exclude_cols or ['patient_id', 'chief_complaint', 'imaging_result']
        feature_cols = [col for col in df.columns 
                       if col not in exclude_cols + [duration_col, event_col]]
        
        # 创建分析数据框
        analysis_df = df[feature_cols + [duration_col, event_col]].copy()
        
        # 处理分类变量
        for col in analysis_df.columns:
            if analysis_df[col].dtype == 'object':
                analysis_df[col] = pd.Categorical(analysis_df[col]).codes
        
        # 重命名列以符合lifelines要求
        analysis_df = analysis_df.rename(columns={
            duration_col: 'T',
            event_col: 'E'
        })
        
        # 拟合Cox模型
        self.cox_model = CoxPHFitter()
        self.cox_model.fit(analysis_df, duration_col='T', event_col='E')
        
        # 输出结果
        print("\n📊 Cox回归结果:")
        self.cox_model.print_summary()
        
        # 计算C-index
        c_index = self.cox_model.concordance_index_
        print(f"\n✅ C-index (一致性指数): {c_index:.4f}")
        
        # 保存特征名称
        self.feature_names = feature_cols
        
        # 保存训练结果
        self.training_results = {
            'c_index': c_index,
            'feature_names': feature_cols,
            'n_samples': len(analysis_df),
            'event_rate': analysis_df['E'].mean()
        }
        
        return self.cox_model
    
    def predict_survival(self, X, times=None):
        """预测生存概率"""
        if self.cox_model is None:
            raise ValueError("Cox模型尚未训练")
        
        if times is None:
            times = [12, 24, 36, 60]  # 1年、2年、3年、5年
        
        # 确保特征顺序一致
        if hasattr(X, 'columns') and self.feature_names:
            X = X[self.feature_names]
        
        # 预测生存函数
        survival_functions = self.cox_model.predict_survival_function(X)
        
        predictions = {}
        for time in times:
            predictions[f'survival_prob_{time}m'] = [
                sf(time) if time <= sf.timeline.max() else np.nan 
                for sf in survival_functions
            ]
        
        # 预测中位生存时间
        median_survival = self.cox_model.predict_median(X)
        predictions['median_survival_months'] = median_survival
        
        # 风险分层
        risk_scores = self.cox_model.predict_partial_hazard(X)
        risk_quartiles = np.percentile(risk_scores, [25, 50, 75])
        
        risk_groups = []
        for score in risk_scores:
            if score <= risk_quartiles[0]:
                risk_groups.append('低危')
            elif score <= risk_quartiles[1]:
                risk_groups.append('中低危')
            elif score <= risk_quartiles[2]:
                risk_groups.append('中高危')
            else:
                risk_groups.append('高危')
        
        predictions['risk_group'] = risk_groups
        predictions['risk_score'] = risk_scores
        
        return predictions
    
    def plot_survival_curves(self, df, duration_col='survival_months', event_col='death_event',
                           risk_groups=None, save_plot=None):
        """绘制生存曲线"""
        plt.figure(figsize=(12, 8))
        
        if risk_groups is not None:
            # 按风险分组绘制
            unique_groups = np.unique(risk_groups)
            colors = ['green', 'yellow', 'orange', 'red']
            
            for i, group in enumerate(unique_groups):
                group_mask = risk_groups == group
                group_data = df[group_mask]
                
                kmf = KaplanMeierFitter()
                kmf.fit(
                    group_data[duration_col],
                    group_data[event_col],
                    label=f'{group} (n={len(group_data)})'
                )
                
                kmf.plot_survival_function(color=colors[i % len(colors)])
        else:
            # 整体生存曲线
            kmf = KaplanMeierFitter()
            kmf.fit(df[duration_col], df[event_col], label=f'整体 (n={len(df)})')
            kmf.plot_survival_function()
        
        plt.xlabel('时间 (月)')
        plt.ylabel('生存概率')
        plt.title('生存曲线分析')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        if save_plot:
            plt.savefig(save_plot, dpi=300, bbox_inches='tight')
        plt.show()
    
    def validate_model(self, df, duration_col='survival_months', event_col='death_event', 
                      test_size=0.2):
        """模型验证"""
        print("🔍 进行模型验证...")
        
        if self.cox_model is None:
            raise ValueError("Cox模型尚未训练")
        
        # 分割数据
        train_df, test_df = train_test_split(df, test_size=test_size, random_state=42)
        
        # 在测试集上计算C-index
        test_features = test_df[self.feature_names]
        test_duration = test_df[duration_col]
        test_event = test_df[event_col]
        
        # 处理分类变量
        for col in test_features.columns:
            if test_features[col].dtype == 'object':
                test_features[col] = pd.Categorical(test_features[col]).codes
        
        # 预测风险分数
        risk_scores = self.cox_model.predict_partial_hazard(test_features)
        
        # 计算测试集C-index
        test_c_index = concordance_index(test_duration, -risk_scores, test_event)
        
        print(f"✅ 测试集C-index: {test_c_index:.4f}")
        
        # 校准分析
        self._calibration_analysis(test_df, duration_col, event_col)
        
        return {
            'test_c_index': test_c_index,
            'train_c_index': self.training_results.get('c_index'),
            'test_size': len(test_df)
        }
    
    def _calibration_analysis(self, df, duration_col, event_col, time_points=[12, 24, 36]):
        """校准分析"""
        print("📏 进行模型校准分析...")
        
        # 预测不同时间点的生存概率
        features = df[self.feature_names]
        
        # 处理分类变量
        for col in features.columns:
            if features[col].dtype == 'object':
                features[col] = pd.Categorical(features[col]).codes
        
        predictions = self.predict_survival(features, times=time_points)
        
        # 计算实际生存率
        for time_point in time_points:
            pred_col = f'survival_prob_{time_point}m'
            if pred_col in predictions:
                # 实际在该时间点的生存状态
                actual_survival = ((df[duration_col] > time_point) | 
                                 ((df[duration_col] <= time_point) & (df[event_col] == 0)))
                
                pred_survival = predictions[pred_col]
                
                # 简单校准分析
                valid_idx = ~np.isnan(pred_survival)
                if valid_idx.sum() > 0:
                    correlation = np.corrcoef(
                        actual_survival[valid_idx].astype(float),
                        pred_survival[valid_idx]
                    )[0, 1]
                    
                    print(f"   {time_point}月生存预测相关性: {correlation:.3f}")


class DeepSurvivalAnalyzer:
    """深度学习生存分析（基于DeepSurv概念的简化实现）"""
    
    def __init__(self, hidden_layers=[64, 32], dropout_rate=0.3):
        self.hidden_layers = hidden_layers
        self.dropout_rate = dropout_rate
        self.model = None
        
    def build_model(self, input_dim):
        """构建神经网络模型"""
        try:
            import tensorflow as tf
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import Dense, Dropout
            from tensorflow.keras.regularizers import l2
            
            model = Sequential()
            
            # 输入层
            model.add(Dense(self.hidden_layers[0], input_dim=input_dim, 
                          activation='relu', kernel_regularizer=l2(0.01)))
            model.add(Dropout(self.dropout_rate))
            
            # 隐藏层
            for units in self.hidden_layers[1:]:
                model.add(Dense(units, activation='relu', kernel_regularizer=l2(0.01)))
                model.add(Dropout(self.dropout_rate))
            
            # 输出层（线性激活用于风险预测）
            model.add(Dense(1, activation='linear'))
            
            self.model = model
            print("✅ 深度生存模型构建完成")
            return model
            
        except ImportError:
            print("❌ 需要安装TensorFlow: pip install tensorflow")
            return None
    
    def train(self, X, duration, event, epochs=100, batch_size=32):
        """训练深度生存模型"""
        if self.model is None:
            self.build_model(X.shape[1])
        
        try:
            # 这里需要实现自定义的Cox损失函数
            # 简化版本：使用排序损失
            print("🚀 开始训练深度生存模型...")
            print("💡 注意：这是简化实现，完整版需要专门的Cox损失函数")
            
            # 创建排序标签（生存时间排序）
            sort_idx = np.argsort(-duration)  # 按生存时间降序排序
            y_rank = np.zeros(len(duration))
            y_rank[sort_idx] = np.arange(len(duration))
            y_rank = y_rank / len(duration)  # 归一化到[0,1]
            
            # 编译模型
            self.model.compile(optimizer='adam', loss='mse', metrics=['mae'])
            
            # 训练
            history = self.model.fit(
                X, y_rank,
                epochs=epochs,
                batch_size=batch_size,
                validation_split=0.2,
                verbose=1
            )
            
            print("✅ 深度生存模型训练完成")
            return history
            
        except Exception as e:
            print(f"❌ 深度模型训练失败: {e}")
            return None


def create_survival_pipeline(data_path, duration_col='survival_months', 
                           event_col='death_event', model_type='cox'):
    """创建完整的生存分析流水线"""
    print("🔬 启动生存分析流水线...")
    
    # 1. 加载数据
    from .data_engineering import DataProcessor
    processor = DataProcessor()
    
    df = processor.load_data(data_path)
    if df is None:
        return None
    
    # 2. 数据清洗
    df_clean = processor.clean_data(df)
    df_features = processor.feature_engineering(df_clean)
    
    # 3. 生存分析
    analyzer = SurvivalAnalyzer()
    survival_df = analyzer.prepare_survival_data(df_features, duration_col, event_col)
    
    # 4. Kaplan-Meier分析
    km_fitter = analyzer.kaplan_meier_analysis(survival_df, duration_col, event_col)
    
    # 5. Cox回归
    cox_model = analyzer.cox_regression(survival_df, duration_col, event_col)
    
    # 6. 模型验证
    validation_results = analyzer.validate_model(survival_df, duration_col, event_col)
    
    # 7. 保存模型
    import joblib
    from datetime import datetime
    model_path = f"models/survival_cox_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
    
    model_data = {
        'cox_model': cox_model,
        'analyzer': analyzer,
        'validation_results': validation_results,
        'feature_names': analyzer.feature_names
    }
    
    joblib.dump(model_data, model_path)
    print(f"✅ 生存模型已保存: {model_path}")
    
    return {
        'analyzer': analyzer,
        'cox_model': cox_model,
        'validation_results': validation_results,
        'model_path': model_path
    }
