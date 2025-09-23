"""
科研场景LLM Prompt模板 - 专业的医疗科研报告生成
"""

from typing import Dict, Any
import json

class ResearchPromptTemplates:
    """科研场景的LLM Prompt模板集合"""
    
    @staticmethod
    def preoperative_assessment_prompt(evidence_bundle: Dict) -> str:
        """术前评估报告Prompt"""
        return f"""
你是一位资深的肝胆外科专家和临床研究员，同时精通中医辨证论治。请基于以下科学证据包，生成一份专业的术前评估报告，包含临床诊疗建议和科研分析。

**证据包数据：**
{json.dumps(evidence_bundle, ensure_ascii=False, indent=2)}

**请按以下结构生成报告：**

## 一、患者基础信息摘要
- 基本信息整理
- 主要症状和体征
- 关键实验室指标解读

## 二、AI模型预测分析
### 诊断预测模型结果
- 模型预测结论：{evidence_bundle.get('diagnostic_prediction', {}).get('prediction', '未知')}
- 预测概率：{evidence_bundle.get('diagnostic_prediction', {}).get('probability', 'N/A')}
- 模型性能：AUC = {evidence_bundle.get('diagnostic_prediction', {}).get('model_performance', {}).get('auc_score', 'N/A')}
- 主要贡献因素分析

### 生存预测模型结果  
- 预测中位生存时间：{evidence_bundle.get('survival_prediction', {}).get('median_survival_months', 'N/A')}月
- 风险分层：{evidence_bundle.get('survival_prediction', {}).get('risk_group', '未知')}
- 各时间点生存概率预测
- 模型C-index：{evidence_bundle.get('survival_prediction', {}).get('model_performance', {}).get('c_index', 'N/A')}

### 复发风险评估
- 2年复发概率：{evidence_bundle.get('recurrence_prediction', {}).get('recurrence_probability_2yr', 'N/A')}
- 主要风险因素识别
- 风险缓解策略

## 三、中西医结合诊疗方案
### 西医诊疗建议
- 诊断依据和分期评估
- 手术适应症评估
- 术前准备和优化措施
- 辅助治疗考虑

### 中医辨证论治
- 基于症状和体质的证型分析
- 中药方剂建议
- 针灸和其他中医疗法
- 术前调理方案

## 四、科研讨论与模型解释
### 模型性能评价
- 各模型的性能指标解读
- 预测结果的临床意义
- 模型局限性和不确定性分析

### 可解释性分析
- 关键特征对预测结果的贡献
- 临床变量的重要性排序
- 模型决策的生物学合理性

### 不确定性评估
- 预测置信度分析
- 数据质量对结果的影响
- 个体化差异的考虑

## 五、临床决策建议
### 立即行动计划
- 基于模型预测的紧急度评估
- 必要的补充检查
- 多学科会诊建议

### 治疗策略制定
- 个体化治疗方案
- 风险效益分析
- 预后改善措施

### 随访监测计划
- 基于风险分层的随访频率
- 关键监测指标
- 早期预警信号

## 六、科研价值与临床转化
### 模型应用价值
- 临床决策支持的意义
- 患者分层管理的优势
- 医疗资源优化配置

### 研究局限性
- 样本特征和代表性
- 模型泛化能力
- 外部验证需求

### 后续研究方向
- 模型改进建议
- 新变量纳入考虑
- 前瞻性验证计划

**重要声明：**
1. 本报告基于AI模型预测和科学分析，仅供临床参考
2. 最终诊疗决策应由主治医师结合临床经验做出
3. 模型预测存在不确定性，需要持续验证和改进
4. 中医治疗建议需要中医师根据具体情况调整

**模型版本信息：**
- 报告生成时间：{evidence_bundle.get('timestamp', '未知')}
- 证据包版本：{evidence_bundle.get('evidence_version', '1.0')}
"""

    @staticmethod
    def postoperative_followup_prompt(evidence_bundle: Dict, surgery_info: Dict) -> str:
        """术后随访报告Prompt"""
        return f"""
你是一位专业的肝胆外科医生和临床研究专家，精通术后随访管理和中西医结合康复。请基于术前预测模型和术后实际情况，生成综合随访报告。

**术前预测证据包：**
{json.dumps(evidence_bundle, ensure_ascii=False, indent=2)}

**手术信息：**
{json.dumps(surgery_info, ensure_ascii=False, indent=2)}

**请生成包含以下内容的术后随访报告：**

## 一、术前预测与术后对比分析
### 预测准确性评估
- 术前模型预测 vs 术后实际情况
- 预测偏差分析和原因探讨
- 模型校准效果评价

### 手术结果评估
- 手术成功率和并发症
- R0切除达成情况
- 病理结果与预测的一致性

## 二、当前康复状态评估
### 生存状态监测
- 当前生存状态与预测模型对比
- 生存曲线实际走向
- 风险分层准确性验证

### 复发监测
- 复发风险动态评估
- 影像学和肿瘤标志物变化
- 早期复发信号识别

## 三、中西医结合康复方案
### 西医康复治疗
- 术后辅助治疗评估
- 肝功能恢复监测
- 营养支持和体能康复

### 中医调理方案
- 术后体质辨识
- 中药调理方案
- 针灸康复治疗
- 饮食起居指导

## 四、预后预测更新
### 基于新数据的预测调整
- 结合术后病理的预后重新评估
- 个体化生存预测更新
- 复发风险重新分层

### 长期管理策略
- 个体化随访计划
- 预防性干预措施
- 生活质量改善建议

## 五、科研数据价值
### 模型验证贡献
- 为模型验证提供的数据价值
- 预测准确性的定量评估
- 模型改进方向建议

### 临床研究价值
- 个案的科研意义
- 可用于发表的数据点
- 多中心研究的贡献潜力

**免责声明：**
本报告结合AI预测模型和临床实际，仅供医疗参考。具体治疗方案需要主治医师综合判断。
"""

    @staticmethod
    def recurrence_risk_assessment_prompt(evidence_bundle: Dict, followup_data: Dict) -> str:
        """复发风险评估报告Prompt"""
        return f"""
你是肝胆外科和肿瘤学专家，精通复发转移的预测和管理。请基于AI模型预测和随访数据，生成专业的复发风险评估报告。

**AI预测证据包：**
{json.dumps(evidence_bundle, ensure_ascii=False, indent=2)}

**随访数据：**
{json.dumps(followup_data, ensure_ascii=False, indent=2)}

**请生成复发风险评估报告：**

## 一、复发风险量化评估
### AI模型预测结果
- 2年复发概率：{evidence_bundle.get('recurrence_prediction', {}).get('recurrence_probability_2yr', 'N/A')}
- 风险分层：{evidence_bundle.get('recurrence_prediction', {}).get('recurrence_risk', '未知')}
- 主要风险因素：{evidence_bundle.get('recurrence_prediction', {}).get('risk_factors', [])}

### 动态风险评估
- 基于最新随访数据的风险更新
- 肿瘤标志物趋势分析
- 影像学变化评估

## 二、复发模式预测
### 可能复发部位
- 肝内复发风险
- 远处转移风险
- 淋巴结转移风险

### 复发时间窗口
- 早期复发（<2年）风险
- 晚期复发（>2年）风险
- 个体化复发时间预测

## 三、监测策略优化
### 个体化监测方案
- 基于风险分层的监测频率
- 关键监测指标选择
- 成本效益优化

### 早期发现策略
- 敏感指标组合
- 影像学监测方案
- 生物标志物监测

## 四、预防干预措施
### 西医预防策略
- 辅助治疗调整
- 免疫治疗考虑
- 靶向治疗选择

### 中医预防调理
- 扶正固本方药
- 清热解毒治疗
- 活血化瘀方案
- 情志调护

## 五、科研贡献与模型优化
### 数据价值
- 为复发预测模型提供验证数据
- 模型校准和改进方向
- 新特征发现潜力

### 研究意义
- 个体化医疗的实践价值
- 精准医学的应用示例
- 中西医结合的科学证据

**临床建议优先级：**
1. 高优先级：{evidence_bundle.get('clinical_recommendations', {}).get('immediate_actions', [])}
2. 中优先级：{evidence_bundle.get('clinical_recommendations', {}).get('additional_tests', [])}
3. 长期计划：{evidence_bundle.get('clinical_recommendations', {}).get('follow_up_plan', [])}
"""

    @staticmethod
    def research_publication_prompt(evidence_bundle: Dict, cohort_data: Dict) -> str:
        """科研发表报告Prompt"""
        return f"""
你是医学统计学专家和临床研究员，请基于AI模型结果和队列数据，生成适合学术发表的研究报告摘要。

**模型证据包：**
{json.dumps(evidence_bundle, ensure_ascii=False, indent=2)}

**队列数据摘要：**
{json.dumps(cohort_data, ensure_ascii=False, indent=2)}

**请生成学术研究报告：**

## Abstract (中英文摘要)

### Background (背景)
- 研究问题的临床重要性
- 现有预测模型的局限性
- 本研究的创新点

### Methods (方法)
- 队列设计和样本量
- 机器学习模型选择和训练
- 统计分析方法
- 验证策略

### Results (结果)
- 模型性能指标
- 关键发现和统计显著性
- 预测准确性评估

### Conclusions (结论)
- 主要发现的临床意义
- 模型的应用价值
- 研究局限性

## Introduction (引言)
### 研究背景
- 疾病流行病学现状
- 预测模型的临床需求
- 人工智能在医疗中的应用

### 研究目标
- 主要研究终点
- 次要研究终点
- 假设验证

## Methods (方法学)
### 研究设计
- 队列研究设计
- 纳入排除标准
- 伦理审查情况

### 数据收集
- 变量定义和测量
- 质量控制措施
- 随访程序

### 统计分析
- 描述性统计
- 生存分析方法
- 机器学习算法
- 模型验证策略

## Results (结果)
### 基线特征
- 患者人口学特征
- 临床特征分布
- 随访完整性

### 模型性能
- 诊断模型：AUC = {evidence_bundle.get('diagnostic_prediction', {}).get('model_performance', {}).get('auc_score', 'N/A')}
- 生存模型：C-index = {evidence_bundle.get('survival_prediction', {}).get('model_performance', {}).get('c_index', 'N/A')}
- 复发模型：AUC = {evidence_bundle.get('recurrence_prediction', {}).get('model_performance', {}).get('auc_score', 'N/A')}

### 特征重要性
- 关键预测因子识别
- 临床变量的贡献度
- 生物学意义解释

### 模型验证
- 内部验证结果
- 校准曲线分析
- 临床净效益评估

## Discussion (讨论)
### 主要发现
- 与既往研究的比较
- 临床意义阐述
- 机制探讨

### 临床应用
- 个体化治疗的指导价值
- 临床决策支持
- 医疗资源优化

### 研究局限性
- 样本局限性
- 模型局限性
- 外部验证需求

### 未来方向
- 模型改进策略
- 多中心验证计划
- 前瞻性研究设计

## Conclusion (结论)
- 研究的主要贡献
- 临床应用前景
- 科研价值总结

**统计学声明：**
所有统计分析使用Python科学计算栈完成，P<0.05为统计学显著。模型性能使用交叉验证评估，结果具有统计学可靠性。

**利益冲突声明：**
作者声明无利益冲突。

**数据可用性：**
去标识化数据可根据合理要求提供，需符合伦理和隐私保护要求。
"""

    @staticmethod
    def tcm_integration_prompt(evidence_bundle: Dict) -> str:
        """中西医结合深度分析Prompt"""
        return f"""
你是中西医结合领域的资深专家，精通现代医学循证研究和传统中医理论。请基于AI模型预测结果，深度分析中西医结合治疗方案。

**AI模型证据包：**
{json.dumps(evidence_bundle, ensure_ascii=False, indent=2)}

**请生成中西医结合深度分析报告：**

## 一、现代医学证据分析
### 循证医学证据
- AI模型预测的统计学意义
- 生存分析的临床价值
- 复发预测的指导意义

### 分子生物学机制
- 相关生物标志物解读
- 肿瘤生物学行为预测
- 治疗靶点识别

## 二、中医理论阐释
### 证候辨识
- 基于症状的证型分析
- 体质辨识和分类
- 病机演变规律

### 中医病因病机
- 正虚邪实的动态平衡
- 气血痰瘀的相互关系
- 脏腑功能失调分析

### 治则治法
- 扶正祛邪的治疗原则
- 个体化治法选择
- 分期论治策略

## 三、中西医结合治疗方案
### 协同治疗策略
- 西医治疗的中医理论支撑
- 中医治疗的现代医学验证
- 优势互补的治疗模式

### 个体化方案设计
- 基于AI预测的中医干预
- 风险分层的中药选择
- 生存预测指导的调理方案

### 疗效评估体系
- 中西医结合疗效指标
- 生活质量评估
- 长期预后监测

## 四、科研创新点
### 方法学创新
- AI模型与中医辨证的结合
- 量化分析中医证候
- 个体化治疗的科学化

### 理论创新
- 传统理论的现代阐释
- 中西医结合的机制研究
- 精准医学的中医应用

## 五、临床应用指导
### 诊疗流程优化
- 中西医结合的标准化流程
- 多学科协作模式
- 质量控制体系

### 医生培训建议
- 中西医结合能力培养
- AI工具使用培训
- 循证医学思维建立

## 六、研究展望
### 短期目标
- 模型验证和优化
- 临床应用推广
- 疗效数据收集

### 长期愿景
- 中西医结合的标准化
- 个体化医疗的实现
- 智能医疗的发展

**中医方药建议：**
基于当前证据，建议中医师考虑以下治疗思路：
- 扶正：{self._get_tcm_strengthening_herbs(evidence_bundle)}
- 祛邪：{self._get_tcm_pathogen_expelling_herbs(evidence_bundle)}
- 调理：{self._get_tcm_regulating_herbs(evidence_bundle)}

**注意事项：**
1. 中医治疗需要专业中医师个体化调整
2. 中西医结合治疗需要密切监测
3. 药物相互作用需要特别注意
4. 定期评估和方案调整必不可少
"""

    @staticmethod
    def model_explanation_prompt(evidence_bundle: Dict, shap_values: Dict) -> str:
        """模型解释性分析Prompt"""
        return f"""
你是医学AI和生物统计学专家，请对机器学习模型的预测结果进行深度解释和临床转化。

**模型预测证据：**
{json.dumps(evidence_bundle, ensure_ascii=False, indent=2)}

**SHAP解释性分析：**
{json.dumps(shap_values, ensure_ascii=False, indent=2)}

**请生成模型解释性分析报告：**

## 一、模型决策机制解析
### 关键特征贡献分析
- 正向贡献因子及其临床意义
- 负向贡献因子及其保护作用
- 特征交互效应分析

### 决策边界解释
- 模型分类/预测的临界点
- 不同特征值对结果的影响
- 敏感性分析结果

## 二、临床变量重要性排序
### 实验室指标
- 各项检验指标的预测价值
- 异常值的临床意义
- 动态变化的预测价值

### 影像学特征
- 关键影像特征识别
- 定量参数的预测价值
- 影像组学的应用潜力

### 临床症状
- 症状严重程度的量化
- 症状组合的预测价值
- 主观症状的客观化

## 三、生物学合理性验证
### 医学机制解释
- 预测因子的病理生理基础
- 生物标志物的分子机制
- 疾病进展的生物学逻辑

### 临床经验验证
- 模型发现与临床经验的一致性
- 新发现的临床验证需求
- 经验知识的量化验证

## 四、个体化解释
### 患者特异性分析
- 该患者的独特风险因素
- 个体化干预靶点
- 精准治疗的指导意义

### 风险因素可调控性
- 可干预的风险因素
- 不可改变的风险因素
- 干预优先级排序

## 五、模型局限性分析
### 数据局限性
- 训练数据的代表性
- 缺失变量的影响
- 数据质量对预测的影响

### 模型局限性
- 算法假设和约束
- 泛化能力评估
- 预测不确定性量化

### 临床应用局限性
- 适用人群范围
- 使用场景限制
- 医生经验的不可替代性

## 六、改进建议
### 模型优化方向
- 新特征纳入建议
- 算法改进策略
- 数据质量提升

### 临床验证需求
- 前瞻性验证设计
- 多中心验证计划
- 真实世界数据收集

**可解释性总结：**
基于SHAP分析，{evidence_bundle.get('explainability', {}).get('explanation_summary', '模型决策主要基于关键临床特征的综合评估')}

**临床应用建议：**
1. 将模型预测作为临床决策的重要参考
2. 结合医生经验进行综合判断
3. 持续收集数据优化模型性能
4. 建立模型应用的质量控制体系
"""

    @staticmethod
    def _get_tcm_strengthening_herbs(evidence_bundle: Dict) -> str:
        """根据证据推荐扶正中药"""
        # 简化的中医药推荐逻辑
        patient_info = evidence_bundle.get('patient_info', {})
        age = patient_info.get('age', 50)
        
        if age > 65:
            return "黄芪、党参、白术、茯苓等益气健脾"
        elif patient_info.get('key_labs', {}).get('albumin', 40) < 35:
            return "人参、黄精、山药、大枣等补气养血"
        else:
            return "太子参、白术、茯苓、甘草等平补脾胃"
    
    @staticmethod
    def _get_tcm_pathogen_expelling_herbs(evidence_bundle: Dict) -> str:
        """根据证据推荐祛邪中药"""
        recurrence_risk = evidence_bundle.get('recurrence_prediction', {}).get('recurrence_risk', '')
        
        if '高风险' in recurrence_risk:
            return "半枝莲、白花蛇舌草、龙葵、藤梨根等清热解毒"
        else:
            return "郁金、柴胡、香附、青皮等疏肝理气"
    
    @staticmethod
    def _get_tcm_regulating_herbs(evidence_bundle: Dict) -> str:
        """根据证据推荐调理中药"""
        return "丹参、红花、当归、川芎等活血化瘀，调和气血"


