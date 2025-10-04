"""
证据包模块 - 将模型预测结果打包成结构化证据，供LLM使用
"""

import json
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional

class EvidenceBuilder:
    """证据包构建器"""
    
    def __init__(self):
        self.diagnostic_model = None
        self.survival_model = None
        self.recurrence_model = None
        self.explainer = None
        
    def set_models(self, diagnostic_model=None, survival_model=None, 
                   recurrence_model=None, explainer=None):
        """设置模型"""
        if diagnostic_model:
            self.diagnostic_model = diagnostic_model
        if survival_model:
            self.survival_model = survival_model
        if recurrence_model:
            self.recurrence_model = recurrence_model
        if explainer:
            self.explainer = explainer
    
    def build_evidence_bundle(self, patient_data: Dict, include_uncertainty=True) -> Dict:
        """构建完整的证据包"""
        print("📦 构建证据包...")
        
        evidence = {
            "patient_info": self._extract_patient_info(patient_data),
            "timestamp": datetime.now().isoformat(),
            "evidence_version": "1.0"
        }
        
        # 转换为DataFrame用于模型预测
        patient_df = pd.DataFrame([patient_data])
        
        # 诊断模型预测
        if self.diagnostic_model:
            evidence["diagnostic_prediction"] = self._get_diagnostic_evidence(patient_df)
        
        # 生存分析预测
        if self.survival_model:
            evidence["survival_prediction"] = self._get_survival_evidence(patient_df)
        
        # 复发预测
        if self.recurrence_model:
            evidence["recurrence_prediction"] = self._get_recurrence_evidence(patient_df)
        
        # 可解释性分析
        if self.explainer:
            evidence["explainability"] = self._get_explainability_evidence(patient_df)
        
        # 不确定度估计
        if include_uncertainty:
            evidence["uncertainty"] = self._estimate_uncertainty(patient_df)
        
        # 临床建议
        evidence["clinical_recommendations"] = self._generate_clinical_recommendations(evidence)
        
        print("✅ 证据包构建完成")
        return evidence
    
    def _extract_patient_info(self, patient_data: Dict) -> Dict:
        """提取患者基础信息"""
        return {
            "age": patient_data.get("age"),
            "sex": patient_data.get("sex"),
            "chief_complaint": patient_data.get("chief_complaint"),
            "key_labs": {
                "ALT": patient_data.get("ALT"),
                "AST": patient_data.get("AST"),
                "AFP": patient_data.get("AFP"),
                "albumin": patient_data.get("albumin")
            },
            "imaging": patient_data.get("imaging_result"),
            "comorbidities": {
                "hypertension": patient_data.get("hypertension", 0),
                "diabetes": patient_data.get("diabetes", 0)
            }
        }
    
    def _get_diagnostic_evidence(self, patient_df: pd.DataFrame) -> Dict:
        """获取诊断预测证据"""
        try:
            predictions, probabilities = self.diagnostic_model.predict(patient_df)
            feature_importance = self.diagnostic_model.get_feature_importance(top_n=5)
            
            return {
                "prediction": "阳性" if predictions[0] == 1 else "阴性",
                "probability": float(probabilities[0]),
                "confidence_level": self._get_confidence_level(probabilities[0]),
                "top_contributing_factors": feature_importance.head(5).to_dict('records') if feature_importance is not None else [],
                "model_performance": {
                    "auc_score": self.diagnostic_model.training_history.get("auc_score"),
                    "model_type": self.diagnostic_model.model_type
                }
            }
        except Exception as e:
            print(f"⚠️  诊断预测失败: {e}")
            return {"error": str(e)}
    
    def _get_survival_evidence(self, patient_df: pd.DataFrame) -> Dict:
        """获取生存预测证据"""
        try:
            survival_predictions = self.survival_model.predict_survival(patient_df)
            
            return {
                "median_survival_months": float(survival_predictions["median_survival_months"][0]),
                "survival_probabilities": {
                    "1_year": float(survival_predictions.get("survival_prob_12m", [np.nan])[0]),
                    "2_year": float(survival_predictions.get("survival_prob_24m", [np.nan])[0]),
                    "3_year": float(survival_predictions.get("survival_prob_36m", [np.nan])[0]),
                    "5_year": float(survival_predictions.get("survival_prob_60m", [np.nan])[0])
                },
                "risk_group": survival_predictions["risk_group"][0],
                "risk_score": float(survival_predictions["risk_score"][0]),
                "model_performance": {
                    "c_index": self.survival_model.training_results.get("c_index"),
                    "model_type": "Cox回归"
                }
            }
        except Exception as e:
            print(f"⚠️  生存预测失败: {e}")
            return {"error": str(e)}
    
    def _get_recurrence_evidence(self, patient_df: pd.DataFrame) -> Dict:
        """获取复发预测证据"""
        try:
            predictions, probabilities = self.recurrence_model.predict(patient_df)
            
            return {
                "recurrence_risk": "高风险" if predictions[0] == 1 else "低风险",
                "recurrence_probability_2yr": float(probabilities[0]),
                "risk_factors": self._identify_recurrence_risk_factors(patient_df),
                "model_performance": {
                    "auc_score": getattr(self.recurrence_model, 'auc_score', None),
                    "model_type": getattr(self.recurrence_model, 'model_type', 'Unknown')
                }
            }
        except Exception as e:
            print(f"⚠️  复发预测失败: {e}")
            return {"error": str(e)}
    
    def _get_explainability_evidence(self, patient_df: pd.DataFrame) -> Dict:
        """获取可解释性证据"""
        try:
            shap_values = self.explainer.explain_prediction(patient_df)
            
            return {
                "top_positive_factors": shap_values.get("top_positive", []),
                "top_negative_factors": shap_values.get("top_negative", []),
                "feature_contributions": shap_values.get("feature_contributions", {}),
                "explanation_summary": shap_values.get("summary", "")
            }
        except Exception as e:
            print(f"⚠️  可解释性分析失败: {e}")
            return {"error": str(e)}
    
    def _estimate_uncertainty(self, patient_df: pd.DataFrame) -> Dict:
        """估计预测不确定度"""
        uncertainty = {
            "diagnostic_confidence": "中等",
            "survival_confidence": "中等",
            "data_quality_score": 0.8,
            "model_reliability": "良好",
            "limitations": [
                "模型基于历史数据训练，个体差异可能影响预测准确性",
                "影像和病理信息的主观性可能影响结果",
                "随访时间限制可能影响长期预测"
            ]
        }
        
        # 基于数据完整性评估不确定度
        missing_rate = patient_df.isnull().sum().sum() / (patient_df.shape[0] * patient_df.shape[1])
        if missing_rate > 0.2:
            uncertainty["data_quality_score"] = 0.6
            uncertainty["diagnostic_confidence"] = "低"
        elif missing_rate > 0.1:
            uncertainty["data_quality_score"] = 0.7
            uncertainty["diagnostic_confidence"] = "中低"
        
        return uncertainty
    
    def _generate_clinical_recommendations(self, evidence: Dict) -> Dict:
        """基于证据生成临床建议"""
        recommendations = {
            "immediate_actions": [],
            "additional_tests": [],
            "treatment_considerations": [],
            "follow_up_plan": [],
            "risk_mitigation": []
        }
        
        # 基于诊断预测的建议
        if "diagnostic_prediction" in evidence:
            diag = evidence["diagnostic_prediction"]
            if diag.get("probability", 0) > 0.7:
                recommendations["immediate_actions"].append("建议尽快完善影像学检查")
                recommendations["additional_tests"].append("增强CT或MRI进一步评估")
        
        # 基于生存预测的建议
        if "survival_prediction" in evidence:
            surv = evidence["survival_prediction"]
            if surv.get("risk_group") in ["高危", "中高危"]:
                recommendations["treatment_considerations"].append("考虑积极的多学科综合治疗")
                recommendations["follow_up_plan"].append("建议3个月内密切随访")
        
        # 基于复发预测的建议
        if "recurrence_prediction" in evidence:
            recur = evidence["recurrence_prediction"]
            if recur.get("recurrence_probability_2yr", 0) > 0.5:
                recommendations["risk_mitigation"].append("建议术后辅助治疗")
                recommendations["follow_up_plan"].append("加强术后监测，每3个月复查")
        
        return recommendations
    
    def _get_confidence_level(self, probability: float) -> str:
        """根据概率获取置信水平"""
        if probability > 0.9 or probability < 0.1:
            return "高"
        elif probability > 0.8 or probability < 0.2:
            return "中高"
        elif probability > 0.6 or probability < 0.4:
            return "中等"
        else:
            return "低"
    
    def _identify_recurrence_risk_factors(self, patient_df: pd.DataFrame) -> List[str]:
        """识别复发风险因素"""
        risk_factors = []
        
        # 检查高危因素
        if patient_df.get("AFP", [0])[0] > 400:
            risk_factors.append("AFP显著升高(>400)")
        
        if patient_df.get("tumor_size_cm", [0])[0] > 5:
            risk_factors.append("肿瘤直径>5cm")
        
        if patient_df.get("portal_vein_invasion", [0])[0] == 1:
            risk_factors.append("门静脉侵犯")
        
        if patient_df.get("lymph_node_metastasis", [0])[0] == 1:
            risk_factors.append("淋巴结转移")
        
        if patient_df.get("histologic_grade", [""])[0] == "低分化":
            risk_factors.append("病理低分化")
        
        return risk_factors
    
    def export_evidence_json(self, evidence: Dict, file_path: str) -> str:
        """导出证据包为JSON文件"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(evidence, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 证据包已导出: {file_path}")
            return file_path
        except Exception as e:
            print(f"❌ 证据包导出失败: {e}")
            return None
    
    def load_evidence_json(self, file_path: str) -> Dict:
        """从JSON文件加载证据包"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                evidence = json.load(f)
            
            print(f"✅ 证据包已加载: {file_path}")
            return evidence
        except Exception as e:
            print(f"❌ 证据包加载失败: {e}")
            return None


