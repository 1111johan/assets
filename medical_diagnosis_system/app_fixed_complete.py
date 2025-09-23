"""
修复版完整医疗AI科研系统前端 - 现代化UI + 完整功能
解决JavaScript错误和组件导入问题
"""

import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import os

# 配置页面
st.set_page_config(
    page_title="医疗AI科研系统",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API配置
API_BASE_URL = "http://127.0.0.1:8000"

# 现代化CSS样式
def load_modern_css():
    """加载现代化CSS样式"""
    st.markdown("""
    <style>
    :root {
        --background: #fafafa;
        --foreground: #0f0f0f;
        --card: #ffffff;
        --primary: #6366f1;
        --primary-foreground: #ffffff;
        --secondary: #f1f5f9;
        --secondary-foreground: #0f172a;
        --muted: #f8fafc;
        --muted-foreground: #64748b;
        --accent: #f1f5f9;
        --accent-foreground: #0f172a;
        --destructive: #ef4444;
        --destructive-foreground: #ffffff;
        --border: #e2e8f0;
        --input: #ffffff;
        --ring: #6366f1;
        --radius: 0.5rem;
    }
    
    .main-header {
        background: linear-gradient(135deg, var(--primary) 0%, #8b5cf6 100%);
        color: white;
        text-align: center;
        padding: 2rem 0;
        border-radius: var(--radius);
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
        color: var(--primary);
        padding: 1rem 0;
        border-left: 4px solid var(--primary);
        padding-left: 1rem;
        margin: 1.5rem 0;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    .modern-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
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
        background: var(--muted);
        padding: 1.5rem;
        border-radius: var(--radius);
        border: 1px solid var(--border);
        margin: 1rem 0;
    }
    
    .success-message {
        background: #dcfce7;
        color: #166534;
        padding: 1rem;
        border-radius: var(--radius);
        border: 1px solid #bbf7d0;
        margin: 1rem 0;
    }
    
    .error-message {
        background: #fef2f2;
        color: #dc2626;
        padding: 1rem;
        border-radius: var(--radius);
        border: 1px solid #fecaca;
        margin: 1rem 0;
    }
    
    .warning-message {
        background: #fefce8;
        color: #ca8a04;
        padding: 1rem;
        border-radius: var(--radius);
        border: 1px solid #fde68a;
        margin: 1rem 0;
    }
    
    .info-message {
        background: #eff6ff;
        color: #1d4ed8;
        padding: 1rem;
        border-radius: var(--radius);
        border: 1px solid #bfdbfe;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--muted-foreground);
        margin: 0.5rem 0 0 0;
    }
    
    .sidebar .sidebar-content {
        padding: 1rem;
    }
    
    .sidebar .sidebar-content .nav-item {
        padding: 0.75rem 1rem;
        margin: 0.25rem 0;
        border-radius: var(--radius);
        cursor: pointer;
        transition: all 0.2s ease-in-out;
    }
    
    .sidebar .sidebar-content .nav-item:hover {
        background: var(--accent);
        color: var(--accent-foreground);
    }
    
    .sidebar .sidebar-content .nav-item.active {
        background: var(--primary);
        color: var(--primary-foreground);
    }
    
    .stButton > button {
        background: var(--primary);
        color: var(--primary-foreground);
        border: none;
        border-radius: var(--radius);
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
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 0.5rem 0.75rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--ring);
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
    }
    
    .stTextArea > div > div > textarea {
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 0.5rem 0.75rem;
    }
    
    .stSelectbox > div > div > select {
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 0.5rem 0.75rem;
    }
    
    .stNumberInput > div > div > input {
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 0.5rem 0.75rem;
    }
    
    .stExpander > div {
        border: 1px solid var(--border);
        border-radius: var(--radius);
    }
    
    .stExpander > div > div {
        background: var(--muted);
        border-radius: var(--radius);
    }
    
    .stDataFrame {
        border: 1px solid var(--border);
        border-radius: var(--radius);
    }
    
    .stAlert {
        border-radius: var(--radius);
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
    
    # 加载CSS样式
    load_modern_css()
    
    # 初始化session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "新增病人报告"
    
    # 主标题
    st.markdown("""
    <div class="main-header">
        <h1>🏥 术前病情预测 & 中西医结合诊疗报告生成系统</h1>
        <p>AI-Powered Medical Diagnostic & Report Generation System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 侧边栏导航
    with st.sidebar:
        st.markdown("### 🧭 导航菜单")
        
        # 导航选项
        nav_options = [
            "新增病人报告", "查看历史记录", "AI对话助手", "报告整理优化", "症状分析", 
            "科研数据分析", "模型训练", "证据包生成", "系统设置"
        ]
        
        selected_page = st.selectbox(
            "选择功能",
            nav_options,
            index=nav_options.index(st.session_state.current_page) if st.session_state.current_page in nav_options else 0
        )
        
        # 更新当前页面
        st.session_state.current_page = selected_page
        
        # 系统状态
        st.markdown("---")
        st.markdown("### 📊 系统状态")
        
        # 检查后端连接
        try:
            response = requests.get(f"{API_BASE_URL}/", timeout=5)
            if response.status_code == 200:
                st.success("✅ 后端API正常")
            else:
                st.error("❌ 后端API异常")
        except:
            st.error("❌ 后端API离线")
    
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
                        # 准备数据 - 修复API格式
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
                        
                        # 调用API生成报告
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
                # 搜索功能
                search_term = st.text_input("🔍 搜索患者", placeholder="输入患者姓名或ID")
                
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
                            st.write(f"**性别**: {patient.get('gender', 'N/A')}")
                        
                        with col2:
                            st.write(f"**主诉**: {patient.get('chief_complaint', 'N/A')}")
                            st.write(f"**创建时间**: {patient.get('created_at', 'N/A')}")
                        
                        # 查看详情按钮
                        if st.button(f"查看详情", key=f"view_{patient.get('id')}"):
                            view_patient_details(patient.get('id'))
            else:
                st.info("📝 暂无患者记录")
        else:
            st.error(f"❌ 获取患者列表失败: {response.text}")
            
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
    """模型训练页面"""
    st.markdown('<h2 class="section-header">🤖 模型训练</h2>', unsafe_allow_html=True)
    
    st.markdown("### 🎯 选择训练任务")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 诊断分类模型")
        if st.button("开始训练诊断模型", type="primary"):
            with st.spinner("正在训练诊断模型..."):
                try:
                    response = requests.post(f"{API_BASE_URL}/research/train_diagnostic_model", 
                                           params={
                                               "file_path": "research_data/sample_medical_data.csv",
                                               "target_column": "diagnosis_target",
                                               "model_type": "random_forest"
                                           })
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ 诊断模型训练完成！")
                        st.json(result)
                    else:
                        st.error(f"❌ 模型训练失败: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")
    
    with col2:
        st.markdown("#### 生存分析模型")
        if st.button("开始训练生存模型", type="primary"):
            with st.spinner("正在训练生存分析模型..."):
                try:
                    response = requests.post(f"{API_BASE_URL}/research/train_survival_model", 
                                           params={
                                               "file_path": "research_data/sample_medical_data.csv",
                                               "target_column": "survival_time",
                                               "model_type": "cox"
                                           })
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("✅ 生存分析模型训练完成！")
                        st.json(result)
                    else:
                        st.error(f"❌ 模型训练失败: {response.text}")
                        
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

def settings_page():
    """设置页面"""
    st.markdown('<h2 class="section-header">⚙️ 系统设置</h2>', unsafe_allow_html=True)
    
    st.markdown("### 🔧 API配置")
    
    # API密钥设置
    current_api_key = st.text_input("DASHSCOPE API Key", value=os.getenv("DASHSCOPE_API_KEY", ""), type="password")
    
    if st.button("💾 保存设置"):
        os.environ["DASHSCOPE_API_KEY"] = current_api_key
        st.success("✅ 设置已保存！")
    
    # API测试
    st.markdown("### 🧪 API测试")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("测试后端API"):
            try:
                response = requests.get(f"{API_BASE_URL}/", timeout=5)
                if response.status_code == 200:
                    st.success("✅ 后端API连接正常")
                else:
                    st.error("❌ 后端API连接失败")
            except Exception as e:
                st.error(f"❌ 连接错误: {str(e)}")
    
    with col2:
        if st.button("测试AI服务"):
            try:
                response = requests.post(f"{API_BASE_URL}/chat", json={
                    "message": "测试消息",
                    "conversation_history": []
                })
                if response.status_code == 200:
                    st.success("✅ AI服务连接正常")
                else:
                    st.error("❌ AI服务连接失败")
            except Exception as e:
                st.error(f"❌ 连接错误: {str(e)}")

if __name__ == "__main__":
    main()