class PromptManager:
    """Prompt管理器"""
    
    def __init__(self):
        self.templates = ResearchPromptTemplates()
        
    def generate_research_report(self, evidence_bundle: Dict, report_type: str, 
                               additional_data: Dict = None) -> str:
        """生成科研报告"""
        if report_type == "preoperative":
            return self.templates.preoperative_assessment_prompt(evidence_bundle)
        elif report_type == "postoperative":
            return self.templates.postoperative_followup_prompt(evidence_bundle, additional_data or {})
        elif report_type == "recurrence":
            return self.templates.recurrence_risk_assessment_prompt(evidence_bundle, additional_data or {})
        elif report_type == "publication":
            return self.templates.research_publication_prompt(evidence_bundle, additional_data or {})
        elif report_type == "tcm_integration":
            return self.templates.tcm_integration_prompt(evidence_bundle)
        elif report_type == "model_explanation":
            return self.templates.model_explanation_prompt(evidence_bundle, additional_data or {})
        else:
            raise ValueError(f"不支持的报告类型: {report_type}")
    
    def get_available_report_types(self) -> List[str]:
        """获取可用的报告类型"""
        return [
            "preoperative",      # 术前评估
            "postoperative",     # 术后随访  
            "recurrence",        # 复发风险评估
            "publication",       # 科研发表
            "tcm_integration",   # 中西医结合
            "model_explanation"  # 模型解释
        ]
    
    def validate_prompt_data(self, evidence_bundle: Dict, report_type: str) -> Dict:
        """验证Prompt数据完整性"""
        validation_result = {
            "is_valid": True,
            "missing_fields": [],
            "warnings": []
        }
        
        required_fields = {
            "preoperative": ["patient_info", "diagnostic_prediction"],
            "postoperative": ["patient_info", "survival_prediction"],
            "recurrence": ["recurrence_prediction"],
            "publication": ["diagnostic_prediction", "survival_prediction"],
            "tcm_integration": ["patient_info"],
            "model_explanation": ["explainability"]
        }
        
        if report_type in required_fields:
            for field in required_fields[report_type]:
                if field not in evidence_bundle:
                    validation_result["missing_fields"].append(field)
                    validation_result["is_valid"] = False
        
        # 检查数据质量
        if "uncertainty" in evidence_bundle:
            uncertainty = evidence_bundle["uncertainty"]
            if uncertainty.get("data_quality_score", 1.0) < 0.7:
                validation_result["warnings"].append("数据质量较低，可能影响报告准确性")
        
        return validation_result
