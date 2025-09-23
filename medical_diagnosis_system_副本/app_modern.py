"""
现代化医疗AI科研系统前端 - 基于medical-diagnostic-system设计
集成现代化UI组件和布局
"""

import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import os
import sys

# 添加组件路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入现代化组件
from components import render_modern_layout, ModernLayout

# 配置页面
st.set_page_config(
    page_title="医疗AI科研系统",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API配置
API_BASE_URL = "http://127.0.0.1:8000"

# 加载现代化CSS样式
def load_modern_css():
    """加载现代化CSS样式"""
    css_file = os.path.join(os.path.dirname(__file__), "styles", "modern_theme.css")
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # 内联CSS作为备用
        st.markdown("""
        <style>
        :root {
            --background: #fafafa;
            --foreground: #0f0f0f;
            --card: #ffffff;
            --primary: #6366f1;
            --border: #e2e8f0;
            --radius: 0.5rem;
        }
        .modern-card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: var(--radius);
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
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
    if 'theme' not in st.session_state:
        st.session_state.theme = "light"
    
    # 渲染现代化布局
    selected_page, layout = render_modern_layout(
        active_page=st.session_state.get('current_page', 'new_patient'),
        show_sidebar=True,
        show_header=True,
        show_search=True,
        show_theme_toggle=True
    )
    
    # 更新当前页面
    st.session_state.current_page = selected_page
    
    # 页面路由
    if selected_page == "new_patient":
        new_patient_page_modern(layout)
    elif selected_page == "history":
        history_page_modern(layout)
    elif selected_page == "ai_chat":
        ai_chat_page_modern(layout)
    elif selected_page == "report_optimize":
        report_optimize_page_modern(layout)
    elif selected_page == "symptom_analysis":
        symptom_analysis_page_modern(layout)
    elif selected_page == "research_analysis":
        research_analysis_page_modern(layout)
    elif selected_page == "model_training":
        model_training_page_modern(layout)
    elif selected_page == "evidence_bundle":
        evidence_bundle_page_modern(layout)
    elif selected_page == "settings":
        settings_page_modern(layout)

def new_patient_page_modern(layout: ModernLayout):
    """现代化新增病人页面"""
    
    # 页面头部
    layout.render_page_header(
        title="新增病人诊疗报告",
        description="创建新的中西医结合诊疗报告",
        icon="📝"
    )
    
    # 使用两列布局
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # 基本信息卡片
        layout.render_card(
            title="基本信息",
            icon="👤",
            content="""
            <div style="display: grid; gap: 1rem;">
                <div>
                    <label style="display: block; font-size: 0.875rem; font-weight: 500; color: var(--muted-foreground); margin-bottom: 0.5rem;">姓名 *</label>
                    <input type="text" placeholder="请输入病人姓名" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--card);">
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                    <div>
                        <label style="display: block; font-size: 0.875rem; font-weight: 500; color: var(--muted-foreground); margin-bottom: 0.5rem;">年龄 *</label>
                        <input type="number" placeholder="年龄" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--card);">
                    </div>
                    <div>
                        <label style="display: block; font-size: 0.875rem; font-weight: 500; color: var(--muted-foreground); margin-bottom: 0.5rem;">性别 *</label>
                        <select style="width: 100%; padding: 0.75rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--card);">
                            <option>男</option>
                            <option>女</option>
                        </select>
                    </div>
                </div>
            </div>
            """,
            card_type="primary"
        )
    
    with col2:
        # 临床信息卡片
        layout.render_card(
            title="临床信息",
            icon="🏥",
            content="""
            <div style="display: grid; gap: 1rem;">
                <div>
                    <label style="display: block; font-size: 0.875rem; font-weight: 500; color: var(--muted-foreground); margin-bottom: 0.5rem;">主诉 *</label>
                    <textarea placeholder="请详细描述主要症状和持续时间" rows="3" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--card); resize: none;"></textarea>
                </div>
                <div>
                    <label style="display: block; font-size: 0.875rem; font-weight: 500; color: var(--muted-foreground); margin-bottom: 0.5rem;">既往病史</label>
                    <textarea placeholder="请描述相关既往病史、手术史、过敏史等" rows="3" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--card); resize: none;"></textarea>
                </div>
            </div>
            """,
            card_type="success"
        )
    
    # 检查结果卡片
    layout.render_card(
        title="检查结果",
        icon="🔬",
        content="""
        <div style="display: grid; gap: 1rem;">
            <div>
                <h4 style="margin: 0 0 1rem 0; font-size: 1rem; font-weight: 600; color: var(--foreground);">实验室检查</h4>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                    <div>
                        <label style="display: block; font-size: 0.75rem; font-weight: 500; color: var(--muted-foreground); margin-bottom: 0.5rem;">ALT (U/L)</label>
                        <input type="number" placeholder="40.0" step="0.01" style="width: 100%; padding: 0.5rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--card); text-align: center;">
                    </div>
                    <div>
                        <label style="display: block; font-size: 0.75rem; font-weight: 500; color: var(--muted-foreground); margin-bottom: 0.5rem;">AST (U/L)</label>
                        <input type="number" placeholder="40.0" step="0.01" style="width: 100%; padding: 0.5rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--card); text-align: center;">
                    </div>
                    <div>
                        <label style="display: block; font-size: 0.75rem; font-weight: 500; color: var(--muted-foreground); margin-bottom: 0.5rem;">AFP (ng/mL)</label>
                        <input type="number" placeholder="20.0" step="0.01" style="width: 100%; padding: 0.5rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--card); text-align: center;">
                    </div>
                </div>
            </div>
            <div>
                <h4 style="margin: 0 0 1rem 0; font-size: 1rem; font-weight: 600; color: var(--foreground);">影像学检查</h4>
                <textarea placeholder="请描述CT、MRI、超声等影像学检查结果..." rows="3" style="width: 100%; padding: 0.75rem; border: 1px solid var(--border); border-radius: var(--radius); background: var(--card); resize: none;"></textarea>
            </div>
        </div>
        """,
        card_type="warning"
    )
    
    # 操作按钮
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🔍 生成报告", type="primary", use_container_width=True):
            st.success("报告生成中...")
    with col2:
        if st.button("💾 保存草稿", use_container_width=True):
            st.info("草稿已保存")
    with col3:
        if st.button("🔄 重置表单", use_container_width=True):
            st.rerun()

def history_page_modern(layout: ModernLayout):
    """现代化历史记录页面"""
    
    # 页面头部
    layout.render_page_header(
        title="查看历史记录",
        description="浏览和管理患者历史记录",
        icon="📚"
    )
    
    # 搜索和筛选
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_query = st.text_input("🔍 搜索患者", placeholder="输入患者姓名或ID")
    with col2:
        date_range = st.date_input("📅 日期范围")
    with col3:
        status_filter = st.selectbox("📊 状态筛选", ["全部", "已完成", "草稿", "待审核"])
    
    # 患者列表
    layout.render_card(
        title="患者记录",
        icon="👥",
        content="""
        <div style="overflow-x: auto;">
            <table class="modern-table" style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: var(--muted);">
                        <th style="padding: 0.75rem; text-align: left; font-weight: 600;">患者ID</th>
                        <th style="padding: 0.75rem; text-align: left; font-weight: 600;">姓名</th>
                        <th style="padding: 0.75rem; text-align: left; font-weight: 600;">年龄</th>
                        <th style="padding: 0.75rem; text-align: left; font-weight: 600;">诊断</th>
                        <th style="padding: 0.75rem; text-align: left; font-weight: 600;">创建时间</th>
                        <th style="padding: 0.75rem; text-align: left; font-weight: 600;">状态</th>
                        <th style="padding: 0.75rem; text-align: left; font-weight: 600;">操作</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding: 0.75rem; border-top: 1px solid var(--border);">#001</td>
                        <td style="padding: 0.75rem; border-top: 1px solid var(--border);">张三</td>
                        <td style="padding: 0.75rem; border-top: 1px solid var(--border);">45</td>
                        <td style="padding: 0.75rem; border-top: 1px solid var(--border);">肝癌</td>
                        <td style="padding: 0.75rem; border-top: 1px solid var(--border);">2024-01-15</td>
                        <td style="padding: 0.75rem; border-top: 1px solid var(--border);">
                            <span class="status-success">已完成</span>
                        </td>
                        <td style="padding: 0.75rem; border-top: 1px solid var(--border);">
                            <button style="padding: 0.25rem 0.5rem; background: var(--primary); color: white; border: none; border-radius: 0.25rem; font-size: 0.75rem;">查看</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        """,
        card_type="default"
    )

def ai_chat_page_modern(layout: ModernLayout):
    """现代化AI对话页面"""
    
    # 页面头部
    layout.render_page_header(
        title="AI对话助手",
        description="智能医疗对话和咨询",
        icon="🤖"
    )
    
    # 聊天界面
    layout.render_card(
        title="智能对话",
        icon="💬",
        content="""
        <div style="height: 400px; border: 1px solid var(--border); border-radius: var(--radius); padding: 1rem; background: var(--muted); overflow-y: auto;">
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <div style="width: 2rem; height: 2rem; background: var(--primary); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <span style="color: white; font-size: 0.875rem;">AI</span>
                    </div>
                    <span style="font-weight: 500;">医疗AI助手</span>
                </div>
                <div style="background: var(--card); padding: 0.75rem; border-radius: var(--radius); margin-left: 2.5rem;">
                    您好！我是医疗AI助手，可以为您提供医疗咨询、症状分析、报告解读等服务。请问有什么可以帮助您的吗？
                </div>
            </div>
        </div>
        """,
        card_type="primary"
    )
    
    # 输入框
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("输入您的问题...", placeholder="请输入您的问题")
    with col2:
        if st.button("发送", type="primary", use_container_width=True):
            if user_input:
                st.success("消息已发送")

def research_analysis_page_modern(layout: ModernLayout):
    """现代化科研分析页面"""
    
    # 页面头部
    layout.render_page_header(
        title="科研数据分析",
        description="数据分析和探索性数据分析(EDA)",
        icon="🔬"
    )
    
    # 指标卡片
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        layout.render_metric_card("总患者数", "1,234", "+12%", "positive", "👥")
    with col2:
        layout.render_metric_card("完成分析", "856", "+8%", "positive", "✅")
    with col3:
        layout.render_metric_card("模型准确率", "94.2%", "+2.1%", "positive", "🎯")
    with col4:
        layout.render_metric_card("数据质量", "98.5%", "+0.5%", "positive", "⭐")
    
    # 分析工具
    layout.render_card(
        title="数据分析工具",
        icon="📊",
        content="""
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;">
            <div>
                <h4 style="margin: 0 0 1rem 0; font-size: 1rem; font-weight: 600;">数据上传</h4>
                <div style="border: 2px dashed var(--border); border-radius: var(--radius); padding: 2rem; text-align: center; background: var(--muted);">
                    <div style="font-size: 2rem; margin-bottom: 1rem;">📁</div>
                    <p style="margin: 0; color: var(--muted-foreground);">拖拽文件到此处或点击上传</p>
                </div>
            </div>
            <div>
                <h4 style="margin: 0 0 1rem 0; font-size: 1rem; font-weight: 600;">分析类型</h4>
                <div style="display: grid; gap: 0.5rem;">
                    <button style="padding: 0.75rem; background: var(--primary); color: white; border: none; border-radius: var(--radius); text-align: left;">描述性统计</button>
                    <button style="padding: 0.75rem; background: var(--secondary); color: var(--secondary-foreground); border: 1px solid var(--border); border-radius: var(--radius); text-align: left;">相关性分析</button>
                    <button style="padding: 0.75rem; background: var(--secondary); color: var(--secondary-foreground); border: 1px solid var(--border); border-radius: var(--radius); text-align: left;">分布分析</button>
                </div>
            </div>
        </div>
        """,
        card_type="success"
    )

def model_training_page_modern(layout: ModernLayout):
    """现代化模型训练页面"""
    
    # 页面头部
    layout.render_page_header(
        title="模型训练",
        description="机器学习模型训练和管理",
        icon="🤖"
    )
    
    # 模型状态
    col1, col2 = st.columns([1, 1])
    with col1:
        layout.render_card(
            title="诊断分类模型",
            icon="🎯",
            content="""
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 1rem;">✅</div>
                <p style="margin: 0 0 1rem 0; font-weight: 600;">模型已训练完成</p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; font-size: 0.875rem;">
                    <div>准确率: 94.2%</div>
                    <div>精确率: 92.8%</div>
                    <div>召回率: 91.5%</div>
                    <div>F1分数: 92.1%</div>
                </div>
            </div>
            """,
            card_type="success"
        )
    
    with col2:
        layout.render_card(
            title="生存分析模型",
            icon="📈",
            content="""
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 1rem;">🔄</div>
                <p style="margin: 0 0 1rem 0; font-weight: 600;">训练中...</p>
                <div style="background: var(--muted); border-radius: var(--radius); padding: 0.5rem;">
                    <div style="background: var(--primary); height: 0.5rem; border-radius: var(--radius); width: 65%;"></div>
                </div>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.875rem; color: var(--muted-foreground);">65% 完成</p>
            </div>
            """,
            card_type="warning"
        )

def evidence_bundle_page_modern(layout: ModernLayout):
    """现代化证据包生成页面"""
    
    # 页面头部
    layout.render_page_header(
        title="证据包生成",
        description="科研级证据包生成和分析",
        icon="📋"
    )
    
    # 分析类型选择
    layout.render_card(
        title="分析类型",
        icon="🔍",
        content="""
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
            <button style="padding: 1rem; background: var(--primary); color: white; border: none; border-radius: var(--radius); text-align: center;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🔬</div>
                <div style="font-weight: 600;">综合分析</div>
            </button>
            <button style="padding: 1rem; background: var(--secondary); color: var(--secondary-foreground); border: 1px solid var(--border); border-radius: var(--radius); text-align: center;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📊</div>
                <div style="font-weight: 600;">样本分析</div>
            </button>
            <button style="padding: 1rem; background: var(--secondary); color: var(--secondary-foreground); border: 1px solid var(--border); border-radius: var(--radius); text-align: center;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🌿</div>
                <div style="font-weight: 600;">中西医结合</div>
            </button>
        </div>
        """,
        card_type="primary"
    )

def report_optimize_page_modern(layout: ModernLayout):
    """现代化报告优化页面"""
    layout.render_page_header("报告整理优化", "AI报告优化和整理", "📊")

def symptom_analysis_page_modern(layout: ModernLayout):
    """现代化症状分析页面"""
    layout.render_page_header("症状分析", "智能症状分析", "🔍")

def settings_page_modern(layout: ModernLayout):
    """现代化设置页面"""
    layout.render_page_header("系统设置", "配置管理", "⚙️")

if __name__ == "__main__":
    main()
