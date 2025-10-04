#!/usr/bin/env python3
"""
使用示例 - 演示如何通过API调用系统功能
"""

import requests
import json
from datetime import datetime

# API 基础URL
API_BASE_URL = "http://127.0.0.1:8000"

def example_patient_data():
    """示例病人数据"""
    return {
        "name": "张三",
        "age": 55,
        "sex": "男",
        "chief_complaint": "右上腹疼痛3周，伴食欲减退、体重下降",
        "history": "高血压5年，无手术史，无过敏史",
        "labs": {
            "ALT": 56,
            "AST": 62,
            "ALP": 120,
            "总胆红素": 25.5,
            "直接胆红素": 8.2,
            "白蛋白": 38,
            "AFP": 420,
            "CA19-9": 45,
            "CEA": 3.2
        },
        "imaging": "CT提示肝右叶占位，大小约3.5cm×2.8cm，边界不清，增强扫描不均匀强化，门静脉无侵犯",
        "additional_notes": "病人精神状态良好，配合治疗，家属支持"
    }

def generate_report_example():
    """生成报告示例"""
    print("📝 生成诊疗报告示例")
    print("-" * 50)
    
    patient_data = example_patient_data()
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/generate_report",
            json={
                "patient": patient_data,
                "report_type": "comprehensive"
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 报告生成成功")
            print(f"病人ID: {result.get('patient_id')}")
            print(f"生成时间: {result.get('generated_at')}")
            print("\n📋 报告内容:")
            print("=" * 50)
            print(result.get('report', ''))
            return result.get('patient_id')
        else:
            print(f"❌ 报告生成失败: {response.status_code}")
            print(response.text)
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        return None

def get_patients_example():
    """获取病人列表示例"""
    print("\n📚 获取病人列表示例")
    print("-" * 50)
    
    try:
        response = requests.get(f"{API_BASE_URL}/patients", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            patients = data.get("patients", [])
            print(f"✅ 获取到 {len(patients)} 个病人记录")
            
            for patient in patients[:3]:  # 只显示前3个
                print(f"  - {patient['name']} ({patient['age']}岁, {patient['sex']})")
                print(f"    主诉: {patient['chief_complaint'][:50]}...")
                print(f"    创建时间: {patient['created_at']}")
                print()
        else:
            print(f"❌ 获取失败: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")

def get_patient_details_example(patient_id):
    """获取病人详情示例"""
    print(f"\n👤 获取病人详情示例 (ID: {patient_id})")
    print("-" * 50)
    
    try:
        response = requests.get(f"{API_BASE_URL}/patient/{patient_id}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            patient = data.get("patient", {})
            reports = data.get("reports", [])
            
            print("✅ 获取病人详情成功")
            print(f"姓名: {patient.get('name')}")
            print(f"年龄: {patient.get('age')}岁")
            print(f"性别: {patient.get('sex')}")
            print(f"主诉: {patient.get('chief_complaint')}")
            print(f"既往病史: {patient.get('history')}")
            print(f"影像学检查: {patient.get('imaging')}")
            print(f"报告数量: {len(reports)}")
            
            if reports:
                print("\n📋 最新报告预览:")
                latest_report = reports[0]
                print(latest_report.get('content', '')[:200] + "...")
        else:
            print(f"❌ 获取失败: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")

def generate_pdf_example(patient_id):
    """生成PDF示例"""
    print(f"\n📄 生成PDF报告示例 (病人ID: {patient_id})")
    print("-" * 50)
    
    try:
        response = requests.post(f"{API_BASE_URL}/generate_pdf/{patient_id}", timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ PDF生成成功")
            print(f"文件名: {result.get('filename')}")
            print(f"文件路径: {result.get('pdf_path')}")
            
            # 提供下载链接
            download_url = f"{API_BASE_URL}/download_pdf/{result.get('filename')}"
            print(f"下载链接: {download_url}")
        else:
            print(f"❌ PDF生成失败: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")

def main():
    """主函数"""
    print("🏥 术前病情预测 & 中西医结合诊疗报告生成系统")
    print("   API 使用示例")
    print("=" * 70)
    
    # 检查API是否可用
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ API服务不可用，请确保后端服务正在运行")
            print("   运行命令: python main.py")
            return
    except requests.exceptions.RequestException:
        print("❌ 无法连接到API服务，请确保后端服务正在运行")
        print("   运行命令: python main.py")
        return
    
    print("✅ API服务连接正常")
    
    # 示例1: 生成报告
    patient_id = generate_report_example()
    
    # 示例2: 获取病人列表
    get_patients_example()
    
    # 示例3: 获取病人详情
    if patient_id:
        get_patient_details_example(patient_id)
        
        # 示例4: 生成PDF
        generate_pdf_example(patient_id)
    
    print("\n" + "=" * 70)
    print("🎉 示例运行完成")
    print("\n💡 更多功能:")
    print("   1. 访问 http://localhost:8501 使用Web界面")
    print("   2. 访问 http://127.0.0.1:8000/docs 查看API文档")
    print("   3. 查看 README.md 了解详细使用说明")

if __name__ == "__main__":
    main()
