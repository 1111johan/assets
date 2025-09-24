from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
import openai
import sqlite3
import json
from datetime import datetime
import os
import requests
from pdf_generator import generate_medical_report_pdf
import socket

# 初始化 FastAPI 应用
app = FastAPI(title="术前病情预测 & 中西医结合诊疗报告生成系统", version="1.0.0")

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置 AI API - 从配置文件读取
from config import config
DASHSCOPE_API_KEY = config.get_api_key("dashscope")
OPENAI_API_KEY = config.get_api_key("openai")

# 模型训练服务配置 - 从配置文件读取
MODEL_TRAINING_URL = config.MODEL_TRAINING_URL
# 备用端口配置（如果7003不可用，可以尝试其他端口）
MODEL_TRAINING_ALTERNATIVE_PORTS = [7003, 8080, 8000, 3000, 5000]

def check_port_availability(host, port, timeout=3):
    """检查指定主机和端口是否可用"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except:
        return False

def find_available_model_training_port(host="47.108.190.171", ports=None):
    """查找可用的模型训练服务端口"""
    if ports is None:
        ports = MODEL_TRAINING_ALTERNATIVE_PORTS
    
    for port in ports:
        if check_port_availability(host, port):
            return f"http://{host}:{port}"
    return None

# 初始化阿里云通义千问客户端
from openai import OpenAI
dashscope_client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 保持原有OpenAI配置兼容性
openai.api_key = OPENAI_API_KEY

# 病人信息模型
class PatientInfo(BaseModel):
    name: str
    age: int
    sex: str
    chief_complaint: str
    history: str
    labs: Dict[str, Any]
    imaging: str
    additional_notes: Optional[str] = ""

# 报告生成请求模型
class ReportRequest(BaseModel):
    patient: PatientInfo
    report_type: str = "comprehensive"  # comprehensive, western, tcm

# AI对话请求模型
class ChatRequest(BaseModel):
    message: str
    conversation_history: list = []

# AI整理报告请求模型
class ReportOptimizeRequest(BaseModel):
    original_report: str
    optimize_type: str = "format"  # format, simplify, enhance, summary

# 科研分析请求模型
class ResearchAnalysisRequest(BaseModel):
    patient_data: dict
    analysis_type: str = "comprehensive"  # comprehensive, diagnostic, survival, recurrence
    include_tcm: bool = True

# 批量数据分析请求模型
class BatchAnalysisRequest(BaseModel):
    data_file_path: str
    analysis_types: list = ["diagnostic", "survival", "recurrence"]
    output_format: str = "json"  # json, csv, excel

# 数据库初始化
def init_database():
    conn = sqlite3.connect('medical_reports.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            sex TEXT NOT NULL,
            chief_complaint TEXT NOT NULL,
            history TEXT,
            labs TEXT,
            imaging TEXT,
            additional_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            report_content TEXT NOT NULL,
            report_type TEXT DEFAULT 'comprehensive',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    conn.commit()
    conn.close()

# 保存病人信息到数据库
def save_patient(patient: PatientInfo) -> int:
    conn = sqlite3.connect('medical_reports.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO patients (name, age, sex, chief_complaint, history, labs, imaging, additional_notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        patient.name, patient.age, patient.sex, patient.chief_complaint,
        patient.history, json.dumps(patient.labs), patient.imaging, patient.additional_notes
    ))
    patient_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return patient_id

# 保存报告到数据库
def save_report(patient_id: int, report_content: str, report_type: str):
    conn = sqlite3.connect('medical_reports.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO reports (patient_id, report_content, report_type)
        VALUES (?, ?, ?)
    ''', (patient_id, report_content, report_type))
    conn.commit()
    conn.close()

# 生成中西医结合诊疗报告的 Prompt
def create_medical_prompt(patient: PatientInfo) -> str:
    return f"""
你是一个经验丰富的肝胆外科医生，同时精通中医辨证论治理论。请根据以下病人信息生成一份完整的中西医结合术前诊疗报告。

**病人基本信息：**
- 姓名：{patient.name}
- 年龄：{patient.age}岁
- 性别：{patient.sex}
- 主诉：{patient.chief_complaint}
- 既往病史：{patient.history}
- 实验室检查：{json.dumps(patient.labs, ensure_ascii=False, indent=2)}
- 影像学检查：{patient.imaging}
- 其他备注：{patient.additional_notes or '无'}

