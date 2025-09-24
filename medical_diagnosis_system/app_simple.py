"""
简化版医疗AI科研系统前端 - 无JavaScript错误，完整功能
基于原版app.py，添加现代化样式，确保所有功能正常工作
"""

import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import os
from config import config

# 配置页面
st.set_page_config(
    page_title="医疗AI科研系统",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API配置 - 从配置文件读取
API_BASE_URL = config.API_BASE_URL
MODEL_TRAINING_URL = config.MODEL_TRAINING_URL

# 现代化CSS样式 - 简化版，避免JavaScript问题
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        text-align: center;
        padding: 2rem 0;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    .section-header {
        color: #6366f1;
        padding: 1rem 0;
        border-left: 4px solid #6366f1;
        padding-left: 1rem;
        margin: 1.5rem 0;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    .modern-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
        transition: all 0.2s ease-in-out;
    }
    
    .modern-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
    }
    
    .report-container {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }
    
    .success-message {
        background: #dcfce7;
        color: #166534;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #bbf7d0;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #fef2f2;
        color: #dc2626;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #fecaca;
        margin: 1rem 0;
    }
    
    .warning-message {
        background: #fefce8;
        color: #ca8a04;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #fde68a;
        margin: 1rem 0;
    }
    
    .info-message {
        background: #eff6ff;
        color: #1d4ed8;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #bfdbfe;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #6366f1;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #64748b;
        margin: 0.5rem 0 0 0;
    }
    
    .sidebar .sidebar-content {
        padding: 1rem;
    }
    
    .sidebar .sidebar-content .nav-item {
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: 0.5rem;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
    }
    
    .sidebar .sidebar-content .nav-item:hover {
        background: #f1f5f9;
        color: #0f172a;
    }
    
    .sidebar .sidebar-content .nav-item.active {
        background: #6366f1;
        color: #ffffff;
    }
    
    .stButton > button {
        background: #6366f1;
        color: #ffffff;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease-in-out;
    }
    
    .stButton > button:hover {
        background: #5b21b6;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stTextInput > div > div > input {
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 0.5rem 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
    }
    
    .stTextArea > div > div > textarea {
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 0.5rem 0.75rem;
    }
    
    .stSelectbox > div > div > select {
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 0.5rem 0.75rem;
    }
    
    .stNumberInput > div > div > input {
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
        padding: 0.5rem 0.75rem;
    }
    
    .stExpander > div {
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
    }
    
    .stExpander > div > div {
        background: #f8fafc;
        border-radius: 0.5rem;
    }
    
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 0.5rem;
    }
    
    .stAlert {
        border-radius: 0.5rem;
    }
    
    .stSuccess {
        background: #dcfce7;
        color: #166534;
        border: 1px solid #bbf7d0;
    }
    
    .stError {
        background: #fef2f2;
        color: #dc2626;
        border: 1px solid #fecaca;
    }
    
    .stWarning {
        background: #fefce8;
        color: #ca8a04;
        border: 1px solid #fde68a;
    }
    
    .stInfo {
        background: #eff6ff;
        color: #1d4ed8;
        border: 1px solid #bfdbfe;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        
        .main-header p {
            font-size: 1rem;
        }
        
        .section-header {
            font-size: 1.25rem;
        }
        
        .modern-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def main():
    """主应用函数"""
    
    # 初始化session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # 主标题
    st.markdown("""
    <div class="main-header">
        <h1>🏥 术前病情预测 & 中西医结合诊疗报告生成系统</h1>
        <p>AI-Powered Medical Diagnostic & Report Generation System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 侧边栏导航
    st.sidebar.title("🧭 导航菜单")
    
    # 导航选项
    nav_options = [
        "新增病人报告", "查看历史记录", "AI对话助手", "报告整理优化", "症状分析", 
        "科研数据分析", "模型训练", "证据包生成", "系统设置"
    ]
    
    selected_page = st.sidebar.selectbox("选择功能", nav_options)
    
    # 系统状态
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 系统状态")
    
    # 检查后端连接
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code == 200:
            st.sidebar.success("✅ 后端API正常")
        else:
            st.sidebar.error("❌ 后端API异常")
    except:
        st.sidebar.error("❌ 后端API离线")
    
    # 页面路由
    if selected_page == "新增病人报告":
        new_patient_page()
    elif selected_page == "查看历史记录":
        history_page()
    elif selected_page == "AI对话助手":
        ai_chat_page()
    elif selected_page == "报告整理优化":
        report_optimize_page()
    elif selected_page == "症状分析":
        symptom_analysis_page()
    elif selected_page == "科研数据分析":
        research_data_analysis_page()
    elif selected_page == "模型训练":
        model_training_page()
    elif selected_page == "证据包生成":
        evidence_bundle_page()
    elif selected_page == "系统设置":
        settings_page()

def new_patient_page():
    """新增病人页面"""
    st.markdown('<h2 class="section-header">📝 新增病人诊疗报告</h2>', unsafe_allow_html=True)
    
    # 使用两个容器：一个用于表单，一个用于结果
    form_container = st.container()
    result_container = st.container()
    
    with form_container:
        with st.form("patient_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 基本信息")
                name = st.text_input("姓名 *", placeholder="请输入病人姓名")
                age = st.number_input("年龄 *", min_value=0, max_value=120, value=50)
                gender = st.selectbox("性别 *", ["男", "女"])
                
                st.markdown("#### 临床信息")
                chief_complaint = st.text_area("主诉 *", placeholder="请详细描述主要症状和持续时间", height=100)
                medical_history = st.text_area("既往病史", placeholder="请描述相关既往病史、手术史、过敏史等", height=100)
            
            with col2:
                st.markdown("#### 实验室检查")
                col2_1, col2_2 = st.columns(2)
                
                with col2_1:
                    alt = st.number_input("ALT (U/L)", min_value=0.0, value=40.0, step=0.1)
                    ast = st.number_input("AST (U/L)", min_value=0.0, value=40.0, step=0.1)
                    alp = st.number_input("ALP (U/L)", min_value=0.0, value=100.0, step=0.1)
                    total_bilirubin = st.number_input("总胆红素 (μmol/L)", min_value=0.0, value=20.0, step=0.1)
                    direct_bilirubin = st.number_input("直接胆红素 (μmol/L)", min_value=0.0, value=5.0, step=0.1)
                
                with col2_2:
                    albumin = st.number_input("白蛋白 (g/L)", min_value=0.0, value=40.0, step=0.1)
                    afp = st.number_input("AFP (ng/mL)", min_value=0.0, value=20.0, step=0.1)
                    ca199 = st.number_input("CA19-9 (U/mL)", min_value=0.0, value=37.0, step=0.1)
                    cea = st.number_input("CEA (ng/mL)", min_value=0.0, value=5.0, step=0.1)
                
                st.markdown("#### 影像学检查")
                imaging_results = st.text_area("影像学检查结果", placeholder="请描述CT、MRI、超声等影像学检查结果...", height=100)
            
            # 提交按钮
            submitted = st.form_submit_button("🔍 生成诊疗报告", type="primary")
    
    # 处理表单提交
    if submitted:
        if not name or not chief_complaint:
            st.error("⚠️ 请填写必填项：姓名和主诉")
        else:
            with result_container:
                with st.spinner("正在生成诊疗报告..."):
                    try:
                        # 准备数据
                        patient_data = {
                            "name": name,
                            "age": age,
                            "gender": gender,
                            "chief_complaint": chief_complaint,
                            "medical_history": medical_history,
                            "lab_results": {
                                "alt": alt,
                                "ast": ast,
                                "alp": alp,
                                "total_bilirubin": total_bilirubin,
                                "direct_bilirubin": direct_bilirubin,
                                "albumin": albumin,
                                "afp": afp,
                                "ca199": ca199,
                                "cea": cea
                            },
                            "imaging_results": imaging_results
                        }
                        
                        # 调用API生成报告
                        api_request = {
                            "patient": {
                                "name": name,
                                "age": age,
                                "sex": gender,
                                "chief_complaint": chief_complaint,
                                "history": medical_history,
                                "labs": {
                                    "ALT": alt,
                                    "AST": ast,
                                    "ALP": alp,
                                    "总胆红素": total_bilirubin,
                                    "直接胆红素": direct_bilirubin,
                                    "白蛋白": albumin,
                                    "AFP": afp,
                                    "CA19-9": ca199,
                                    "CEA": cea
                                },
                                "imaging": imaging_results,
                                "additional_notes": ""
                            },
                            "report_type": "comprehensive"
                        }
                        response = requests.post(f"{API_BASE_URL}/generate_report", json=api_request)
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            st.success("✅ 诊疗报告生成成功！")
                            
                            # 显示报告
                            st.markdown('<div class="report-container">', unsafe_allow_html=True)
                            st.markdown("### 📋 中西医结合诊疗报告")
                            st.markdown(f"**患者姓名**: {name}")
                            st.markdown(f"**年龄**: {age}岁")
                            st.markdown(f"**性别**: {gender}")
                            st.markdown(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                            st.markdown("---")
                            
                            # 显示报告内容
                            st.markdown(result.get("report", "报告生成失败"))
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            # 下载按钮
                            if "report" in result:
                                st.download_button(
                                    label="📥 下载报告",
                                    data=result["report"],
                                    file_name=f"诊疗报告_{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                    mime="text/plain"
                                )
                        else:
                            st.error(f"❌ 报告生成失败: {response.text}")
                            
                    except Exception as e:
                        st.error(f"❌ 发生错误: {str(e)}")

def history_page():
    """历史记录页面"""
    st.markdown('<h2 class="section-header">📚 查看历史记录</h2>', unsafe_allow_html=True)
    
    try:
        # 获取患者列表
        response = requests.get(f"{API_BASE_URL}/patients")
        
        if response.status_code == 200:
            data = response.json()
            patients = data.get('patients', []) if isinstance(data, dict) else data
            
            if patients:
                # 操作按钮区域
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    # 搜索功能
                    search_term = st.text_input("🔍 搜索患者", placeholder="输入患者姓名或ID")
                
                with col2:
                    if st.button("🗑️ 删除全部记录", type="secondary", help="删除所有患者记录"):
                        if st.session_state.get('confirm_delete_all', False):
                            delete_all_patients()
                            st.session_state.confirm_delete_all = False
                            st.rerun()
                        else:
                            st.session_state.confirm_delete_all = True
                            st.warning("⚠️ 点击确认删除所有记录")
                
                with col3:
                    if st.session_state.get('confirm_delete_all', False):
                        if st.button("✅ 确认删除", type="primary"):
                            delete_all_patients()
                            st.session_state.confirm_delete_all = False
                            st.rerun()
                        if st.button("❌ 取消", type="secondary"):
                            st.session_state.confirm_delete_all = False
                            st.rerun()
                
                # 筛选患者
                filtered_patients = patients
                if search_term:
                    filtered_patients = [p for p in patients if search_term.lower() in p.get('name', '').lower()]
                
                # 显示患者列表
                st.markdown(f"### 患者记录 ({len(filtered_patients)} 条)")
                
                for patient in filtered_patients:
                    with st.expander(f"👤 {patient.get('name', '未知')} - {patient.get('created_at', '未知时间')}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**患者ID**: {patient.get('id', 'N/A')}")
                            st.write(f"**姓名**: {patient.get('name', 'N/A')}")
                            st.write(f"**年龄**: {patient.get('age', 'N/A')}岁")
                            st.write(f"**性别**: {patient.get('sex', 'N/A')}")
                        
                        with col2:
                            st.write(f"**主诉**: {patient.get('chief_complaint', 'N/A')}")
                            st.write(f"**创建时间**: {patient.get('created_at', 'N/A')}")
                        
                        # 操作按钮
                        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
                        
                        with col_btn1:
                            if st.button(f"👁️ 查看详情", key=f"view_{patient.get('id')}"):
                                view_patient_details(patient.get('id'))
                        
                        with col_btn2:
                            if st.button(f"🗑️ 删除", key=f"delete_{patient.get('id')}", type="secondary"):
                                if st.session_state.get(f'confirm_delete_{patient.get("id")}', False):
                                    delete_patient(patient.get('id'))
                                    st.session_state[f'confirm_delete_{patient.get("id")}'] = False
                                    st.rerun()
                                else:
                                    st.session_state[f'confirm_delete_{patient.get("id")}'] = True
                                    st.warning(f"⚠️ 确认删除患者 {patient.get('name', '未知')} 的记录？")
                        
                        with col_btn3:
                            if st.session_state.get(f'confirm_delete_{patient.get("id")}', False):
                                if st.button(f"✅ 确认", key=f"confirm_{patient.get('id')}", type="primary"):
                                    delete_patient(patient.get('id'))
                                    st.session_state[f'confirm_delete_{patient.get("id")}'] = False
                                    st.rerun()
                                if st.button(f"❌ 取消", key=f"cancel_{patient.get('id')}", type="secondary"):
                                    st.session_state[f'confirm_delete_{patient.get("id")}'] = False
                                    st.rerun()
            else:
                st.info("📝 暂无患者记录")
        else:
            st.error(f"❌ 获取患者列表失败: {response.text}")
            
    except Exception as e:
        st.error(f"❌ 发生错误: {str(e)}")

def delete_patient(patient_id):
    """删除单个患者记录"""
    try:
        response = requests.delete(f"{API_BASE_URL}/patient/{patient_id}")
        
        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ {result.get('message', '患者记录已删除')}")
            st.rerun()
        else:
            st.error(f"❌ 删除患者记录失败: {response.text}")
            
    except Exception as e:
        st.error(f"❌ 发生错误: {str(e)}")

def delete_all_patients():
    """删除所有患者记录"""
    try:
        response = requests.delete(f"{API_BASE_URL}/patients/all")
        
        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ {result.get('message', '所有记录已删除')}")
            st.rerun()
        else:
            st.error(f"❌ 删除所有记录失败: {response.text}")
            
    except Exception as e:
        st.error(f"❌ 发生错误: {str(e)}")

def view_patient_details(patient_id):
    """查看患者详情"""
    try:
        response = requests.get(f"{API_BASE_URL}/patient/{patient_id}")
        
        if response.status_code == 200:
            patient = response.json()
            
            st.markdown("### 📋 患者详细信息")
            st.json(patient)
        else:
            st.error(f"❌ 获取患者详情失败: {response.text}")
            
    except Exception as e:
        st.error(f"❌ 发生错误: {str(e)}")

def ai_chat_page():
    """AI对话页面"""
    st.markdown('<h2 class="section-header">🤖 AI对话助手</h2>', unsafe_allow_html=True)
    
    # 聊天历史
    if st.session_state.chat_history:
        st.markdown("### 💬 对话历史")
        for i, message in enumerate(st.session_state.chat_history):
            if message["role"] == "user":
                st.markdown(f"**您**: {message['content']}")
            else:
                st.markdown(f"**AI**: {message['content']}")
            st.markdown("---")
    
    # 输入框
    user_input = st.text_input("💬 请输入您的问题", placeholder="例如：请解释一下肝癌的早期症状")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        send_button = st.button("发送", type="primary")
    with col2:
        clear_button = st.button("清空对话")
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()
    
    if send_button and user_input:
        with st.spinner("AI正在思考..."):
            try:
                # 调用AI API
                response = requests.post(f"{API_BASE_URL}/chat", json={
                    "message": user_input,
                    "conversation_history": st.session_state.chat_history
                })
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result.get("response", "抱歉，我无法回答您的问题。")
                    
                    # 添加到聊天历史
                    st.session_state.chat_history.append({"role": "user", "content": user_input})
                    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
                    
                    st.rerun()
                else:
                    st.error(f"❌ AI对话失败: {response.text}")
                    
            except Exception as e:
                st.error(f"❌ 发生错误: {str(e)}")

def report_optimize_page():
    """报告优化页面"""
    st.markdown('<h2 class="section-header">📊 报告整理优化</h2>', unsafe_allow_html=True)
    
    st.markdown("### 📝 输入需要优化的报告内容")
    
    report_text = st.text_area("报告内容", placeholder="请粘贴需要优化的报告内容...", height=200)
    
    if st.button("🔧 优化报告", type="primary"):
        if report_text:
            with st.spinner("正在优化报告..."):
                try:
                    response = requests.post(f"{API_BASE_URL}/optimize_report", json={
                        "original_report": report_text,
                        "optimize_type": "format"
                    })
                    
                    if response.status_code == 200:
                        result = response.json()
                        optimized_report = result.get("optimized_report", "优化失败")
                        
                        st.success("✅ 报告优化完成！")
                        st.markdown("### 📋 优化后的报告")
                        st.markdown(optimized_report)
                        
                        # 下载按钮
                        st.download_button(
                            label="📥 下载优化后的报告",
                            data=optimized_report,
                            file_name=f"优化报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error(f"❌ 报告优化失败: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")
        else:
            st.warning("⚠️ 请输入需要优化的报告内容")

def symptom_analysis_page():
    """症状分析页面"""
    st.markdown('<h2 class="section-header">🔍 症状分析</h2>', unsafe_allow_html=True)
    
    st.markdown("### 📝 输入症状信息")
    
    symptoms = st.text_area("症状描述", placeholder="请详细描述患者的症状，例如：发热、咳嗽、胸痛等...", height=150)
    
    if st.button("🔍 分析症状", type="primary"):
        if symptoms:
            with st.spinner("正在分析症状..."):
                try:
                    response = requests.post(f"{API_BASE_URL}/analyze_symptoms", json={
                        "symptoms": symptoms,
                        "analysis_type": "comprehensive"
                    })
                    
                    if response.status_code == 200:
                        result = response.json()
                        analysis = result.get("analysis", "分析失败")
                        
                        st.success("✅ 症状分析完成！")
                        st.markdown("### 📋 分析结果")
                        st.markdown(analysis)
                    else:
                        st.error(f"❌ 症状分析失败: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")
        else:
            st.warning("⚠️ 请输入症状描述")

def research_data_analysis_page():
    """科研数据分析页面"""
    st.markdown('<h2 class="section-header">🔬 科研数据分析</h2>', unsafe_allow_html=True)
    
    st.markdown("### 📊 数据上传和分析")
    
    # 文件上传
    uploaded_file = st.file_uploader("选择数据文件", type=['csv', 'xlsx', 'xls'])
    
    if uploaded_file is not None:
        try:
            # 读取数据
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ 数据加载成功！共 {len(df)} 行数据")
            
            # 显示数据预览
            st.markdown("### 📋 数据预览")
            st.dataframe(df.head(), use_container_width=True)
            
            # 基本统计信息
            st.markdown("### 📈 基本统计信息")
            st.dataframe(df.describe(), use_container_width=True)
            
            # 数据质量检查
            st.markdown("### 🔍 数据质量检查")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("总行数", len(df))
            with col2:
                st.metric("缺失值", df.isnull().sum().sum())
            with col3:
                st.metric("重复行", df.duplicated().sum())
            
        except Exception as e:
            st.error(f"❌ 数据加载失败: {str(e)}")

def model_training_page():
    """模型训练页面 - 集成外部模型训练服务"""
    st.markdown('<h2 class="section-header">🤖 科研模型训练</h2>', unsafe_allow_html=True)
    
    # 检查模型训练服务连接状态
    st.markdown("### 🔗 服务连接状态")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔍 检查模型训练服务", type="secondary"):
            with st.spinner("检查服务连接..."):
                try:
                    response = requests.get(f"{API_BASE_URL}/model_training/status", timeout=5)
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("success"):
                            st.success("✅ 模型训练服务连接正常")
                            st.json(result.get("response", {"status": "connected"}))
                        else:
                            st.warning(f"⚠️ 服务状态: {result.get('status', 'unknown')}")
                            st.error(f"错误: {result.get('error', 'unknown error')}")
                    else:
                        st.warning(f"⚠️ 服务响应异常: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ 无法连接到模型训练服务: {str(e)}")
    
    with col2:
        if st.button("📊 查看可用模型", type="secondary"):
            with st.spinner("获取模型列表..."):
                try:
                    response = requests.get(f"{API_BASE_URL}/model_training/models", timeout=10)
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("success"):
                            st.success("✅ 获取模型列表成功")
                            st.json(result.get("models", []))
                        else:
                            st.error(f"❌ 获取模型列表失败: {result.get('error', 'unknown error')}")
                    else:
                        st.error(f"❌ 获取模型列表失败: {response.text}")
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")
    
    with col3:
        if st.button("📈 查看训练历史", type="secondary"):
            with st.spinner("获取训练历史..."):
                try:
                    response = requests.get(f"{API_BASE_URL}/model_training/history", timeout=10)
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("success"):
                            st.success("✅ 获取训练历史成功")
                            st.json(result.get("history", []))
                        else:
                            st.error(f"❌ 获取训练历史失败: {result.get('error', 'unknown error')}")
                    else:
                        st.error(f"❌ 获取训练历史失败: {response.text}")
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")
    
    st.markdown("---")
    st.markdown("### 🎯 模型训练任务")
    
    # 训练任务选择
    tab1, tab2, tab3, tab4 = st.tabs(["🏥 诊断分类", "⏰ 生存分析", "🔄 复发预测", "🧠 深度学习"])
    
    with tab1:
        st.markdown("#### 诊断分类模型训练")
        
        col1, col2 = st.columns(2)
        
        with col1:
            model_type = st.selectbox("模型类型", ["random_forest", "xgboost", "svm", "logistic_regression"], key="diag_model")
            target_column = st.text_input("目标列名", value="diagnosis", key="diag_target")
            test_size = st.slider("测试集比例", 0.1, 0.5, 0.2, key="diag_test")
        
        with col2:
            file_path = st.text_input("数据文件路径", value="research_data/medical_data.csv", key="diag_file")
            max_depth = st.number_input("最大深度", value=10, min_value=1, max_value=50, key="diag_depth")
            n_estimators = st.number_input("估计器数量", value=100, min_value=10, max_value=1000, key="diag_est")
        
        if st.button("🚀 开始训练诊断模型", type="primary", key="diag_train"):
            with st.spinner("正在训练诊断分类模型..."):
                try:
                    training_data = {
                        "model_type": model_type,
                        "file_path": file_path,
                        "target_column": target_column,
                        "test_size": test_size,
                        "max_depth": max_depth,
                        "n_estimators": n_estimators,
                        "task_type": "classification"
                    }
                    
                    response = requests.post(f"{API_BASE_URL}/model_training/train", 
                                           json=training_data, 
                                           timeout=300)  # 5分钟超时
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("success"):
                            training_result = result.get("result", {})
                            st.success("✅ 诊断模型训练完成！")
                            
                            # 显示训练结果
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("准确率", f"{training_result.get('accuracy', 0):.3f}")
                                st.metric("精确率", f"{training_result.get('precision', 0):.3f}")
                            with col2:
                                st.metric("召回率", f"{training_result.get('recall', 0):.3f}")
                                st.metric("F1分数", f"{training_result.get('f1_score', 0):.3f}")
                            
                            st.json(training_result)
                        else:
                            st.error(f"❌ 模型训练失败: {result.get('error', 'unknown error')}")
                    else:
                        st.error(f"❌ 模型训练失败: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")
    
    with tab2:
        st.markdown("#### 生存分析模型训练")
        
        col1, col2 = st.columns(2)
        
        with col1:
            survival_model = st.selectbox("生存模型类型", ["cox", "random_forest_survival", "gradient_boosting_survival"], key="surv_model")
            time_column = st.text_input("时间列名", value="survival_time", key="surv_time")
            event_column = st.text_input("事件列名", value="event", key="surv_event")
        
        with col2:
            file_path = st.text_input("数据文件路径", value="research_data/survival_data.csv", key="surv_file")
            alpha = st.slider("正则化参数", 0.01, 1.0, 0.1, key="surv_alpha")
            max_iter = st.number_input("最大迭代次数", value=1000, min_value=100, max_value=10000, key="surv_iter")
        
        if st.button("🚀 开始训练生存模型", type="primary", key="surv_train"):
            with st.spinner("正在训练生存分析模型..."):
                try:
                    training_data = {
                        "model_type": survival_model,
                        "file_path": file_path,
                        "time_column": time_column,
                        "event_column": event_column,
                        "alpha": alpha,
                        "max_iter": max_iter,
                        "task_type": "survival"
                    }
                    
                    response = requests.post(f"{API_BASE_URL}/model_training/train", 
                                           json=training_data, 
                                           timeout=600)  # 10分钟超时
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("success"):
                            training_result = result.get("result", {})
                            st.success("✅ 生存分析模型训练完成！")
                            
                            # 显示训练结果
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("C-index", f"{training_result.get('c_index', 0):.3f}")
                                st.metric("AUC", f"{training_result.get('auc', 0):.3f}")
                            with col2:
                                st.metric("Brier Score", f"{training_result.get('brier_score', 0):.3f}")
                                st.metric("训练时间", f"{training_result.get('training_time', 0):.1f}秒")
                            
                            st.json(training_result)
                        else:
                            st.error(f"❌ 模型训练失败: {result.get('error', 'unknown error')}")
                    else:
                        st.error(f"❌ 模型训练失败: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")
    
    with tab3:
        st.markdown("#### 复发预测模型训练")
        
        col1, col2 = st.columns(2)
        
        with col1:
            recurrence_model = st.selectbox("复发模型类型", ["random_forest", "xgboost", "neural_network"], key="rec_model")
            recurrence_column = st.text_input("复发列名", value="recurrence", key="rec_target")
            time_window = st.number_input("预测时间窗口(天)", value=365, min_value=30, max_value=3650, key="rec_window")
        
        with col2:
            file_path = st.text_input("数据文件路径", value="research_data/recurrence_data.csv", key="rec_file")
            learning_rate = st.slider("学习率", 0.001, 0.5, 0.1, key="rec_lr")
            epochs = st.number_input("训练轮数", value=100, min_value=10, max_value=1000, key="rec_epochs")
        
        if st.button("🚀 开始训练复发模型", type="primary", key="rec_train"):
            with st.spinner("正在训练复发预测模型..."):
                try:
                    training_data = {
                        "model_type": recurrence_model,
                        "file_path": file_path,
                        "target_column": recurrence_column,
                        "time_window": time_window,
                        "learning_rate": learning_rate,
                        "epochs": epochs,
                        "task_type": "recurrence_prediction"
                    }
                    
                    response = requests.post(f"{API_BASE_URL}/model_training/train", 
                                           json=training_data, 
                                           timeout=600)
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("success"):
                            training_result = result.get("result", {})
                            st.success("✅ 复发预测模型训练完成！")
                            
                            # 显示训练结果
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("准确率", f"{training_result.get('accuracy', 0):.3f}")
                                st.metric("AUC", f"{training_result.get('auc', 0):.3f}")
                            with col2:
                                st.metric("精确率", f"{training_result.get('precision', 0):.3f}")
                                st.metric("召回率", f"{training_result.get('recall', 0):.3f}")
                            
                            st.json(training_result)
                        else:
                            st.error(f"❌ 模型训练失败: {result.get('error', 'unknown error')}")
                    else:
                        st.error(f"❌ 模型训练失败: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")
    
    with tab4:
        st.markdown("#### 深度学习模型训练")
        
        col1, col2 = st.columns(2)
        
        with col1:
            dl_model = st.selectbox("深度学习模型", ["cnn", "lstm", "transformer", "resnet"], key="dl_model")
            input_shape = st.text_input("输入形状", value="(224, 224, 3)", key="dl_input")
            num_classes = st.number_input("分类数量", value=2, min_value=2, max_value=100, key="dl_classes")
        
        with col2:
            file_path = st.text_input("数据文件路径", value="research_data/deep_learning_data.csv", key="dl_file")
            batch_size = st.selectbox("批次大小", [16, 32, 64, 128], key="dl_batch")
            learning_rate = st.slider("学习率", 0.0001, 0.01, 0.001, key="dl_lr")
        
        if st.button("🚀 开始训练深度学习模型", type="primary", key="dl_train"):
            with st.spinner("正在训练深度学习模型..."):
                try:
                    training_data = {
                        "model_type": dl_model,
                        "file_path": file_path,
                        "input_shape": input_shape,
                        "num_classes": num_classes,
                        "batch_size": batch_size,
                        "learning_rate": learning_rate,
                        "task_type": "deep_learning"
                    }
                    
                    response = requests.post(f"{API_BASE_URL}/model_training/train", 
                                           json=training_data, 
                                           timeout=1200)  # 20分钟超时
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("success"):
                            training_result = result.get("result", {})
                            st.success("✅ 深度学习模型训练完成！")
                            
                            # 显示训练结果
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("训练准确率", f"{training_result.get('train_accuracy', 0):.3f}")
                                st.metric("验证准确率", f"{training_result.get('val_accuracy', 0):.3f}")
                            with col2:
                                st.metric("训练损失", f"{training_result.get('train_loss', 0):.3f}")
                                st.metric("验证损失", f"{training_result.get('val_loss', 0):.3f}")
                            
                            st.json(training_result)
                        else:
                            st.error(f"❌ 模型训练失败: {result.get('error', 'unknown error')}")
                    else:
                        st.error(f"❌ 模型训练失败: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")
    
    # 模型管理部分
    st.markdown("---")
    st.markdown("### 🔧 模型管理")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 下载训练好的模型", type="secondary"):
            with st.spinner("获取模型列表..."):
                try:
                    response = requests.get(f"{API_BASE_URL}/model_training/models/download", timeout=30)
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("success"):
                            st.success("✅ 模型下载链接已生成")
                            st.download_button(
                                label="下载模型文件",
                                data=result.get("model_data", b""),
                                file_name="trained_model.pkl",
                                mime=result.get("content_type", "application/octet-stream")
                            )
                        else:
                            st.error(f"❌ 下载失败: {result.get('error', 'unknown error')}")
                    else:
                        st.error(f"❌ 下载失败: {response.text}")
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")
    
    with col2:
        if st.button("🗑️ 删除模型", type="secondary"):
            model_id = st.text_input("输入模型ID", key="delete_model_id")
            if st.button("确认删除", key="confirm_delete"):
                try:
                    response = requests.delete(f"{API_BASE_URL}/model_training/models/{model_id}", timeout=30)
                    if response.status_code == 200:
                        result = response.json()
                        if result.get("success"):
                            st.success("✅ 模型删除成功")
                        else:
                            st.error(f"❌ 删除失败: {result.get('error', 'unknown error')}")
                    else:
                        st.error(f"❌ 删除失败: {response.text}")
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")
    
    with col3:
        if st.button("📊 模型性能评估", type="secondary"):
            model_id = st.text_input("输入模型ID", key="eval_model_id")
            if st.button("开始评估", key="start_eval"):
                with st.spinner("正在评估模型性能..."):
                    try:
                        response = requests.post(f"{API_BASE_URL}/model_training/models/{model_id}/evaluate", timeout=60)
                        if response.status_code == 200:
                            result = response.json()
                            if result.get("success"):
                                st.success("✅ 模型评估完成")
                                st.json(result.get("evaluation", {}))
                            else:
                                st.error(f"❌ 评估失败: {result.get('error', 'unknown error')}")
                        else:
                            st.error(f"❌ 评估失败: {response.text}")
                    except Exception as e:
                        st.error(f"❌ 发生错误: {str(e)}")

def evidence_bundle_page():
    """证据包生成页面"""
    st.markdown('<h2 class="section-header">📋 证据包生成</h2>', unsafe_allow_html=True)
    
    st.markdown("### 🔬 科研证据包生成")
    
    col1, col2 = st.columns(2)
    
    with col1:
        analysis_type = st.selectbox("分析类型", ["comprehensive", "sample", "tcm_integration"])
        include_tcm = st.checkbox("包含中医分析", value=True)
    
    with col2:
        st.markdown("#### 患者数据")
        patient_name = st.text_input("患者姓名", value="示例患者")
        patient_age = st.number_input("年龄", value=50, min_value=0, max_value=120)
    
    if st.button("🔬 生成证据包", type="primary"):
        with st.spinner("正在生成科研证据包..."):
            try:
                patient_data = {
                    "name": patient_name,
                    "age": patient_age,
                    "gender": "男",
                    "chief_complaint": "右上腹疼痛3个月",
                    "medical_history": "无特殊病史"
                }
                
                response = requests.post(f"{API_BASE_URL}/research/generate_evidence_bundle", json={
                    "patient_data": patient_data,
                    "analysis_type": analysis_type,
                    "include_tcm": include_tcm
                })
                
                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ 证据包生成完成！")
                    
                    # 显示证据包
                    st.markdown("### 📋 科研证据包")
                    st.json(result.get("evidence_bundle", {}))
                    
                    # 显示科研报告
                    st.markdown("### 📊 科研分析报告")
                    st.markdown(result.get("research_report", "报告生成失败"))
                    
                else:
                    st.error(f"❌ 证据包生成失败: {response.text}")
                    
            except Exception as e:
                st.error(f"❌ 发生错误: {str(e)}")

def check_api_status():
    """检查后端API状态"""
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_database_status():
    """检查数据库状态"""
    try:
        response = requests.get(f"{API_BASE_URL}/patients", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_model_training_status():
    """检查模型训练服务状态"""
    try:
        response = requests.get(f"{API_BASE_URL}/model_training/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("success", False)
        return False
    except:
        return False

def settings_page():
    """设置页面"""
    st.markdown('<h2 class="section-header">⚙️ 系统设置</h2>', unsafe_allow_html=True)
    
    # 系统状态概览
    st.markdown("### 📊 系统状态")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("系统版本", config.VERSION)
    
    with col2:
        api_status = "正常" if check_api_status() else "异常"
        st.metric("后端API", api_status)
    
    with col3:
        db_status = "正常" if check_database_status() else "异常"
        st.metric("数据库", db_status)
    
    with col4:
        model_status = "正常" if check_model_training_status() else "异常"
        st.metric("模型训练", model_status)
    
    st.markdown("---")
    
    # API配置状态（只显示，不编辑）
    st.markdown("### 🔧 API配置状态")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**DASHSCOPE API**")
        if config.is_api_configured("dashscope"):
            st.success(f"✅ 已配置: {config.get_masked_api_key('dashscope')}")
        else:
            st.error("❌ 未配置")
    
    with col2:
        st.markdown("**OpenAI API**")
        if config.is_api_configured("openai"):
            st.success(f"✅ 已配置: {config.get_masked_api_key('openai')}")
        else:
            st.warning("⚠️ 未配置（可选）")
    
    # 服务配置
    st.markdown("### 🌐 服务配置")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**后端API地址**")
        st.code(config.API_BASE_URL)
    
    with col2:
        st.markdown(f"**模型训练服务**")
        st.code(config.MODEL_TRAINING_URL)
    
    st.markdown("---")
    
    # API测试
    st.markdown("### 🧪 连接测试")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 测试后端API", use_container_width=True):
            with st.spinner("正在测试后端API..."):
                try:
                    response = requests.get(f"{API_BASE_URL}/", timeout=5)
                    if response.status_code == 200:
                        st.success("✅ 后端API连接正常")
                    else:
                        st.error(f"❌ 后端API响应异常: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ 后端API连接失败: {str(e)}")
    
    with col2:
        if st.button("🤖 测试模型训练API", use_container_width=True):
            with st.spinner("正在测试模型训练API..."):
                try:
                    response = requests.get(f"{API_BASE_URL}/model_training/status", timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("success"):
                            st.success("✅ 模型训练API连接正常")
                        else:
                            st.warning(f"⚠️ 模型训练服务状态: {data.get('status', 'unknown')}")
                    else:
                        st.error(f"❌ 模型训练API响应异常: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ 模型训练API连接失败: {str(e)}")
    
    # 系统信息
    st.markdown("### ℹ️ 系统信息")
    
    info_col1, info_col2 = st.columns(2)
    
    with info_col1:
        st.markdown("""
        **功能特性:**
        - ✅ 患者报告生成
        - ✅ AI智能聊天
        - ✅ 报告优化
        - ✅ 症状分析
        - ✅ 模型训练
        - ✅ 历史记录管理
        """)
    
    with info_col2:
        st.markdown("""
        **技术栈:**
        - 🐍 Python + Streamlit
        - 🚀 FastAPI 后端
        - 🤖 阿里云通义千问
        - 📊 SQLite 数据库
        - 🎨 现代化UI设计
        """)
    
    # 配置说明
    st.markdown("### 📝 配置说明")
    st.info("""
    **API密钥配置:**
    - 系统已预配置DASHSCOPE API密钥，无需手动设置
    - 如需修改配置，请编辑 `config.py` 文件
    - 生产环境建议使用环境变量设置敏感信息
    
    **服务地址:**
    - 后端API: 本地服务，端口8000
    - 模型训练: 本地模拟服务，端口7003
    - 生产环境可修改为实际服务器地址
    """)

if __name__ == "__main__":
    main()
