"""
医疗AI科研模块
包含数据工程、机器学习模型、生存分析、可解释性等功能
"""

__version__ = "1.0.0"
__author__ = "Medical AI Research Team"

# 模块导入
from .data_engineering import DataProcessor, EDAAnalyzer
from .diagnostic_models import DiagnosticPredictor
from .survival_analysis import SurvivalAnalyzer
from .recurrence_prediction import RecurrencePredictor
from .explainability import ModelExplainer
from .evidence_bundle import EvidenceBuilder
from .research_prompts import ResearchPromptTemplates

__all__ = [
    'DataProcessor',
    'EDAAnalyzer', 
    'DiagnosticPredictor',
    'SurvivalAnalyzer',
    'RecurrencePredictor',
    'ModelExplainer',
    'EvidenceBuilder',
    'ResearchPromptTemplates'
]