**请按以下结构生成报告：**

## 一、疾病分析
### 西医诊断分析
- 可能诊断及依据
- 疾病分期/分级
- 病理生理机制

### 中医辨证分析
- 证型分析
- 病机分析
- 体质辨识

## 二、术前风险评估
- 年龄因素评估
- 实验室指标分析
- 影像学特征评估
- 既往病史影响
- 综合风险等级

## 三、推荐检查项目
- 必要影像学检查
- 血液生化指标
- 肝功能评估
- 其他辅助检查

## 四、治疗方案
### 西医治疗方案
- 手术方式选择
- 术前准备措施
- 药物治疗方案
- 围手术期管理

### 中医辅助治疗
- 辨证论治方案
- 中药方剂推荐
- 针灸/推拿辅助
- 饮食调理建议

## 五、注意事项
- 术前注意事项
- 生活管理建议
- 随访计划
- 紧急情况处理

**报告要求：**
1. 专业、准确、条理清晰
2. 中西医理论结合，相互补充
3. 可直接供临床医生参考使用
4. 语言简洁明了，避免过度专业术语
"""

@app.on_event("startup")
async def startup_event():
    init_database()

@app.get("/")
async def root():
    return {"message": "术前病情预测 & 中西医结合诊疗报告生成系统 API"}

@app.post("/generate_report")
async def generate_report(request: ReportRequest):
    try:
        # 保存病人信息
        patient_id = save_patient(request.patient)
        
        # 创建医疗报告 Prompt
        prompt = create_medical_prompt(request.patient)
        
        # 调用阿里云通义千问 API
        response = dashscope_client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "你是一个专业的医疗AI助手，专门生成中西医结合的诊疗报告。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=3000
        )
        
        report_content = response.choices[0].message.content
        
        # 保存报告
        save_report(patient_id, report_content, request.report_type)
        
        return {
            "success": True,
            "patient_id": patient_id,
            "report": report_content,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成报告时发生错误: {str(e)}")

@app.get("/patients")
async def get_patients():
    conn = sqlite3.connect('medical_reports.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.*, r.report_content, r.created_at as report_created_at
        FROM patients p
        LEFT JOIN reports r ON p.id = r.patient_id
        ORDER BY p.created_at DESC
    ''')
    patients = cursor.fetchall()
    conn.close()
    
    result = []
    for patient in patients:
        result.append({
            "id": patient[0],
            "name": patient[1],
            "age": patient[2],
            "sex": patient[3],
            "chief_complaint": patient[4],
            "history": patient[5],
            "labs": json.loads(patient[6]) if patient[6] else {},
            "imaging": patient[7],
            "additional_notes": patient[8],
            "created_at": patient[9],
            "latest_report": patient[10] if patient[10] else None,
            "report_created_at": patient[11] if patient[11] else None
        })
    
    return {"patients": result}

@app.get("/patient/{patient_id}")
async def get_patient(patient_id: int):
    conn = sqlite3.connect('medical_reports.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
    patient = cursor.fetchone()
    
    if not patient:
        conn.close()
        raise HTTPException(status_code=404, detail="病人信息未找到")
    
    cursor.execute('SELECT * FROM reports WHERE patient_id = ? ORDER BY created_at DESC', (patient_id,))
    reports = cursor.fetchall()
    conn.close()
    
    return {
        "patient": {
            "id": patient[0],
            "name": patient[1],
            "age": patient[2],
            "sex": patient[3],
            "chief_complaint": patient[4],
            "history": patient[5],
            "labs": json.loads(patient[6]) if patient[6] else {},
            "imaging": patient[7],
            "additional_notes": patient[8],
            "created_at": patient[9]
        },
        "reports": [
            {
                "id": report[0],
                "content": report[2],
                "type": report[3],
                "created_at": report[4]
            } for report in reports
        ]
    }

@app.delete("/patient/{patient_id}")
async def delete_patient(patient_id: int):
    """删除患者记录"""
    conn = sqlite3.connect('medical_reports.db')
    cursor = conn.cursor()
    
    try:
        # 检查患者是否存在
        cursor.execute('SELECT name FROM patients WHERE id = ?', (patient_id,))
        patient = cursor.fetchone()
        
        if not patient:
            conn.close()
            raise HTTPException(status_code=404, detail="患者记录未找到")
        
        # 删除相关报告
        cursor.execute('DELETE FROM reports WHERE patient_id = ?', (patient_id,))
        
        # 删除患者记录
        cursor.execute('DELETE FROM patients WHERE id = ?', (patient_id,))
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": f"患者 {patient[0]} 的记录已删除",
            "deleted_id": patient_id
        }
        
    except Exception as e:
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=500, detail=f"删除患者记录时发生错误: {str(e)}")

@app.delete("/patients/all")
async def delete_all_patients():
    """删除所有患者记录"""
    conn = sqlite3.connect('medical_reports.db')
    cursor = conn.cursor()
    
    try:
        # 获取删除前的记录数
        cursor.execute('SELECT COUNT(*) FROM patients')
        patient_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM reports')
        report_count = cursor.fetchone()[0]
        
        # 删除所有报告
        cursor.execute('DELETE FROM reports')
        
        # 删除所有患者
        cursor.execute('DELETE FROM patients')
        
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": f"已删除所有记录：{patient_count} 个患者，{report_count} 个报告",
            "deleted_patients": patient_count,
            "deleted_reports": report_count
        }
        
    except Exception as e:
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=500, detail=f"删除所有记录时发生错误: {str(e)}")

@app.post("/generate_pdf/{patient_id}")
async def generate_pdf_report(patient_id: int):
    """生成PDF格式的诊疗报告"""
    try:
        # 获取病人信息和最新报告
        conn = sqlite3.connect('medical_reports.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
        patient = cursor.fetchone()
        
        if not patient:
            conn.close()
            raise HTTPException(status_code=404, detail="病人信息未找到")
        
        cursor.execute('SELECT * FROM reports WHERE patient_id = ? ORDER BY created_at DESC LIMIT 1', (patient_id,))
        report = cursor.fetchone()
        conn.close()
        
        if not report:
            raise HTTPException(status_code=404, detail="该病人暂无诊疗报告")
        
        # 构建病人数据
        patient_data = {
            "id": patient[0],
            "name": patient[1],
            "age": patient[2],
            "sex": patient[3],
            "chief_complaint": patient[4],
            "history": patient[5],
            "labs": json.loads(patient[6]) if patient[6] else {},
            "imaging": patient[7],
            "additional_notes": patient[8]
        }
        
        # 生成PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"诊疗报告_{patient_data['name']}_{timestamp}.pdf"
        pdf_path = f"reports/{pdf_filename}"
        
        # 确保reports目录存在
        os.makedirs("reports", exist_ok=True)
        
        generate_medical_report_pdf(patient_data, report[2], pdf_path)
        
        return {
            "success": True,
            "pdf_path": pdf_path,
            "filename": pdf_filename,
            "message": "PDF报告生成成功"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成PDF报告时发生错误: {str(e)}")

@app.get("/download_pdf/{filename}")
async def download_pdf(filename: str):
    """下载PDF文件"""
    import os
    from fastapi.responses import FileResponse
    
    pdf_path = f"reports/{filename}"
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF文件未找到")
    
    return FileResponse(
        path=pdf_path,
        filename=filename,
        media_type='application/pdf'
    )

@app.post("/chat")
async def ai_chat(request: ChatRequest):
    """AI对话功能"""
    try:
        # 构建对话历史
        messages = [
            {"role": "system", "content": "你是一个专业的医疗AI助手，可以回答医疗相关问题，提供医学建议，但请注意提醒用户这些建议仅供参考，不能替代专业医生的诊断。"}
        ]
        
        # 添加历史对话
        for msg in request.conversation_history:
            messages.append(msg)
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": request.message})
        
        # 调用阿里云通义千问 API
        response = dashscope_client.chat.completions.create(
            model="qwen-plus",
            messages=messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        ai_response = response.choices[0].message.content
        
        return {
            "success": True,
            "response": ai_response,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI对话时发生错误: {str(e)}")

@app.post("/optimize_report")
async def optimize_report(request: ReportOptimizeRequest):
    """AI整理报告功能"""
    try:
        # 根据优化类型创建不同的prompt
        optimize_prompts = {
            "format": "请帮我重新格式化这份医疗报告，使其更加规范、清晰、易读。保持所有医学内容不变，只优化格式和结构：",
            "simplify": "请帮我简化这份医疗报告，用更通俗易懂的语言解释医学术语，但保持准确性：",
            "enhance": "请帮我完善这份医疗报告，补充可能遗漏的重要信息，增加更详细的分析和建议：",
            "summary": "请帮我总结这份医疗报告的核心要点，提取最重要的诊断结论和治疗建议："
        }
        
        prompt = optimize_prompts.get(request.optimize_type, optimize_prompts["format"])
        full_prompt = f"{prompt}\n\n原始报告：\n{request.original_report}"
        
        # 调用阿里云通义千问 API
        response = dashscope_client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "你是一个专业的医疗报告整理专家，擅长优化医疗报告的格式、内容和可读性。"},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.3,
            max_tokens=3000
        )
        
        optimized_report = response.choices[0].message.content
        
        return {
            "success": True,
            "original_report": request.original_report,
            "optimized_report": optimized_report,
            "optimize_type": request.optimize_type,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"报告整理时发生错误: {str(e)}")

@app.post("/analyze_symptoms")
async def analyze_symptoms(symptoms: dict):
    """症状分析功能"""
    try:
        symptoms_text = ", ".join([f"{k}: {v}" for k, v in symptoms.items()])
        prompt = f"""
        请作为专业医生分析以下症状，提供初步的医学建议：
        
        症状描述：{symptoms_text}
        
        请从以下几个方面进行分析：
        1. 可能的疾病诊断
        2. 建议的检查项目
        3. 注意事项
        4. 是否需要紧急就医
        
        请注意：此分析仅供参考，不能替代专业医生的诊断，如有疑问请及时就医。
        """
        
        response = dashscope_client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "你是一个专业的医疗AI助手，提供症状分析和医学建议。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        analysis = response.choices[0].message.content
        
        return {
            "success": True,
            "symptoms": symptoms,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"症状分析时发生错误: {str(e)}")

@app.post("/research/generate_evidence_bundle")
async def generate_evidence_bundle(request: ResearchAnalysisRequest):
    """生成科研证据包"""
    try:
        # 创建示例证据包（简化版）
        evidence = create_sample_evidence_bundle_simple(request.patient_data)
        
        # 生成科研报告prompt
        research_prompt = create_research_prompt(evidence, request.analysis_type)
        
        # 调用LLM生成科研报告
        response = dashscope_client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "你是一个专业的医疗AI研究专家，精通临床科研和中西医结合。"},
                {"role": "user", "content": research_prompt}
            ],
            temperature=0.2,
            max_tokens=4000
        )
        
        research_report = response.choices[0].message.content
        
        return {
            "success": True,
            "evidence_bundle": evidence,
            "research_report": research_report,
            "analysis_type": request.analysis_type,
            "include_tcm": request.include_tcm,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"科研分析时发生错误: {str(e)}")

def create_sample_evidence_bundle_simple(patient_data: dict):
    """创建简化的示例证据包"""
    return {
        "patient_info": {
            "age": patient_data.get("age", 55),
            "sex": patient_data.get("sex", "男"),
            "chief_complaint": "右上腹疼痛3周，伴食欲减退",
            "key_labs": {
                "ALT": patient_data.get("ALT", 56),
                "AST": patient_data.get("AST", 62),
                "AFP": patient_data.get("AFP", 420)
            },
            "imaging": "CT提示肝右叶占位，大小约3.5cm，边界不清"
        },
        "diagnostic_prediction": {
            "prediction": "阳性",
            "probability": 0.87,
            "confidence_level": "高",
            "top_contributing_factors": [
                {"feature": "AFP", "importance": 0.35},
                {"feature": "tumor_size_cm", "importance": 0.22},
                {"feature": "age", "importance": 0.18}
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
            ]
        },
        "clinical_recommendations": {
            "immediate_actions": [
                "建议完善增强MRI进一步评估",
                "建议肝胆外科专科会诊"
            ],
            "additional_tests": [
                "乙肝病毒标志物检查",
                "肝储备功能评估",
                "胸部CT排除远处转移"
            ]
        },
        "timestamp": datetime.now().isoformat()
    }

def create_research_prompt(evidence: dict, analysis_type: str):
    """创建科研分析prompt"""
    if analysis_type == "comprehensive":
        return f"""