def create_evidence_template():
    """创建证据包模板"""
    template = {
        "patient_info": {
            "age": "患者年龄",
            "sex": "患者性别",
            "chief_complaint": "主诉",
            "key_labs": {
                "ALT": "ALT值",
                "AST": "AST值", 
                "AFP": "AFP值"
            },
            "imaging": "影像学描述",
            "comorbidities": {
                "hypertension": "是否高血压(0/1)",
                "diabetes": "是否糖尿病(0/1)"
            }
        },
        "diagnostic_prediction": {
            "prediction": "诊断预测结果",
            "probability": "预测概率",
            "confidence_level": "置信水平",
            "top_contributing_factors": "主要贡献因素",
            "model_performance": {
                "auc_score": "模型AUC得分",
                "model_type": "模型类型"
            }
        },
        "survival_prediction": {
            "median_survival_months": "中位生存时间(月)",
            "survival_probabilities": {
                "1_year": "1年生存率",
                "2_year": "2年生存率",
                "3_year": "3年生存率",
                "5_year": "5年生存率"
            },
            "risk_group": "风险分组",
            "risk_score": "风险评分",
            "model_performance": {
                "c_index": "C指数",
                "model_type": "模型类型"
            }
        },
        "recurrence_prediction": {
            "recurrence_risk": "复发风险等级",
            "recurrence_probability_2yr": "2年复发概率",
            "risk_factors": "复发危险因素",
            "model_performance": {
                "auc_score": "模型AUC得分",
                "model_type": "模型类型"
            }
        },
        "explainability": {
            "top_positive_factors": "正向影响因素",
            "top_negative_factors": "负向影响因素",
            "feature_contributions": "特征贡献度",
            "explanation_summary": "解释性总结"
        },
        "uncertainty": {
            "diagnostic_confidence": "诊断置信度",
            "survival_confidence": "生存预测置信度",
            "data_quality_score": "数据质量评分",
            "model_reliability": "模型可靠性",
            "limitations": "局限性说明"
        },
        "clinical_recommendations": {
            "immediate_actions": "立即行动建议",
            "additional_tests": "补充检查建议",
            "treatment_considerations": "治疗考虑",
            "follow_up_plan": "随访计划",
            "risk_mitigation": "风险缓解措施"
        }
    }
    
    return template


