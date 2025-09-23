"""
模型可解释性分析模块 - SHAP分析、特征重要性、不确定度估计
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any, Optional

class ModelExplainer:
    """模型可解释性分析器"""
    
    def __init__(self):
        self.shap_explainer = None
        self.feature_names = None
        
    def setup_shap_explainer(self, model, X_background, model_type='tree'):
        """设置SHAP解释器"""
        try:
            import shap
            
            if model_type == 'tree':
                # 用于XGBoost、LightGBM、RandomForest
                self.shap_explainer = shap.TreeExplainer(model)
            elif model_type == 'linear':
                # 用于线性模型
                self.shap_explainer = shap.LinearExplainer(model, X_background)
            elif model_type == 'kernel':
                # 通用解释器，较慢但支持所有模型
                self.shap_explainer = shap.KernelExplainer(model.predict_proba, X_background)
            else:
                raise ValueError(f"不支持的模型类型: {model_type}")
            
            self.feature_names = X_background.columns.tolist() if hasattr(X_background, 'columns') else None
            print(f"✅ SHAP {model_type}解释器已设置")
            
        except ImportError:
            print("❌ 需要安装SHAP: pip install shap")
            return None
        except Exception as e:
            print(f"❌ SHAP解释器设置失败: {e}")
            return None
    
    def explain_prediction(self, X_sample, plot_explanation=True):
        """解释单个预测"""
        if self.shap_explainer is None:
            print("❌ SHAP解释器尚未设置")
            return None
        
        try:
            import shap
            
            # 计算SHAP值
            shap_values = self.shap_explainer.shap_values(X_sample)
            
            # 如果是二分类，取正类的SHAP值
            if isinstance(shap_values, list):
                shap_values = shap_values[1]
            
            # 确保是2D数组
            if len(shap_values.shape) == 1:
                shap_values = shap_values.reshape(1, -1)
            
            # 获取特征值
            if hasattr(X_sample, 'values'):
                feature_values = X_sample.values[0] if len(X_sample.shape) > 1 else X_sample.values
            else:
                feature_values = X_sample[0] if len(X_sample.shape) > 1 else X_sample
            
            # 创建特征贡献分析
            feature_contributions = {}
            if self.feature_names:
                for i, feature_name in enumerate(self.feature_names):
                    if i < len(shap_values[0]):
                        feature_contributions[feature_name] = {
                            "shap_value": float(shap_values[0][i]),
                            "feature_value": float(feature_values[i]),
                            "contribution_type": "正向" if shap_values[0][i] > 0 else "负向"
                        }
            
            # 排序特征贡献
            sorted_contributions = sorted(
                feature_contributions.items(),
                key=lambda x: abs(x[1]["shap_value"]),
                reverse=True
            )
            
            # 提取top因素
            top_positive = []
            top_negative = []
            
            for feature, contrib in sorted_contributions[:10]:
                if contrib["shap_value"] > 0:
                    top_positive.append({
                        "feature": feature,
                        "contribution": contrib["shap_value"],
                        "value": contrib["feature_value"]
                    })
                else:
                    top_negative.append({
                        "feature": feature,
                        "contribution": abs(contrib["shap_value"]),
                        "value": contrib["feature_value"]
                    })
            
            # 生成解释性总结
            explanation_summary = self._generate_explanation_summary(
                top_positive[:3], top_negative[:3]
            )
            
            # 绘制解释图
            if plot_explanation:
                self._plot_shap_explanation(shap_values, X_sample, feature_contributions)
            
            return {
                "shap_values": shap_values.tolist(),
                "feature_contributions": feature_contributions,
                "top_positive": top_positive[:5],
                "top_negative": top_negative[:5],
                "summary": explanation_summary
            }
            
        except Exception as e:
            print(f"❌ SHAP解释失败: {e}")
            return None
    
    def _generate_explanation_summary(self, top_positive: List, top_negative: List) -> str:
        """生成解释性总结"""
        summary_parts = []
        
        if top_positive:
            positive_features = [f"{item['feature']}({item['value']:.2f})" for item in top_positive]
            summary_parts.append(f"主要风险因素: {', '.join(positive_features)}")
        
        if top_negative:
            negative_features = [f"{item['feature']}({item['value']:.2f})" for item in top_negative]
            summary_parts.append(f"主要保护因素: {', '.join(negative_features)}")
        
        return "; ".join(summary_parts)
    
    def _plot_shap_explanation(self, shap_values, X_sample, feature_contributions):
        """绘制SHAP解释图"""
        try:
            import shap
            
            # 创建图形
            fig, axes = plt.subplots(1, 2, figsize=(15, 6))
            
            # 瀑布图
            if hasattr(shap, 'waterfall_plot'):
                shap.waterfall_plot(
                    shap.Explanation(
                        values=shap_values[0],
                        base_values=self.shap_explainer.expected_value,
                        data=X_sample.values[0] if hasattr(X_sample, 'values') else X_sample,
                        feature_names=self.feature_names
                    ),
                    show=False
                )
                plt.subplot(1, 2, 1)
                plt.title("SHAP瀑布图")
            
            # 特征贡献条形图
            plt.subplot(1, 2, 2)
            
            # 选择top10特征
            sorted_features = sorted(
                feature_contributions.items(),
                key=lambda x: abs(x[1]["shap_value"]),
                reverse=True
            )[:10]
            
            features = [item[0] for item in sorted_features]
            values = [item[1]["shap_value"] for item in sorted_features]
            colors = ['red' if v > 0 else 'blue' for v in values]
            
            plt.barh(range(len(features)), values, color=colors, alpha=0.7)
            plt.yticks(range(len(features)), features)
            plt.xlabel('SHAP值 (对预测的贡献)')
            plt.title('特征贡献度分析')
            plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)
            
            plt.tight_layout()
            plt.show()
            
        except Exception as e:
            print(f"⚠️  SHAP可视化失败: {e}")
    
    def global_feature_importance(self, X_data, model, top_n=20):
        """全局特征重要性分析"""
        if self.shap_explainer is None:
            print("❌ SHAP解释器尚未设置")
            return None
        
        try:
            import shap
            
            # 计算所有样本的SHAP值
            shap_values = self.shap_explainer.shap_values(X_data)
            
            if isinstance(shap_values, list):
                shap_values = shap_values[1]  # 取正类
            
            # 计算全局重要性
            global_importance = np.abs(shap_values).mean(0)
            
            # 创建重要性DataFrame
            if self.feature_names:
                importance_df = pd.DataFrame({
                    'feature': self.feature_names,
                    'importance': global_importance
                }).sort_values('importance', ascending=False)
            else:
                importance_df = pd.DataFrame({
                    'feature': [f'feature_{i}' for i in range(len(global_importance))],
                    'importance': global_importance
                }).sort_values('importance', ascending=False)
            
            # 绘制全局重要性
            plt.figure(figsize=(12, 8))
            top_features = importance_df.head(top_n)
            
            plt.subplot(2, 1, 1)
            plt.barh(range(len(top_features)), top_features['importance'])
            plt.yticks(range(len(top_features)), top_features['feature'])
            plt.xlabel('平均|SHAP值|')
            plt.title(f'全局特征重要性 (Top {top_n})')
            plt.gca().invert_yaxis()
            
            # SHAP summary plot
            plt.subplot(2, 1, 2)
            if hasattr(shap, 'summary_plot'):
                shap.summary_plot(shap_values, X_data, feature_names=self.feature_names, show=False)
                plt.title('SHAP特征影响分布')
            
            plt.tight_layout()
            plt.show()
            
            return importance_df
            
        except Exception as e:
            print(f"❌ 全局重要性分析失败: {e}")
            return None
    
    def analyze_feature_interactions(self, X_sample, feature_pairs=None):
        """分析特征交互效应"""
        if self.shap_explainer is None:
            print("❌ SHAP解释器尚未设置")
            return None
        
        try:
            import shap
            
            if feature_pairs is None and self.feature_names:
                # 自动选择重要特征对
                importance = self.global_feature_importance(X_sample, None, top_n=5)
                if importance is not None:
                    top_features = importance.head(5)['feature'].tolist()
                    feature_pairs = [(top_features[i], top_features[j]) 
                                   for i in range(len(top_features)) 
                                   for j in range(i+1, len(top_features))][:3]
            
            if feature_pairs and hasattr(shap, 'dependence_plot'):
                fig, axes = plt.subplots(1, len(feature_pairs), figsize=(5*len(feature_pairs), 4))
                if len(feature_pairs) == 1:
                    axes = [axes]
                
                shap_values = self.shap_explainer.shap_values(X_sample)
                if isinstance(shap_values, list):
                    shap_values = shap_values[1]
                
                for i, (feat1, feat2) in enumerate(feature_pairs):
                    if feat1 in self.feature_names and feat2 in self.feature_names:
                        feat1_idx = self.feature_names.index(feat1)
                        
                        plt.subplot(1, len(feature_pairs), i+1)
                        shap.dependence_plot(
                            feat1_idx, shap_values, X_sample,
                            interaction_index=feat2,
                            feature_names=self.feature_names,
                            show=False
                        )
                        plt.title(f'{feat1} vs {feat2}交互效应')
                
                plt.tight_layout()
                plt.show()
            
            return feature_pairs
            
        except Exception as e:
            print(f"❌ 特征交互分析失败: {e}")
            return None


class UncertaintyEstimator:
    """不确定度估计器"""
    
    @staticmethod
    def bootstrap_confidence_interval(model, X, y, n_bootstrap=100, confidence_level=0.95):
        """Bootstrap置信区间估计"""
        print(f"🔄 进行Bootstrap不确定度估计 (n={n_bootstrap})...")
        
        bootstrap_scores = []
        n_samples = len(X)
        
        for i in range(n_bootstrap):
            # Bootstrap采样
            indices = np.random.choice(n_samples, n_samples, replace=True)
            X_boot = X.iloc[indices] if hasattr(X, 'iloc') else X[indices]
            y_boot = y.iloc[indices] if hasattr(y, 'iloc') else y[indices]
            
            # 训练模型
            model_copy = model.__class__(**model.get_params())
            model_copy.fit(X_boot, y_boot)
            
            # 评估性能
            if hasattr(model_copy, 'predict_proba'):
                y_pred_proba = model_copy.predict_proba(X)[:, 1]
                from sklearn.metrics import roc_auc_score
                score = roc_auc_score(y, y_pred_proba)
            else:
                from sklearn.metrics import accuracy_score
                y_pred = model_copy.predict(X)
                score = accuracy_score(y, y_pred)
            
            bootstrap_scores.append(score)
        
        # 计算置信区间
        alpha = 1 - confidence_level
        lower_percentile = (alpha / 2) * 100
        upper_percentile = (1 - alpha / 2) * 100
        
        ci_lower = np.percentile(bootstrap_scores, lower_percentile)
        ci_upper = np.percentile(bootstrap_scores, upper_percentile)
        mean_score = np.mean(bootstrap_scores)
        std_score = np.std(bootstrap_scores)
        
        print(f"✅ Bootstrap结果:")
        print(f"   平均性能: {mean_score:.4f} ± {std_score:.4f}")
        print(f"   {confidence_level*100}%置信区间: [{ci_lower:.4f}, {ci_upper:.4f}]")
        
        return {
            'mean_score': mean_score,
            'std_score': std_score,
            'confidence_interval': (ci_lower, ci_upper),
            'bootstrap_scores': bootstrap_scores
        }
    
    @staticmethod
    def prediction_uncertainty(model, X_sample, n_iterations=100):
        """预测不确定度估计"""
        if not hasattr(model, 'predict_proba'):
            print("⚠️  模型不支持概率预测，无法估计不确定度")
            return None
        
        # 使用模型的内在不确定性（如果支持）
        predictions = []
        
        for _ in range(n_iterations):
            # 添加小量噪声来估计不确定性
            noise_scale = 0.01
            X_noisy = X_sample + np.random.normal(0, noise_scale, X_sample.shape)
            pred_proba = model.predict_proba(X_noisy)[:, 1]
            predictions.append(pred_proba[0])
        
        mean_pred = np.mean(predictions)
        std_pred = np.std(predictions)
        
        # 计算置信区间
        ci_lower = np.percentile(predictions, 2.5)
        ci_upper = np.percentile(predictions, 97.5)
        
        uncertainty_level = "低" if std_pred < 0.05 else "中" if std_pred < 0.1 else "高"
        
        return {
            'mean_prediction': mean_pred,
            'std_prediction': std_pred,
            'confidence_interval': (ci_lower, ci_upper),
            'uncertainty_level': uncertainty_level,
            'all_predictions': predictions
        }
    
    @staticmethod
    def calibration_analysis(y_true, y_pred_proba, n_bins=10):
        """模型校准分析"""
        from sklearn.calibration import calibration_curve
        
        # 计算校准曲线
        fraction_of_positives, mean_predicted_value = calibration_curve(
            y_true, y_pred_proba, n_bins=n_bins
        )
        
        # 绘制校准曲线
        plt.figure(figsize=(10, 6))
        
        plt.subplot(1, 2, 1)
        plt.plot(mean_predicted_value, fraction_of_positives, "s-", label="模型校准")
        plt.plot([0, 1], [0, 1], "k:", label="完美校准")
        plt.xlabel("平均预测概率")
        plt.ylabel("实际阳性比例")
        plt.title("校准曲线")
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 预测概率直方图
        plt.subplot(1, 2, 2)
        plt.hist(y_pred_proba, bins=20, alpha=0.7, density=True)
        plt.xlabel("预测概率")
        plt.ylabel("密度")
        plt.title("预测概率分布")
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # 计算Brier Score
        brier_score = np.mean((y_pred_proba - y_true) ** 2)
        
        return {
            'calibration_curve': (fraction_of_positives, mean_predicted_value),
            'brier_score': brier_score,
            'is_well_calibrated': brier_score < 0.1
        }


class ClinicalDecisionSupport:
    """临床决策支持"""
    
    @staticmethod
    def generate_risk_stratification(evidence_bundle: Dict) -> Dict:
        """生成风险分层建议"""
        risk_stratification = {
            "overall_risk": "中等",
            "risk_factors": [],
            "protective_factors": [],
            "actionable_recommendations": []
        }
        
        # 综合各模型的风险评估
        diagnostic_prob = evidence_bundle.get('diagnostic_prediction', {}).get('probability', 0)
        survival_risk = evidence_bundle.get('survival_prediction', {}).get('risk_group', '')
        recurrence_prob = evidence_bundle.get('recurrence_prediction', {}).get('recurrence_probability_2yr', 0)
        
        # 计算综合风险分数
        risk_score = 0
        if diagnostic_prob > 0.8:
            risk_score += 2
        elif diagnostic_prob > 0.6:
            risk_score += 1
        
        if '高危' in survival_risk:
            risk_score += 2
        elif '中高危' in survival_risk:
            risk_score += 1
        
        if recurrence_prob > 0.5:
            risk_score += 2
        elif recurrence_prob > 0.3:
            risk_score += 1
        
        # 确定总体风险等级
        if risk_score >= 5:
            risk_stratification["overall_risk"] = "高危"
        elif risk_score >= 3:
            risk_stratification["overall_risk"] = "中高危"
        elif risk_score >= 1:
            risk_stratification["overall_risk"] = "中等"
        else:
            risk_stratification["overall_risk"] = "低危"
        
        # 生成具体建议
        if risk_stratification["overall_risk"] in ["高危", "中高危"]:
            risk_stratification["actionable_recommendations"].extend([
                "建议多学科团队会诊",
                "考虑积极的综合治疗方案",
                "密切监测和随访"
            ])
        
        return risk_stratification
    
    @staticmethod
    def generate_treatment_timeline(evidence_bundle: Dict) -> Dict:
        """生成治疗时间线建议"""
        timeline = {
            "immediate": [],      # 立即（1-3天）
            "short_term": [],     # 短期（1-2周）
            "medium_term": [],    # 中期（1-3月）
            "long_term": []       # 长期（>3月）
        }
        
        # 基于风险分层制定时间线
        diagnostic_prob = evidence_bundle.get('diagnostic_prediction', {}).get('probability', 0)
        
        if diagnostic_prob > 0.8:
            timeline["immediate"].append("完善影像学检查")
            timeline["short_term"].append("专科会诊和治疗方案制定")
            timeline["medium_term"].append("实施治疗方案")
            timeline["long_term"].append("长期随访和监测")
        
        return timeline