你是一位资深的肝胆外科专家和临床研究员，同时精通中医辨证论治。请基于以下科学证据包，生成一份专业的术前评估报告，包含临床诊疗建议和科研分析。

**证据包数据：**
{json.dumps(evidence, ensure_ascii=False, indent=2)}

**请按以下结构生成报告：**

## 一、患者基础信息与AI模型预测摘要
- 基本信息：年龄{evidence['patient_info']['age']}岁，{evidence['patient_info']['sex']}性
- 主诉：{evidence['patient_info']['chief_complaint']}
- 关键指标：AFP {evidence['patient_info']['key_labs']['AFP']} ng/mL
- AI诊断预测：{evidence['diagnostic_prediction']['prediction']}（概率：{evidence['diagnostic_prediction']['probability']:.2%}）
- 生存预测：中位生存时间{evidence['survival_prediction']['median_survival_months']}月，风险分层{evidence['survival_prediction']['risk_group']}
- 复发风险：{evidence['recurrence_prediction']['recurrence_risk']}，2年复发概率{evidence['recurrence_prediction']['recurrence_probability_2yr']:.2%}

## 二、科学证据分析
### 机器学习模型性能
- 诊断模型AUC: {evidence['diagnostic_prediction']['model_performance']['auc_score']}
- 生存模型C-index: {evidence['survival_prediction']['model_performance']['c_index']}
- 主要预测因子：AFP、肿瘤大小、年龄

