"""
现代化头部组件 - 基于medical-diagnostic-system设计
"""

import streamlit as st
from typing import Optional

class ModernHeader:
    """现代化头部组件"""
    
    def __init__(self):
        self.title = "术前病情预测 & 中西医结合诊疗报告生成系统"
        self.subtitle = "AI-Powered Medical Diagnostic & Report Generation System"
    
    def render(self, show_search: bool = True, show_theme_toggle: bool = True):
        """渲染头部组件"""
        
        # 头部容器
        st.markdown("""
        <div class="main-header">
            <div style="display: flex; align-items: center; justify-content: space-between; max-width: 1200px; margin: 0 auto;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="display: flex; align-items: center; justify-content: center; width: 3rem; height: 3rem; background: linear-gradient(135deg, var(--primary), var(--medical-gradient-end)); border-radius: 0.75rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
                        <span style="color: white; font-size: 1.5rem;">🏥</span>
                    </div>
                    <div>
                        <h1 style="margin: 0; font-size: 1.5rem; font-weight: 700; color: var(--foreground); background: linear-gradient(135deg, var(--primary), var(--medical-gradient-end)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                            """ + self.title + """
                        </h1>
                        <p style="margin: 0; font-size: 0.875rem; color: var(--muted-foreground); font-weight: 500;">
                            """ + self.subtitle + """
                        </p>
                    </div>
                </div>
                
                <div style="display: flex; align-items: center; gap: 1rem;">
        """, unsafe_allow_html=True)
        
        # 搜索框
        if show_search:
            search_query = st.text_input(
                "搜索患者、报告...",
                placeholder="搜索患者、报告...",
                key="header_search",
                help="搜索患者信息或报告内容"
            )
        
        # 主题切换按钮
        if show_theme_toggle:
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("🌞", key="theme_light", help="浅色主题"):
                    st.session_state.theme = "light"
                    st.rerun()
            with col2:
                if st.button("🌙", key="theme_dark", help="深色主题"):
                    st.session_state.theme = "dark"
                    st.rerun()
        
        # 通知按钮
        if st.button("🔔", key="notifications", help="通知"):
            st.info("暂无新通知")
        
        # 设置按钮
        if st.button("⚙️", key="settings", help="设置"):
            st.info("设置功能开发中...")
        
        # 用户信息
        st.markdown("""
                    <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem; background: var(--muted); border-radius: var(--radius);">
                        <div style="width: 2rem; height: 2rem; background: var(--primary); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                            <span style="color: white; font-size: 0.875rem; font-weight: 600;">医</span>
                        </div>
                        <div>
                            <div style="font-size: 0.875rem; font-weight: 500; color: var(--foreground);">医生账户</div>
                            <div style="font-size: 0.75rem; color: var(--muted-foreground);">在线</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 系统状态栏
        st.markdown("""
        <div style="background: var(--card); border-bottom: 1px solid var(--border); padding: 0.5rem 2rem; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; justify-content: space-between; max-width: 1200px; margin: 0 auto;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.25rem 0.75rem; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 9999px;">
                        <div style="width: 0.5rem; height: 0.5rem; background: var(--medical-success); border-radius: 50%; animation: pulse 2s infinite;"></div>
                        <span style="font-size: 0.75rem; font-weight: 500; color: var(--medical-success);">系统正常</span>
                    </div>
                    <div style="font-size: 0.75rem; color: var(--muted-foreground);">
                        <span>在线用户: 24</span>
                        <span style="margin: 0 0.5rem;">•</span>
                        <span>活跃模型: 3</span>
                        <span style="margin: 0 0.5rem;">•</span>
                        <span>今日报告: 156</span>
                    </div>
                </div>
                <div style="font-size: 0.75rem; color: var(--muted-foreground);">
                    """ + st.session_state.get('current_time', '') + """
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def update_time(self):
        """更新时间显示"""
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.current_time = current_time

def render_modern_header(show_search: bool = True, show_theme_toggle: bool = True):
    """渲染现代化头部的便捷函数"""
    header = ModernHeader()
    header.update_time()
    header.render(show_search, show_theme_toggle)
