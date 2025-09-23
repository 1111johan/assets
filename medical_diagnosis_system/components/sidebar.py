"""
现代化侧边栏组件 - 基于medical-diagnostic-system设计
"""

import streamlit as st
from typing import Dict, List, Optional

class ModernSidebar:
    """现代化侧边栏组件"""
    
    def __init__(self):
        self.menu_items = [
            {
                "id": "new_patient",
                "label": "新增病人报告",
                "icon": "📝",
                "description": "创建新的诊疗报告"
            },
            {
                "id": "history",
                "label": "查看历史记录", 
                "icon": "📚",
                "description": "浏览患者历史记录"
            },
            {
                "id": "ai_chat",
                "label": "AI对话助手",
                "icon": "🤖",
                "description": "智能医疗对话"
            },
            {
                "id": "report_optimize",
                "label": "报告整理优化",
                "icon": "📊",
                "description": "AI报告优化"
            },
            {
                "id": "symptom_analysis",
                "label": "症状分析",
                "icon": "🔍",
                "description": "智能症状分析"
            },
            {
                "id": "research_analysis",
                "label": "科研数据分析",
                "icon": "🔬",
                "description": "数据分析和EDA"
            },
            {
                "id": "model_training",
                "label": "模型训练",
                "icon": "🤖",
                "description": "机器学习模型训练"
            },
            {
                "id": "evidence_bundle",
                "label": "证据包生成",
                "icon": "📋",
                "description": "科研级证据包生成"
            },
            {
                "id": "settings",
                "label": "系统设置",
                "icon": "⚙️",
                "description": "配置管理"
            }
        ]
    
    def render(self, active_page: str = "new_patient") -> str:
        """渲染侧边栏并返回选中的页面"""
        
        # 侧边栏标题
        st.sidebar.markdown("""
        <div class="sidebar-header">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                <div style="width: 2rem; height: 2rem; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 0.5rem; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-size: 1.25rem;">🏥</span>
                </div>
                <div>
                    <h2 style="margin: 0; font-size: 1.125rem; font-weight: 600; color: var(--sidebar-foreground);">医疗AI科研系统</h2>
                    <p style="margin: 0; font-size: 0.75rem; color: var(--muted-foreground);">Medical AI Research System</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 系统状态指示器
        st.sidebar.markdown("""
        <div style="padding: 0.75rem; background: var(--medical-surface); border-radius: var(--radius); margin-bottom: 1rem; border: 1px solid var(--border);">
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                <div style="width: 0.5rem; height: 0.5rem; background: var(--medical-success); border-radius: 50%; animation: pulse 2s infinite;"></div>
                <span style="font-size: 0.875rem; font-weight: 500; color: var(--medical-success);">系统运行正常</span>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: var(--muted-foreground);">
                <span>在线用户: 24</span>
                <span>活跃模型: 3</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 功能选择器
        st.sidebar.markdown("""
        <div style="margin-bottom: 1rem;">
            <label style="font-size: 0.75rem; font-weight: 500; color: var(--muted-foreground); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; display: block;">选择功能</label>
        </div>
        """, unsafe_allow_html=True)
        
        # 菜单项
        selected_page = active_page
        
        for item in self.menu_items:
            is_active = item["id"] == active_page
            active_class = "active" if is_active else ""
            
            # 创建菜单项
            if st.sidebar.button(
                f"{item['icon']} {item['label']}",
                key=f"sidebar_{item['id']}",
                help=item['description'],
                use_container_width=True
            ):
                selected_page = item["id"]
                st.rerun()
            
            # 添加活跃状态样式
            if is_active:
                st.sidebar.markdown(f"""
                <style>
                .stButton > button[kind="secondary"][data-testid="baseButton-secondary"]:nth-of-type({self.menu_items.index(item) + 1}) {{
                    background: rgba(99, 102, 241, 0.1) !important;
                    color: var(--sidebar-primary) !important;
                    border: 1px solid rgba(99, 102, 241, 0.2) !important;
                    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1) !important;
                }}
                </style>
                """, unsafe_allow_html=True)
        
        # 底部信息
        st.sidebar.markdown("""
        <div style="position: absolute; bottom: 1rem; left: 1rem; right: 1rem;">
            <div style="padding: 0.75rem; background: var(--muted); border-radius: var(--radius); text-align: center;">
                <div style="font-size: 0.75rem; color: var(--muted-foreground); margin-bottom: 0.25rem;">版本 1.0.0</div>
                <div style="font-size: 0.75rem; color: var(--muted-foreground);">© 2024 医疗AI科研系统</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        return selected_page
    
    def get_page_title(self, page_id: str) -> str:
        """获取页面标题"""
        for item in self.menu_items:
            if item["id"] == page_id:
                return item["label"]
        return "未知页面"
    
    def get_page_description(self, page_id: str) -> str:
        """获取页面描述"""
        for item in self.menu_items:
            if item["id"] == page_id:
                return item["description"]
        return ""

def render_modern_sidebar(active_page: str = "new_patient") -> str:
    """渲染现代化侧边栏的便捷函数"""
    sidebar = ModernSidebar()
    return sidebar.render(active_page)
