"""
诊断模型模块 - 实现各种机器学习诊断模型
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score, roc_curve, confusion_matrix
import xgboost as xgb
import lightgbm as lgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class DiagnosticPredictor:
    """诊断预测模型"""
    
    def __init__(self, model_type='xgboost'):
        self.model_type = model_type
        self.model = None
        self.feature_names = None
        self.training_history = {}
        
    def prepare_model(self, model_type=None):
        """准备模型"""
        if model_type:
            self.model_type = model_type
            
        if self.model_type == 'xgboost':
            self.model = xgb.XGBClassifier(
                objective='binary:logistic',
                eval_metric='auc',
                random_state=42,
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1
            )
        elif self.model_type == 'lightgbm':
            self.model = lgb.LGBMClassifier(
                objective='binary',
                metric='auc',
                random_state=42,
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                verbose=-1
            )
        elif self.model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
        elif self.model_type == 'logistic':
            self.model = LogisticRegression(
                random_state=42,
                max_iter=1000
            )
        else:
            raise ValueError(f"不支持的模型类型: {model_type}")
        
        print(f"✅ {self.model_type}模型已准备")
        return self.model
    
    def train(self, X, y, test_size=0.2, validation=True):
        """训练模型"""
        print(f"🚀 开始训练{self.model_type}模型...")
        
        # 数据分割
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        self.feature_names = X.columns.tolist() if hasattr(X, 'columns') else None
        
        # 训练模型
        if self.model_type in ['xgboost', 'lightgbm']:
            # 支持验证集的模型
            eval_set = [(X_test, y_test)] if validation else None
            self.model.fit(
                X_train, y_train,
                eval_set=eval_set,
                verbose=False
            )
        else:
            self.model.fit(X_train, y_train)
        
        # 预测和评估
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        y_pred = self.model.predict(X_test)
        
        # 计算性能指标
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        # 保存训练历史
        self.training_history = {
            'model_type': self.model_type,
            'train_size': len(X_train),
            'test_size': len(X_test),
            'auc_score': auc_score,
            'training_time': datetime.now().isoformat(),
            'feature_count': X.shape[1]
        }
        
        print(f"✅ 模型训练完成")
        print(f"   训练集大小: {len(X_train)}")
        print(f"   测试集大小: {len(X_test)}")
        print(f"   AUC得分: {auc_score:.4f}")
        
        # 生成详细评估报告
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
        print("\n📊 模型性能评估:")
        
        # 分类报告
        print("\n分类报告:")
        print(classification_report(y_true, y_pred))
        
        # 混淆矩阵
        cm = confusion_matrix(y_true, y_pred)
        print(f"\n混淆矩阵:")
        print(f"   真阴性: {cm[0,0]}, 假阳性: {cm[0,1]}")
        print(f"   假阴性: {cm[1,0]}, 真阳性: {cm[1,1]}")
        
        # ROC曲线
        fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
        
        plt.figure(figsize=(12, 4))
        
        # ROC曲线
        plt.subplot(1, 3, 1)
        plt.plot(fpr, tpr, label=f'ROC曲线 (AUC = {roc_auc_score(y_true, y_pred_proba):.3f})')
        plt.plot([0, 1], [0, 1], 'k--', label='随机分类器')
        plt.xlabel('假阳性率')
        plt.ylabel('真阳性率')
        plt.title('ROC曲线')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 预测概率分布
        plt.subplot(1, 3, 2)
        plt.hist(y_pred_proba[y_true == 0], bins=20, alpha=0.7, label='阴性样本', density=True)
        plt.hist(y_pred_proba[y_true == 1], bins=20, alpha=0.7, label='阳性样本', density=True)
        plt.xlabel('预测概率')
        plt.ylabel('密度')
        plt.title('预测概率分布')
        plt.legend()
        
        # 混淆矩阵热力图
        plt.subplot(1, 3, 3)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.title('混淆矩阵')
        plt.ylabel('真实标签')
        plt.xlabel('预测标签')
        
        plt.tight_layout()
        plt.show()
    
    def predict(self, X):
        """预测新样本"""
        if self.model is None:
            raise ValueError("模型尚未训练，请先调用train()方法")
        
        if hasattr(X, 'columns') and self.feature_names:
            # 确保特征顺序一致
            X = X[self.feature_names]
        
        probabilities = self.model.predict_proba(X)[:, 1]
        predictions = self.model.predict(X)
        
        return predictions, probabilities
    
    def get_feature_importance(self, top_n=10):
        """获取特征重要性"""
        if self.model is None:
            raise ValueError("模型尚未训练")
        
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
        elif hasattr(self.model, 'coef_'):
            importances = np.abs(self.model.coef_[0])
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
        plt.figure(figsize=(10, 6))
        top_features = feature_importance.head(top_n)
        plt.barh(range(len(top_features)), top_features['importance'])
        plt.yticks(range(len(top_features)), top_features['feature'])
        plt.xlabel('重要性得分')
        plt.title(f'Top {top_n} 特征重要性')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.show()
        
        return feature_importance
    
    def hyperparameter_tuning(self, X, y, cv=5):
        """超参数调优"""
        print(f"🔧 开始{self.model_type}超参数调优...")
        
        if self.model_type == 'xgboost':
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [3, 6, 9],
                'learning_rate': [0.01, 0.1, 0.2],
                'subsample': [0.8, 0.9, 1.0]
            }
        elif self.model_type == 'lightgbm':
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [3, 6, 9],
                'learning_rate': [0.01, 0.1, 0.2],
                'subsample': [0.8, 0.9, 1.0]
            }
        elif self.model_type == 'random_forest':
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [5, 10, 15],
                'min_samples_split': [2, 5, 10]
            }
        else:
            param_grid = {
                'C': [0.1, 1, 10],
                'penalty': ['l1', 'l2']
            }
        
        grid_search = GridSearchCV(
            self.model, param_grid,
            cv=cv, scoring='roc_auc',
            n_jobs=-1, verbose=1
        )
        
        grid_search.fit(X, y)
        
        print(f"✅ 最佳参数: {grid_search.best_params_}")
        print(f"✅ 最佳CV得分: {grid_search.best_score_:.4f}")
        
        self.model = grid_search.best_estimator_
        return grid_search.best_params_, grid_search.best_score_
    
    def save_model(self, file_path):
        """保存模型"""
        if self.model is None:
            raise ValueError("模型尚未训练")
        
        model_data = {
            'model': self.model,
            'model_type': self.model_type,
            'feature_names': self.feature_names,
            'training_history': self.training_history
        }
        
        joblib.dump(model_data, file_path)
        print(f"✅ 模型已保存: {file_path}")
    
    def load_model(self, file_path):
        """加载模型"""
        model_data = joblib.load(file_path)
        
        self.model = model_data['model']
        self.model_type = model_data['model_type']
        self.feature_names = model_data['feature_names']
        self.training_history = model_data.get('training_history', {})
        
        print(f"✅ 模型已加载: {file_path}")
        print(f"   模型类型: {self.model_type}")
        print(f"   特征数量: {len(self.feature_names) if self.feature_names else 'Unknown'}")
        
        return self.model


class MultiClassDiagnosticPredictor(DiagnosticPredictor):
    """多分类诊断预测器"""
    
    def __init__(self, model_type='xgboost', n_classes=3):
        super().__init__(model_type)
        self.n_classes = n_classes
        
    def prepare_model(self, model_type=None):
        """准备多分类模型"""
        if model_type:
            self.model_type = model_type
            
        if self.model_type == 'xgboost':
            self.model = xgb.XGBClassifier(
                objective='multi:softprob',
                eval_metric='mlogloss',
                random_state=42,
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1
            )
        elif self.model_type == 'lightgbm':
            self.model = lgb.LGBMClassifier(
                objective='multiclass',
                metric='multi_logloss',
                random_state=42,
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                verbose=-1
            )
        elif self.model_type == 'random_forest':
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
        elif self.model_type == 'logistic':
            self.model = LogisticRegression(
                random_state=42,
                max_iter=1000,
                multi_class='ovr'
            )
        
        print(f"✅ {self.model_type}多分类模型已准备")
        return self.model


def create_diagnostic_pipeline(data_path, target_column, model_type='xgboost'):
    """创建完整的诊断模型训练流水线"""
    print("🔬 启动诊断模型训练流水线...")
    
    # 1. 加载数据
    from .data_engineering import DataProcessor
    processor = DataProcessor()
    
    df = processor.load_data(data_path)
    if df is None:
        return None
    
    # 2. 数据清洗和特征工程
    df_clean = processor.clean_data(df)
    df_features = processor.feature_engineering(df_clean)
    
    # 3. 准备ML数据
    X, y = processor.prepare_ml_data(df_features, target_column)
    
    # 4. 训练模型
    predictor = DiagnosticPredictor(model_type)
    predictor.prepare_model()
    
    results = predictor.train(X, y)
    
    # 5. 特征重要性分析
    feature_importance = predictor.get_feature_importance()
    
    # 6. 保存模型
    model_path = f"models/diagnostic_{model_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pkl"
    predictor.save_model(model_path)
    
    return {
        'predictor': predictor,
        'results': results,
        'feature_importance': feature_importance,
        'model_path': model_path
    }