class EvidenceValidator:
    """证据包验证器"""
    
    @staticmethod
    def validate_evidence_bundle(evidence: Dict) -> Dict:
        """验证证据包完整性和有效性"""
        validation_report = {
            "is_valid": True,
            "warnings": [],
            "errors": [],
            "completeness_score": 0.0
        }
        
        required_sections = [
            "patient_info",
            "diagnostic_prediction",
            "survival_prediction",
            "clinical_recommendations"
        ]
        
        present_sections = 0
        for section in required_sections:
            if section in evidence:
                present_sections += 1
            else:
                validation_report["errors"].append(f"缺少必需部分: {section}")
                validation_report["is_valid"] = False
        
        validation_report["completeness_score"] = present_sections / len(required_sections)
        
        # 检查数据质量
        if "diagnostic_prediction" in evidence:
            diag = evidence["diagnostic_prediction"]
            if "probability" in diag:
                prob = diag["probability"]
                if not (0 <= prob <= 1):
                    validation_report["warnings"].append("诊断概率超出有效范围[0,1]")
        
        if "survival_prediction" in evidence:
            surv = evidence["survival_prediction"]
            if "median_survival_months" in surv:
                survival_time = surv["median_survival_months"]
                if survival_time <= 0:
                    validation_report["warnings"].append("预测生存时间为非正数")
        
        return validation_report


