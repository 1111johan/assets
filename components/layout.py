"""
现代化页面布局组件 - 基于medical-diagnostic-system设计
"""

import streamlit as st
from typing import Optional, Dict, Any
from .sidebar import render_modern_sidebar
from .header import render_modern_header

class ModernLayout:
    """现代化页面布局组件"""
    
    def __init__(self):
        self.sidebar_width = 280
        self.header_height = 120
        
    def render_sidebar(self, active_page: str = "new_patient") -> str:
        """渲染侧边栏"""
        return render_modern_sidebar(active_page)
    
    def render_header(self, show_search: bool = True, show_theme_toggle: bool = True):
        """渲染头部"""
        render_modern_header(show_search, show_theme_toggle)
    
    def render_page_header(self, title: str, description: str = "", icon: str = "📋"):
        """渲染页面头部"""
        st.markdown(f"""
        <div class="medical-card" style="margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                <div style="width: 2.5rem; height: 2.5rem; background: linear-gradient(135deg, var(--primary), var(--medical-gradient-end)); border-radius: 0.5rem; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-size: 1.25rem;">{icon}</span>
                </div>
                <div>
                    <h2 style="margin: 0; font-size: 1.5rem; font-weight: 600; color: var(--foreground);">{title}</h2>
                    {f'<p style="margin: 0; font-size: 0.875rem; color: var(--muted-foreground);">{description}</p>' if description else ''}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_card(self, title: str = "", content: str = "", icon: str = "", 
                   card_type: str = "default", actions: list = None) -> None:
        """渲染卡片组件"""
        
        # 卡片类型样式
        card_styles = {
            "default": "background: var(--card); border: 1px solid var(--border);",
            "primary": "background: linear-gradient(135deg, rgba(99, 102, 241, 0.05), rgba(139, 92, 246, 0.05)); border: 1px solid rgba(99, 102, 241, 0.2);",
            "success": "background: linear-gradient(135deg, rgba(16, 185, 129, 0.05), rgba(34, 197, 94, 0.05)); border: 1px solid rgba(16, 185, 129, 0.2);",
            "warning": "background: linear-gradient(135deg, rgba(245, 158, 11, 0.05), rgba(251, 191, 36, 0.05)); border: 1px solid rgba(245, 158, 11, 0.2);",
            "error": "background: linear-gradient(135deg, rgba(239, 68, 68, 0.05), rgba(248, 113, 113, 0.05)); border: 1px solid rgba(239, 68, 68, 0.2);"
        }
        
        style = card_styles.get(card_type, card_styles["default"])
        
        st.markdown(f"""
        <div class="modern-card" style="{style} padding: 1.5rem; margin-bottom: 1rem; border-radius: var(--radius);">
            {f'''
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1rem;">
                {f'<span style="font-size: 1.25rem;">{icon}</span>' if icon else ''}
                <h3 style="margin: 0; font-size: 1.125rem; font-weight: 600; color: var(--foreground);">{title}</h3>
            </div>
            ''' if title else ''}
            <div style="color: var(--foreground);">
                {content}
            </div>
            {f'''
            <div style="display: flex; gap: 0.5rem; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border);">
                {''.join([f'<button class="modern-button modern-button-{action.get("type", "secondary")}" style="padding: 0.5rem 1rem; font-size: 0.875rem;">{action["label"]}</button>' for action in actions])}
            </div>
            ''' if actions else ''}
        </div>
        """, unsafe_allow_html=True)
    
    def render_metric_card(self, title: str, value: str, change: str = "", 
                          change_type: str = "neutral", icon: str = ""):
        """渲染指标卡片"""
        
        change_colors = {
            "positive": "var(--medical-success)",
            "negative": "var(--medical-error)", 
            "neutral": "var(--muted-foreground)"
        }
        
        change_color = change_colors.get(change_type, change_colors["neutral"])
        
        st.markdown(f"""
        <div class="medical-card" style="text-align: center;">
            {f'<div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>' if icon else ''}
            <div style="font-size: 2rem; font-weight: 700; color: var(--foreground); margin-bottom: 0.25rem;">{value}</div>
            <div style="font-size: 0.875rem; font-weight: 500; color: var(--muted-foreground); margin-bottom: 0.5rem;">{title}</div>
            {f'<div style="font-size: 0.75rem; color: {change_color};">{change}</div>' if change else ''}
        </div>
        """, unsafe_allow_html=True)
    
    def render_loading_state(self, message: str = "加载中..."):
        """渲染加载状态"""
        st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 3rem; text-align: center;">
            <div class="loading-spinner" style="width: 2rem; height: 2rem; margin-bottom: 1rem;"></div>
            <p style="color: var(--muted-foreground); font-size: 0.875rem;">{message}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_empty_state(self, title: str, description: str, icon: str = "📋", 
                          action_label: str = "", action_callback: callable = None):
        """渲染空状态"""
        st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 3rem; text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;">{icon}</div>
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.25rem; font-weight: 600; color: var(--foreground);">{title}</h3>
            <p style="margin: 0 0 2rem 0; color: var(--muted-foreground); font-size: 0.875rem; max-width: 400px;">{description}</p>
            {f'''
            <button class="modern-button modern-button-primary" onclick="{action_callback.__name__ if action_callback else ''}()" style="padding: 0.75rem 1.5rem;">
                {action_label}
            </button>
            ''' if action_label else ''}
        </div>
        """, unsafe_allow_html=True)
    
    def render_tabs(self, tabs: list, active_tab: str = None) -> str:
        """渲染标签页"""
        if not tabs:
            return None
            
        # 创建标签页
        tab_labels = [tab["label"] for tab in tabs]
        tab_icons = [tab.get("icon", "") for tab in tabs]
        
        # 使用Streamlit的tabs组件
        tab_objects = st.tabs([f"{icon} {label}" for icon, label in zip(tab_icons, tab_labels)])
        
        # 返回选中的标签页索引
        return tab_objects

def render_modern_layout(active_page: str = "new_patient", 
                        show_sidebar: bool = True, 
                        show_header: bool = True,
                        show_search: bool = True,
                        show_theme_toggle: bool = True) -> tuple:
    """渲染现代化布局的便捷函数"""
    
    layout = ModernLayout()
    
    # 渲染侧边栏
    if show_sidebar:
        selected_page = layout.render_sidebar(active_page)
    else:
        selected_page = active_page
    
    # 渲染头部
    if show_header:
        layout.render_header(show_search, show_theme_toggle)
    
    return selected_page, layout
