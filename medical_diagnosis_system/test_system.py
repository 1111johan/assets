#!/usr/bin/env python3
"""
系统测试脚本 - 验证各个功能模块是否正常工作
"""

import requests
import json
import time
import os
from datetime import datetime

# 测试配置
API_BASE_URL = "http://127.0.0.1:8000"
TEST_PATIENT = {
    "name": "测试病人",
    "age": 55,
    "sex": "男",
    "chief_complaint": "右上腹疼痛3周，伴食欲减退",
    "history": "高血压5年，无手术史",
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
    "imaging": "CT提示肝右叶占位，大小约3.5cm，边界不清，增强扫描不均匀强化",
    "additional_notes": "病人精神状态良好，配合治疗"
}

def test_api_connection():
    """测试API连接"""
    print("🔍 测试API连接...")
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ API连接正常")
            return True
        else:
            print(f"❌ API连接失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API连接失败: {e}")
        return False

def test_generate_report():
    """测试报告生成功能"""
    print("🔍 测试报告生成功能...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/generate_report",
            json={
                "patient": TEST_PATIENT,
                "report_type": "comprehensive"
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success") and result.get("report"):
                print("✅ 报告生成成功")
                print(f"   病人ID: {result.get('patient_id')}")
                print(f"   报告长度: {len(result.get('report', ''))} 字符")
                return result.get("patient_id")
            else:
                print("❌ 报告生成失败: 响应格式错误")
                return None
        else:
            print(f"❌ 报告生成失败: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ 报告生成失败: {e}")
        return None

def test_get_patients():
    """测试获取病人列表"""
    print("🔍 测试获取病人列表...")
    try:
        response = requests.get(f"{API_BASE_URL}/patients", timeout=10)
        if response.status_code == 200:
            data = response.json()
            patients = data.get("patients", [])
            print(f"✅ 获取病人列表成功，共 {len(patients)} 个病人")
            return True
        else:
            print(f"❌ 获取病人列表失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取病人列表失败: {e}")
        return False

def test_get_patient_details(patient_id):
    """测试获取病人详情"""
    print("🔍 测试获取病人详情...")
    try:
        response = requests.get(f"{API_BASE_URL}/patient/{patient_id}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            patient = data.get("patient", {})
            reports = data.get("reports", [])
            print(f"✅ 获取病人详情成功")
            print(f"   姓名: {patient.get('name')}")
            print(f"   报告数量: {len(reports)}")
            return True
        else:
            print(f"❌ 获取病人详情失败: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取病人详情失败: {e}")
        return False

def test_generate_pdf(patient_id):
    """测试PDF生成功能"""
    print("🔍 测试PDF生成功能...")
    try:
        response = requests.post(f"{API_BASE_URL}/generate_pdf/{patient_id}", timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                print("✅ PDF生成成功")
                print(f"   文件名: {result.get('filename')}")
                return True
            else:
                print("❌ PDF生成失败: 响应格式错误")
                return False
        else:
            print(f"❌ PDF生成失败: {response.status_code} - {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ PDF生成失败: {e}")
        return False

def test_database_creation():
    """测试数据库创建"""
    print("🔍 测试数据库创建...")
    try:
        if os.path.exists("medical_reports.db"):
            print("✅ 数据库文件已创建")
            return True
        else:
            print("❌ 数据库文件未找到")
            return False
    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("🏥 术前病情预测 & 中西医结合诊疗报告生成系统 - 功能测试")
    print("=" * 70)
    
    tests_passed = 0
    total_tests = 6
    
    # 测试1: API连接
    if test_api_connection():
        tests_passed += 1
    print()
    
    # 测试2: 数据库创建
    if test_database_creation():
        tests_passed += 1
    print()
    
    # 测试3: 报告生成
    patient_id = test_generate_report()
    if patient_id:
        tests_passed += 1
    print()
    
    # 测试4: 获取病人列表
    if test_get_patients():
        tests_passed += 1
    print()
    
    # 测试5: 获取病人详情
    if patient_id and test_get_patient_details(patient_id):
        tests_passed += 1
    print()
    
    # 测试6: PDF生成
    if patient_id and test_generate_pdf(patient_id):
        tests_passed += 1
    print()
    
    # 测试结果汇总
    print("=" * 70)
    print(f"📊 测试结果: {tests_passed}/{total_tests} 通过")
    
    if tests_passed == total_tests:
        print("🎉 所有测试通过！系统运行正常")
        print("\n💡 下一步:")
        print("   1. 运行 'python start.py' 启动完整系统")
        print("   2. 在浏览器中访问 http://localhost:8501")
        print("   3. 开始使用系统生成诊疗报告")
    else:
        print("⚠️  部分测试失败，请检查系统配置")
        print("\n🔧 故障排除:")
        print("   1. 确保后端服务正在运行 (python main.py)")
        print("   2. 检查 OpenAI API Key 是否正确配置")
        print("   3. 确保所有依赖已安装 (pip install -r requirements.txt)")

if __name__ == "__main__":
    run_all_tests()