def create_sample_evidence_bundle():
    """创建示例证据包"""
    sample_evidence = {
        "patient_info": {
            "age": 55,
            "sex": "男",
            "chief_complaint": "右上腹疼痛3周，伴食欲减退",
            "key_labs": {
                "ALT": 56,
                "AST": 62,
                "AFP": 420,
                "albumin": 38
            },
            "imaging": "CT提示肝右叶占位，大小约3.5cm，边界不清，增强扫描不均匀强化",
            "comorbidities": {
                "hypertension": 1,
                "diabetes": 0
            }
        },
        "diagnostic_prediction": {
            "prediction": "阳性",
            "probability": 0.87,
            "confidence_level": "高",
            "top_contributing_factors": [
                {"feature": "AFP", "importance": 0.35},
                {"feature": "tumor_size_cm", "importance": 0.22},
                {"feature": "age", "importance": 0.18},
                {"feature": "ALT", "importance": 0.12},
                {"feature": "imaging_占位", "importance": 0.10}
            ],
            "model_performance": {
                "auc_score": 0.89,
                "model_type": "XGBoost"
            }
        },
        "survival_prediction": {
            "median_survival_months": 36.5,
            "survival_probabilities": {
                "1_year": 0.85,
                "2_year": 0.68,
                "3_year": 0.52,
                "5_year": 0.31
            },
            "risk_group": "中高危",
            "risk_score": 1.23,
            "model_performance": {
                "c_index": 0.72,
                "model_type": "Cox回归"
            }
        },
        "recurrence_prediction": {
            "recurrence_risk": "高风险",
            "recurrence_probability_2yr": 0.42,
            "risk_factors": [
                "AFP显著升高(>400)",
                "肿瘤直径>3cm",
                "影像提示边界不清"
            ],
            "model_performance": {
                "auc_score": 0.76,
                "model_type": "LightGBM"
            }
        },
        "explainability": {
            "top_positive_factors": [
                "AFP水平是最重要的风险因素",
                "肿瘤大小显著影响预后",
                "年龄因素需要考虑"
            ],
            "top_negative_factors": [
                "白蛋白水平相对正常",
                "无明确门静脉侵犯"
            ],
            "explanation_summary": "AFP显著升高和肿瘤大小是主要驱动因素，建议重点关注"
        },
        "uncertainty": {
            "diagnostic_confidence": "高",
            "survival_confidence": "中等",
            "data_quality_score": 0.85,
            "model_reliability": "良好",
            "limitations": [
                "模型基于回顾性数据，前瞻性验证有限",
                "个体化因素可能影响预测准确性",
                "中医证型信息缺失可能影响综合评估"
            ]
        },
        "clinical_recommendations": {
            "immediate_actions": [
                "建议完善增强MRI进一步评估肿瘤特征",
                "建议肝胆外科专科会诊"
            ],
            "additional_tests": [
                "乙肝病毒标志物检查",
                "肝储备功能评估(ICG-R15)",
                "胸部CT排除远处转移"
            ],
            "treatment_considerations": [
                "考虑新辅助治疗可能性",
                "评估手术切除可行性",
                "多学科团队讨论治疗方案"
            ],
            "follow_up_plan": [
                "术前每2周随访",
                "术后3个月内每月随访",
                "长期每3-6个月随访"
            ],
            "risk_mitigation": [
                "优化肝功能",
                "控制合并症",
                "营养支持"
            ]
        },
        "timestamp": datetime.now().isoformat(),
        "evidence_version": "1.0"
    }
    
    return sample_evidence