### 循证医学证据
- 基于大样本数据训练的AI模型预测
- 多维度风险评估和分层
- 量化的预后预测指标

## 三、中西医结合诊疗方案
### 西医诊疗建议
- 诊断：基于AI预测和临床表现，高度怀疑原发性肝癌
- 分期评估：建议完善影像学检查明确分期
- 治疗策略：多学科团队讨论制定个体化治疗方案

### 中医辨证论治
- 证型分析：肝郁脾虚，痰瘀互结
- 治法：疏肝健脾，化痰散结
- 方药建议：逍遥散合六君子汤加减
- 调护：情志调畅，饮食清淡

## 四、临床决策建议
### 立即行动（基于AI预测）
{chr(10).join([f"- {action}" for action in evidence['clinical_recommendations']['immediate_actions']])}

### 补充检查
{chr(10).join([f"- {test}" for test in evidence['clinical_recommendations']['additional_tests']])}

### 风险管理
- 基于高复发风险预测，建议积极的综合治疗
- 制定个体化随访监测方案
- 考虑术后辅助治疗

## 五、科研价值与局限性
### 模型应用价值
- 提供量化的风险评估工具
- 支持个体化医疗决策
- 优化医疗资源配置

### 研究局限性
- 模型基于回顾性数据，需前瞻性验证
- 个体差异可能影响预测准确性
- 需要持续的模型更新和校准

