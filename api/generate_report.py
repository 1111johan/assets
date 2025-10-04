"""
Vercel Serverless Function for generating medical reports
"""
import os
import json
from datetime import datetime
from openai import OpenAI
from typing import Dict, Any

# Initialize OpenAI client
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

dashscope_client = OpenAI(
    api_key=DASHSCOPE_API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

def handler(request):
    """Main handler for Vercel serverless function"""
    if request.method == "POST":
        try:
            # Parse request body
            body = request.get_json()
            if not body:
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "Invalid request body"})
                }
            
            patient_data = body.get("patient", {})
            report_type = body.get("report_type", "comprehensive")
            
            # Generate report
            report_content = generate_medical_report(patient_data)
            
            # Save to database (simplified for serverless)
            patient_id = save_patient_simple(patient_data)
            
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": json.dumps({
                    "success": True,
                    "patient_id": patient_id,
                    "report": report_content,
                    "generated_at": datetime.now().isoformat()
                })
            }
            
        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": f"生成报告时发生错误: {str(e)}"})
            }
    
    elif request.method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": ""
        }
    
    else:
        return {
            "statusCode": 405,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Method not allowed"})
        }

def generate_medical_report(patient: Dict[str, Any]) -> str:
    """Generate medical report using AI"""
    prompt = f"""
    你是一个经验丰富的肝胆外科医生，同时精通中医辨证论治理论。请根据以下病人信息生成一份完整的中西医结合术前诊疗报告。

    **病人基本信息：**
    - 姓名：{patient.get('name', '未知')}
    - 年龄：{patient.get('age', 0)}岁
    - 性别：{patient.get('sex', '未知')}
    - 主诉：{patient.get('chief_complaint', '无')}
    - 既往病史：{patient.get('history', '无')}
    - 实验室检查：{json.dumps(patient.get('labs', {}), ensure_ascii=False, indent=2)}
    - 影像学检查：{patient.get('imaging', '无')}
    - 其他备注：{patient.get('additional_notes', '无')}

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
    
    try:
        response = dashscope_client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "你是一个专业的医疗AI助手，专门生成中西医结合的诊疗报告。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=3000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"报告生成失败：{str(e)}"

def save_patient_simple(patient: Dict[str, Any]) -> str:
    """Simple patient saving for serverless environment"""
    # In a real implementation, you would use a database service
    # For now, return a simple ID
    return f"patient_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# Vercel entry point
def main(request):
    return handler(request)

# Alternative entry point for Vercel
def handler(request):
    """Main handler for Vercel serverless function"""
    if request.method == "POST":
        try:
            # Parse request body
            body = request.get_json()
            if not body:
                return {
                    "statusCode": 400,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "Invalid request body"})
                }
            
            patient_data = body.get("patient", {})
            report_type = body.get("report_type", "comprehensive")
            
            # Generate report
            report_content = generate_medical_report(patient_data)
            
            # Save to database (simplified for serverless)
            patient_id = save_patient_simple(patient_data)
            
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": json.dumps({
                    "success": True,
                    "patient_id": patient_id,
                    "report": report_content,
                    "generated_at": datetime.now().isoformat()
                })
            }
            
        except Exception as e:
            return {
                "statusCode": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": f"生成报告时发生错误: {str(e)}"})
            }
    
    elif request.method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": ""
        }
    
    else:
        return {
            "statusCode": 405,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Method not allowed"})
        }