"""
复发预测模块 - 术后复发和转移预测
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report
import xgboost as xgb
import lightgbm as lgb
import matplotlib.pyplot as plt
from datetime import datetime

class RecurrencePredictor:
    """复发预测器"""
    
    def __init__(self, model_type='xgboost', prediction_window=24):
        self.model_type = model_type
        self.prediction_window = prediction_window  # 预测窗口（月）
        self.model = None
        self.feature_names = None
        self.training_results = {}
        
    def prepare_recurrence_data(self, df, recurrence_col='recurrence', 
                              recurrence_time_col='recurrence_months'):
        """准备复发预测数据"""
        print(f"📊 准备复发预测数据（预测窗口：{self.prediction_window}月）...")
        
        # 验证必需列
        if recurrence_col not in df.columns:
            raise ValueError(f"缺少复发标志列: {recurrence_col}")
        
        # 创建时间窗口内复发标签
        if recurrence_time_col in df.columns:
            # 基于复发时间创建标签
            recurrence_in_window = (
                (df[recurrence_col] == 1) & 
                (df[recurrence_time_col] <= self.prediction_window)
            ).astype(int)
        else:
            # 直接使用复发标志
            recurrence_in_window = df[recurrence_col].astype(int)
        
        df = df.copy()
        df['recurrence_target'] = recurrence_in_window
        
        # 统计信息
        total_patients = len(df)
        recurrence_cases = recurrence_in_window.sum()
        recurrence_rate = recurrence_cases / total_patients
        
        print(f"✅ 复发数据准备完成:")
        print(f"   总患者数: {total_patients}")
        print(f"   {self.prediction_window}月内复发: {recurrence_cases} ({recurrence_rate:.2%})")
        
        return df
    
    def prepare_model(self):
        """准备复发预测模型"""
        if self.model_type == 'xgboost':
            self.model = xgb.XGBClassifier(
                objective='binary:logistic',
                eval_metric='auc',
                random_state=42,
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8
            )
        elif self.model_type == 'lightgbm':
            self.model = lgb.LGBMClassifier(
                objective='binary',
                metric='auc',
                random_state=42,
                n_estimators=200,
                max_depth=6,
                learning_rate=0.1,
                subsample=0.8,
                colsample_bytree=0.8,
                verbose=-1
            )
        elif self.model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=200,
                max_depth=10,
                random_state=42,
                class_weight='balanced'  # 处理类别不平衡
            )
        
        print(f"✅ {self.model_type}复发预测模型已准备")
        return self.model
    
    def train(self, df, target_col='recurrence_target', exclude_cols=None, test_size=0.2):
        """训练复发预测模型"""
        print(f"🚀 开始训练{self.model_type}复发预测模型...")
        
        # 准备特征
        exclude_cols = exclude_cols or [
            'patient_id', 'recurrence', 'recurrence_months', 'recurrence_target',
            'chief_complaint', 'imaging_result', 'survival_months', 'death_event'
        ]
        
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        
        X = df[feature_cols].copy()
        y = df[target_col].copy()
        
        # 处理分类变量
        for col in X.columns:
            if X[col].dtype == 'object':
                X[col] = pd.Categorical(X[col]).codes
        
        # 处理缺失值
        X = X.fillna(X.median())
        
        self.feature_names = feature_cols
        
        # 数据分割
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        # 训练模型
        if self.model is None:
            self.prepare_model()
        
        if self.model_type in ['xgboost', 'lightgbm']:
            self.model.fit(
                X_train, y_train,
                eval_set=[(X_test, y_test)],
                verbose=False
            )
        else:
            self.model.fit(X_train, y_train)
        
        # 预测和评估
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        y_pred = self.model.predict(X_test)
        
        # 计算性能指标
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        # 保存训练结果
        self.training_results = {
            'model_type': self.model_type,
            'prediction_window': self.prediction_window,
            'train_size': len(X_train),
            'test_size': len(X_test),
            'auc_score': auc_score,
            'feature_count': X.shape[1],
            'recurrence_rate': y.mean(),
            'training_time': datetime.now().isoformat()
        }
        
        print(f"✅ 复发预测模型训练完成")
        print(f"   训练集大小: {len(X_train)}")
        print(f"   测试集大小: {len(X_test)}")
        print(f"   AUC得分: {auc_score:.4f}")
        print(f"   复发率: {y.mean():.2%}")
        
        # 生成详细评估
        self._generate_evaluation_report(y_test, y_pred, y_pred_proba)
        
        return {
            'model': self.model,
            'auc_score': auc_score,
            'y_test': y_test,
            'y_pred': y_pred,
            'y_pred_proba': y_pred_proba
        }
    
    def _generate_evaluation_report(self, y_true, y_pred, y_pred_proba):
        """生成评估报告"""
        print("\n📊 复发预测模型性能评估:")
        
        # 分类报告
        print("\n分类报告:")
        print(classification_report(y_true, y_pred, target_names=['无复发', '复发']))
        
        # ROC曲线
        from sklearn.metrics import roc_curve, precision_recall_curve
        
        fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
        precision, recall, _ = precision_recall_curve(y_true, y_pred_proba)
        
        plt.figure(figsize=(15, 5))
        
        # ROC曲线
        plt.subplot(1, 3, 1)
        plt.plot(fpr, tpr, label=f'ROC曲线 (AUC = {roc_auc_score(y_true, y_pred_proba):.3f})')
        plt.plot([0, 1], [0, 1], 'k--', label='随机分类器')
        plt.xlabel('假阳性率')
        plt.ylabel('真阳性率')
        plt.title('ROC曲线')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # PR曲线
        plt.subplot(1, 3, 2)
        from sklearn.metrics import average_precision_score
        ap_score = average_precision_score(y_true, y_pred_proba)
        plt.plot(recall, precision, label=f'PR曲线 (AP = {ap_score:.3f})')
        plt.xlabel('召回率')
        plt.ylabel('精确率')
        plt.title('Precision-Recall曲线')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 预测概率分布
        plt.subplot(1, 3, 3)
        plt.hist(y_pred_proba[y_true == 0], bins=20, alpha=0.7, label='无复发', density=True)
        plt.hist(y_pred_proba[y_true == 1], bins=20, alpha=0.7, label='复发', density=True)
        plt.xlabel('预测概率')
        plt.ylabel('密度')
        plt.title('预测概率分布')
        plt.legend()
        
        plt.tight_layout()
        plt.show()
    
    def predict_recurrence(self, X):
        """预测复发风险"""
        if self.model is None:
            raise ValueError("模型尚未训练")
        
        # 确保特征顺序一致
        if hasattr(X, 'columns') and self.feature_names:
            X = X[self.feature_names]
        
        # 处理分类变量
        X_processed = X.copy()
        for col in X_processed.columns:
            if X_processed[col].dtype == 'object':
                X_processed[col] = pd.Categorical(X_processed[col]).codes
        
        # 处理缺失值
        X_processed = X_processed.fillna(X_processed.median())
        
        # 预测
        probabilities = self.model.predict_proba(X_processed)[:, 1]
        predictions = self.model.predict(X_processed)
        
        # 风险分层
        risk_levels = []
        for prob in probabilities:
            if prob > 0.7:
                risk_levels.append('高危')
            elif prob > 0.5:
                risk_levels.append('中高危')
            elif prob > 0.3:
                risk_levels.append('中等')
            else:
                risk_levels.append('低危')
        
        return {
            'predictions': predictions,
            'probabilities': probabilities,
            'risk_levels': risk_levels,
            'prediction_window': self.prediction_window
        }
    
    def get_feature_importance(self, top_n=10):
        """获取特征重要性"""
        if self.model is None:
            raise ValueError("模型尚未训练")
        
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
        else:
            print("⚠️  该模型不支持特征重要性分析")
            return None
        
        if self.feature_names:
            feature_importance = pd.DataFrame({
                'feature': self.feature_names,
                'importance': importances
            }).sort_values('importance', ascending=False)
        else:
            feature_importance = pd.DataFrame({
                'feature': [f'feature_{i}' for i in range(len(importances))],
                'importance': importances
            }).sort_values('importance', ascending=False)
        
        # 绘制特征重要性
        plt.figure(figsize=(12, 6))
        top_features = feature_importance.head(top_n)
        
        plt.barh(range(len(top_features)), top_features['importance'])
        plt.yticks(range(len(top_features)), top_features['feature'])
        plt.xlabel('重要性得分')
        plt.title(f'复发预测模型 - Top {top_n} 特征重要性')
        plt.gca().invert_yaxis()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        return feature_importance
    
    def analyze_recurrence_patterns(self, df, recurrence_col='recurrence', 
                                  recurrence_time_col='recurrence_months'):
        """分析复发模式"""
        print("🔍 分析复发模式...")
        
        if recurrence_col not in df.columns:
            print(f"⚠️  缺少复发列: {recurrence_col}")
            return None
        
        recurrence_data = df[df[recurrence_col] == 1].copy()
        
        if len(recurrence_data) == 0:
            print("⚠️  数据中无复发病例")
            return None
        
        analysis_results = {
            'total_recurrences': len(recurrence_data),
            'recurrence_rate': len(recurrence_data) / len(df)
        }
        
        if recurrence_time_col in df.columns:
            recurrence_times = recurrence_data[recurrence_time_col].dropna()
            
            analysis_results.update({
                'median_recurrence_time': recurrence_times.median(),
                'mean_recurrence_time': recurrence_times.mean(),
                'early_recurrence_rate': (recurrence_times <= 12).mean(),  # 1年内复发率
                'late_recurrence_rate': (recurrence_times > 24).mean()      # 2年后复发率
            })
            
            # 绘制复发时间分布
            plt.figure(figsize=(12, 4))
            
            plt.subplot(1, 2, 1)
            recurrence_times.hist(bins=20, alpha=0.7, edgecolor='black')
            plt.axvline(recurrence_times.median(), color='red', linestyle='--', 
                       label=f'中位数: {recurrence_times.median():.1f}月')
            plt.xlabel('复发时间 (月)')
            plt.ylabel('患者数')
            plt.title('复发时间分布')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            # 累积复发率
            plt.subplot(1, 2, 2)
            time_points = np.arange(0, recurrence_times.max() + 1, 3)
            cumulative_recurrence = []
            
            for t in time_points:
                cum_rate = (recurrence_times <= t).mean()
                cumulative_recurrence.append(cum_rate)
            
            plt.plot(time_points, cumulative_recurrence, marker='o')
            plt.xlabel('时间 (月)')
            plt.ylabel('累积复发率')
            plt.title('累积复发率曲线')
            plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.show()
        
        print(f"📊 复发模式分析结果:")
        for key, value in analysis_results.items():
            if isinstance(value, float):
                print(f"   {key}: {value:.3f}")
            else:
                print(f"   {key}: {value}")
        
        return analysis_results
    
    def identify_risk_factors(self, df, recurrence_col='recurrence'):
        """识别复发风险因素"""
        print("🔍 识别复发风险因素...")
        
        risk_factors = {}
        
        # 数值变量的风险因素分析
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col != recurrence_col:
                recurrence_group = df[df[recurrence_col] == 1][col].dropna()
                non_recurrence_group = df[df[recurrence_col] == 0][col].dropna()
                
                if len(recurrence_group) > 0 and len(non_recurrence_group) > 0:
                    # t检验
                    from scipy.stats import ttest_ind
                    t_stat, p_value = ttest_ind(recurrence_group, non_recurrence_group)
                    
                    risk_factors[col] = {
                        'recurrence_mean': recurrence_group.mean(),
                        'non_recurrence_mean': non_recurrence_group.mean(),
                        'p_value': p_value,
                        'significant': p_value < 0.05,
                        'effect_direction': 'increase' if recurrence_group.mean() > non_recurrence_group.mean() else 'decrease'
                    }
        
        # 分类变量的风险因素分析
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        for col in categorical_cols:
            if col != recurrence_col:
                # 卡方检验
                from scipy.stats import chi2_contingency
                contingency_table = pd.crosstab(df[col], df[recurrence_col])
                
                if contingency_table.shape[0] > 1 and contingency_table.shape[1] > 1:
                    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
                    
                    risk_factors[col] = {
                        'contingency_table': contingency_table.to_dict(),
                        'chi2_statistic': chi2,
                        'p_value': p_value,
                        'significant': p_value < 0.05
                    }
        
        # 筛选显著的风险因素
        significant_factors = {k: v for k, v in risk_factors.items() if v.get('significant', False)}
        
        print(f"✅ 发现{len(significant_factors)}个显著风险因素:")
        for factor, stats in significant_factors.items():
            print(f"   {factor}: p={stats['p_value']:.4f}")
        
        return risk_factors
    
    def predict(self, X):
        """预测新样本复发风险"""
        if self.model is None:
            raise ValueError("模型尚未训练")
        
        # 数据预处理
        X_processed = X.copy()
        
        # 确保特征顺序
        if hasattr(X, 'columns') and self.feature_names:
            X_processed = X_processed[self.feature_names]
        
        # 处理分类变量
        for col in X_processed.columns:
            if X_processed[col].dtype == 'object':
                X_processed[col] = pd.Categorical(X_processed[col]).codes
        
        # 处理缺失值
        X_processed = X_processed.fillna(X_processed.median())
        
        # 预测
        probabilities = self.model.predict_proba(X_processed)[:, 1]
        predictions = self.model.predict(X_processed)
        
        return predictions, probabilities
    
    def save_model(self, file_path):
        """保存模型"""
        import joblib
        
        if self.model is None:
            raise ValueError("模型尚未训练")
        
        model_data = {
            'model': self.model,
            'model_type': self.model_type,
            'prediction_window': self.prediction_window,
            'feature_names': self.feature_names,
            'training_results': self.training_results
        }
        
        joblib.dump(model_data, file_path)
        print(f"✅ 复发预测模型已保存: {file_path}")
    
    def load_model(self, file_path):
        """加载模型"""
        import joblib
        
        model_data = joblib.load(file_path)
        
        self.model = model_data['model']
        self.model_type = model_data['model_type']
        self.prediction_window = model_data['prediction_window']
        self.feature_names = model_data['feature_names']
        self.training_results = model_data.get('training_results', {})
        
        print(f"✅ 复发预测模型已加载: {file_path}")
        print(f"   模型类型: {self.model_type}")
        print(f"   预测窗口: {self.prediction_window}月")
        
        return self.model


def create_recurrence_pipeline(data_path, recurrence_col='recurrence', 
                             recurrence_time_col='recurrence_months',
                             prediction_window=24, model_type='xgboost'):
    """创建完整的复发预测流水线"""
    print("🔬 启动复发预测流水线...")
    
    # 1. 加载数据
    from .data_engineering import DataProcessor
    processor = DataProcessor()
    
    df = processor.load_data(data_path)
    if df is None:
        return None
    
    # 2. 数据清洗和特征工程
    df_clean = processor.clean_data(df)
    df_features = processor.feature_engineering(df_clean)
    
    # 3. 复发预测分析
    predictor = RecurrencePredictor(model_type, prediction_window)
    
    # 准备复发数据
    df_recurrence = predictor.prepare_recurrence_data(
        df_features, recurrence_col, recurrence_time_col
    )
    
    # 分析复发模式
    recurrence_patterns = predictor.analyze_recurrence_patterns(
        df_recurrence, recurrence_col, recurrence_time_col
    )
    
    # 识别风险因素
    risk_factors = predictor.identify_risk_factors(df_recurrence, recurrence_col)
    
    # 训练模型
    training_results = predictor.train(df_recurrence)
    
    # 特征重要性分析
    feature_importance = predictor.get_feature_importance()
    
    # 保存模型
    model_path = f"models/recurrence_{model_type}_{prediction_window}m_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
    predictor.save_model(model_path)
    
    return {
        'predictor': predictor,
        'training_results': training_results,
        'recurrence_patterns': recurrence_patterns,
        'risk_factors': risk_factors,
        'feature_importance': feature_importance,
        'model_path': model_path
    }