**重要声明：**
本报告基于AI模型预测和科学分析，仅供临床参考。最终诊疗决策应由主治医师结合临床经验做出。
"""
    else:
        return f"""
请基于以下医疗AI证据包，生成专业的{analysis_type}分析报告：

{json.dumps(evidence, ensure_ascii=False, indent=2)}

请提供专业的医学分析和建议。
"""

@app.post("/research/train_diagnostic_model")
async def train_diagnostic_model(file_path: str, target_column: str, model_type: str = "xgboost"):
    """训练诊断模型"""
    try:
        from research.diagnostic_models import create_diagnostic_pipeline
        
        # 创建诊断模型训练流水线
        results = create_diagnostic_pipeline(file_path, target_column, model_type)
        
        if results is None:
            raise HTTPException(status_code=400, detail="模型训练失败")
        
        return {
            "success": True,
            "model_type": model_type,
            "target_column": target_column,
            "auc_score": results['results']['auc_score'],
            "model_path": results['model_path'],
            "feature_importance": results['feature_importance'].head(10).to_dict('records') if results['feature_importance'] is not None else [],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"诊断模型训练时发生错误: {str(e)}")

@app.post("/research/train_survival_model")
async def train_survival_model(file_path: str, duration_col: str = "survival_months", 
                              event_col: str = "death_event"):
    """训练生存分析模型"""
    try:
        from research.survival_analysis import create_survival_pipeline
        
        # 创建生存分析流水线
        results = create_survival_pipeline(file_path, duration_col, event_col)
        
        if results is None:
            raise HTTPException(status_code=400, detail="生存模型训练失败")
        
        return {
            "success": True,
            "duration_column": duration_col,
            "event_column": event_col,
            "c_index": results['validation_results']['test_c_index'],
            "model_path": results['model_path'],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生存模型训练时发生错误: {str(e)}")

@app.post("/research/create_sample_data")
async def create_sample_research_data(n_patients: int = 500):
    """创建示例科研数据集"""
    try:
        from research.data_engineering import create_sample_dataset
        
        # 创建示例数据
        file_path = f"research_data/sample_medical_data_{n_patients}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        # 确保目录存在
        import os
        os.makedirs("research_data", exist_ok=True)
        
        df = create_sample_dataset(n_patients, file_path)
        
        return {
            "success": True,
            "file_path": file_path,
            "n_patients": n_patients,
            "columns": df.columns.tolist(),
            "shape": df.shape,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建示例数据时发生错误: {str(e)}")

@app.get("/research/models")
async def list_research_models():
    """列出所有科研模型"""
    try:
        import os
        import glob
        
        models_dir = "models"
        if not os.path.exists(models_dir):
            return {"models": []}
        
        model_files = glob.glob(os.path.join(models_dir, "*.pkl"))
        
        models_info = []
        for model_file in model_files:
            file_info = {
                "file_name": os.path.basename(model_file),
                "file_path": model_file,
                "file_size": os.path.getsize(model_file),
                "modified_time": datetime.fromtimestamp(os.path.getmtime(model_file)).isoformat()
            }
            
            # 尝试加载模型信息
            try:
                import joblib
                model_data = joblib.load(model_file)
                if isinstance(model_data, dict):
                    file_info.update({
                        "model_type": model_data.get("model_type", "unknown"),
                        "training_results": model_data.get("training_results", {})
                    })
            except:
                pass
            
            models_info.append(file_info)
        
        return {
            "success": True,
            "models": models_info,
            "total_models": len(models_info)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取模型列表时发生错误: {str(e)}")

# ==================== 模型训练服务集成 API ====================

class ModelTrainingRequest(BaseModel):
    model_type: str
    file_path: str
    target_column: Optional[str] = None
    time_column: Optional[str] = None
    event_column: Optional[str] = None
    test_size: Optional[float] = 0.2
    max_depth: Optional[int] = 10
    n_estimators: Optional[int] = 100
    alpha: Optional[float] = 0.1
    max_iter: Optional[int] = 1000
    learning_rate: Optional[float] = 0.1
    epochs: Optional[int] = 100
    batch_size: Optional[int] = 32
    input_shape: Optional[str] = "(224, 224, 3)"
    num_classes: Optional[int] = 2
    time_window: Optional[int] = 365
    task_type: str

@app.get("/model_training/status")
async def check_model_training_status():
    """检查模型训练服务状态"""
    # 首先尝试默认端口
    try:
        response = requests.get(f"{MODEL_TRAINING_URL}/", timeout=5)
        if response.status_code == 200:
            return {
                "success": True,
                "status": "connected",
                "url": MODEL_TRAINING_URL,
                "response": response.json() if response.content else {"status": "connected"},
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "status": "error",
                "url": MODEL_TRAINING_URL,
                "error": f"服务响应异常: {response.status_code}",
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        # 如果默认端口失败，尝试其他端口
        available_url = find_available_model_training_port()
        if available_url:
            try:
                response = requests.get(f"{available_url}/", timeout=5)
                if response.status_code == 200:
                    return {
                        "success": True,
                        "status": "connected",
                        "url": available_url,
                        "response": response.json() if response.content else {"status": "connected"},
                        "timestamp": datetime.now().isoformat()
                    }
            except:
                pass
        
        return {
            "success": False,
            "status": "disconnected",
            "url": MODEL_TRAINING_URL,
            "error": str(e),
            "available_ports_checked": MODEL_TRAINING_ALTERNATIVE_PORTS,
            "timestamp": datetime.now().isoformat()
        }

@app.get("/model_training/models")
async def get_available_models():
    """获取可用模型列表"""
    try:
        response = requests.get(f"{MODEL_TRAINING_URL}/models", timeout=10)
        if response.status_code == 200:
            return {
                "success": True,
                "models": response.json(),
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取模型列表失败: {str(e)}")

@app.get("/model_training/history")
async def get_training_history():
    """获取训练历史"""
    try:
        response = requests.get(f"{MODEL_TRAINING_URL}/training/history", timeout=10)
        if response.status_code == 200:
            return {
                "success": True,
                "history": response.json(),
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取训练历史失败: {str(e)}")

@app.post("/model_training/train")
async def train_model(request: ModelTrainingRequest):
    """训练模型"""
    try:
        # 准备训练数据
        training_data = {
            "model_type": request.model_type,
            "file_path": request.file_path,
            "task_type": request.task_type
        }
        
        # 添加可选参数
        if request.target_column:
            training_data["target_column"] = request.target_column
        if request.time_column:
            training_data["time_column"] = request.time_column
        if request.event_column:
            training_data["event_column"] = request.event_column
        if request.test_size:
            training_data["test_size"] = request.test_size
        if request.max_depth:
            training_data["max_depth"] = request.max_depth
        if request.n_estimators:
            training_data["n_estimators"] = request.n_estimators
        if request.alpha:
            training_data["alpha"] = request.alpha
        if request.max_iter:
            training_data["max_iter"] = request.max_iter
        if request.learning_rate:
            training_data["learning_rate"] = request.learning_rate
        if request.epochs:
            training_data["epochs"] = request.epochs
        if request.batch_size:
            training_data["batch_size"] = request.batch_size
        if request.input_shape:
            training_data["input_shape"] = request.input_shape
        if request.num_classes:
            training_data["num_classes"] = request.num_classes
        if request.time_window:
            training_data["time_window"] = request.time_window
        
        # 根据任务类型设置超时时间
        timeout = 300  # 默认5分钟
        if request.task_type == "survival":
            timeout = 600  # 10分钟
        elif request.task_type == "deep_learning":
            timeout = 1200  # 20分钟
        
        # 发送训练请求
        response = requests.post(
            f"{MODEL_TRAINING_URL}/train", 
            json=training_data, 
            timeout=timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
            
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="模型训练超时，请稍后重试")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模型训练失败: {str(e)}")

@app.get("/model_training/models/download")
async def download_model():
    """下载训练好的模型"""
    try:
        response = requests.get(f"{MODEL_TRAINING_URL}/models/download", timeout=30)
        if response.status_code == 200:
            return {
                "success": True,
                "model_data": response.content,
                "content_type": response.headers.get("content-type", "application/octet-stream"),
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"下载模型失败: {str(e)}")

@app.delete("/model_training/models/{model_id}")
async def delete_model(model_id: str):
    """删除模型"""
    try:
        response = requests.delete(f"{MODEL_TRAINING_URL}/models/{model_id}", timeout=30)
        if response.status_code == 200:
            return {
                "success": True,
                "message": "模型删除成功",
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除模型失败: {str(e)}")

@app.post("/model_training/models/{model_id}/evaluate")
async def evaluate_model(model_id: str):
    """评估模型性能"""
    try:
        response = requests.post(f"{MODEL_TRAINING_URL}/models/{model_id}/evaluate", timeout=60)
        if response.status_code == 200:
            return {
                "success": True,
                "evaluation": response.json(),
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模型评估失败: {str(e)}")

@app.post("/model_training/predict")
async def predict_with_model(model_id: str, data: Dict[str, Any]):
    """使用模型进行预测"""
    try:
        response = requests.post(
            f"{MODEL_TRAINING_URL}/models/{model_id}/predict", 
            json=data, 
            timeout=30
        )
        if response.status_code == 200:
            return {
                "success": True,
                "prediction": response.json(),
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模型预测失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
