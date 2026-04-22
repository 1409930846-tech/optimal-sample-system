"""
An Optimal Samples Selection System - Streamlit Web Version
1:1 Replica of Tkinter AI_system.py - Fixed Layout
"""

import streamlit as st
import random
from typing import List, Optional
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from algorithm_core import run_algorithm
from db_manager import DatabaseManager

st.set_page_config(
    page_title="An Optimal Samples Selection System",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

COLOR_BG = "#e8f4f8"
COLOR_PRIMARY = "#1565c0"
COLOR_SECONDARY = "#ff6f00"
COLOR_ACCENT = "#2e7d32"
COLOR_TEXT_DARK = "#1a1a2e"
COLOR_CARD = "#ffffff"
COLOR_GRAY = "#757575"
COLOR_ORANGE = "#ff6f00"

st.markdown(f"""
<script>
// 调试函数：记录按钮点击
function logClick(btnName) {{
    console.log('[DEBUG] Button clicked: ' + btnName);
}}

// 添加点击日志到所有自定义按钮
document.querySelectorAll('button').forEach(function(btn) {{
    btn.addEventListener('click', function() {{
        logClick(btn.textContent.trim());
    }});
}});
</script>
<style>
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    .stApp {{
        background-color: {COLOR_BG};
    }}

    /* Main Header Banner */
    .main-header {{
        background-color: {COLOR_PRIMARY};
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
        margin-top: 20px;
    }}
    .main-header h1 {{
        margin: 0;
        font-size: 20px;
        font-weight: bold;
        font-family: Arial, sans-serif;
        color: white;
    }}

    /* 页面整体向上移动 */
    .stApp {{
        padding-top: 0 !important;
    }}
    [data-testid="stMainBlockContainer"] {{
        padding-top: 0 !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }}
    .main {{
        padding-top: 0 !important;
    }}
    .stMainBlockContainer {{
        padding-top: 0 !important;
    }}

    /* Section Title - outside card */
    .section-header {{
        color: {COLOR_PRIMARY};
        font-size: 16px;
        font-weight: bold;
        font-family: Arial, sans-serif;
        margin-bottom: 5px;
    }}

    /* Parameter Input: Tkinter Style */
    .param-label {{
        color: {COLOR_TEXT_DARK};
        font-size: 15px;
        font-weight: bold;
        font-family: Arial, sans-serif;
    }}

    /* Parameter Input Card */
    .param-card {{
        background-color: white;
        border: 2px solid {COLOR_PRIMARY};
        border-radius: 0px;
        padding: 15px;
        margin-bottom: 15px;
    }}

    /* Streamlit Alert/StError font size */
    .stAlert {{
        font-size: 11px;
    }}
    .stAlert > div {{
        font-size: 11px;
    }}

    /* Text input white background - rectangle with blue border */
    .stTextInput > div > div > input {{
        background-color: white;
        border: 2px solid {COLOR_PRIMARY};
        border-radius: 0px;
        color: {COLOR_TEXT_DARK};
    }}

    /* Text area - rectangle with blue border */
    .stTextArea > div > div > textarea {{
        background-color: white;
        border: 2px solid {COLOR_PRIMARY};
        border-radius: 0px;
        color: {COLOR_TEXT_DARK};
        font-family: 'Courier New', monospace !important;
    }}

    /* Sample Display - Tkinter Style Text Box */
    .sample-display {{
        background-color: white;
        border: 2px solid {COLOR_PRIMARY};
        border-radius: 0px;
        padding: 8px;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        color: {COLOR_TEXT_DARK};
        min-height: 80px;
        width: 100%;
        box-sizing: border-box;
    }}

    /* Results Display - Tkinter Style Text Box */
    .results-display {{
        background-color: white;
        border: 2px solid {COLOR_PRIMARY};
        border-radius: 0px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        color: {COLOR_PRIMARY};
        min-height: 200px;
        width: 100%;
        box-sizing: border-box;
    }}

    /* File List Box - Tkinter Style */
    .file-list {{
        flex: 1;
        background-color: white;
        border: 2px solid {COLOR_PRIMARY};
        border-radius: 0px;
        padding: 5px;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        overflow-y: auto;
        box-sizing: border-box;
        width: 100%;
        min-height: 200px;
    }}
    .file-item {{
        padding: 3px 5px;
        border-bottom: 1px solid #ddd;
        color: {COLOR_TEXT_DARK};
    }}
    .file-item:last-child {{
        border-bottom: none;
    }}

    /* Sample Selection Area - Flex layout for vertical alignment */
    .sample-section {{
        display: flex;
        background-color: white;
        padding: 10px;
        align-items: stretch;
    }}
    .sample-btn-stack {{
        display: flex;
        flex-direction: column;
        gap: 8px;
        width: 200px;
    }}
    .sample-display-col {{
        flex: 1;
        display: flex;
        flex-direction: column;
        padding-left: 10px;
    }}

    /* File Operation Area - 2x2 Grid layout */
    .file-op-section {{
        display: flex;
        background-color: white;
        padding: 10px;
        align-items: stretch;
        min-height: 300px;
    }}
    .file-op-list-col {{
        flex: 1;
        display: flex;
        flex-direction: column;
        min-width: 0;
    }}
    .file-list {{
        flex: 1;
        background-color: white;
        border: 2px solid {COLOR_PRIMARY};
        border-radius: 0px;
        padding: 5px;
        overflow-y: auto;
        min-height: 200px;
    }}
    .file-item {{
        padding: 3px 0;
        font-family: Arial, sans-serif;
        font-size: 12px;
        color: {COLOR_TEXT_DARK};
    }}
    .file-op-btn-wrapper {{
        flex: 0 0 auto;
        display: flex;
        align-items: center;
        padding-left: 20px;
        margin-left: auto;
    }}
    .file-op-btn-grid {{
        display: flex;
        gap: 8px;
    }}
    .file-op-btn-stack {{
        display: flex;
        flex-direction: column;
        gap: 8px;
    }}
    .file-op-btn-left {{
        display: flex;
        flex-direction: column;
        gap: 8px;
        flex: 1;
    }}
    .file-op-btn-right {{
        display: flex;
        flex-direction: column;
        gap: 8px;
        flex: 1;
    }}

    /* Streamlit Button Override - Gray Style */
    .stButton > button {{
        border-radius: 0px !important;
        font-family: Arial !important;
        font-weight: bold !important;
        padding: 6px 10px !important;
        border: none !important;
        cursor: pointer !important;
        font-size: 11px !important;
        height: 50px !important;
        width: 100% !important;
    }}

    /* Gray buttons for sample selection */
    .gray-buttons button {{
        background-color: {COLOR_GRAY} !important;
        color: white !important;
    }}
    .gray-buttons button:hover {{
        background-color: #666 !important;
    }}

    /* Blue buttons for file operation */
    .blue-buttons button {{
        background-color: {COLOR_PRIMARY} !important;
        color: white !important;
    }}
    .blue-buttons button:hover {{
        background-color: #1976d2 !important;
    }}

    /* File operation container - control spacing from title */
    .file-op-buttons {{
        margin-bottom: -100px;
        padding-top: 0;
    }}

    /* Blue buttons for file operation */
    .file-op-buttons button {{
        background-color: {COLOR_PRIMARY} !important;
        color: white !important;
    }}
    .file-op-buttons button:hover {{
        background-color: #1976d2 !important;
    }}

    /* File operation selectbox - white style */
    .file-op-buttons .stSelectbox > div > div {{
        background-color: white !important;
        border: 2px solid {COLOR_PRIMARY} !important;
        border-radius: 0px !important;
    }}
    .file-op-buttons .stSelectbox [data-baseweb="select"] {{
        background-color: white !important;
    }}
    .file-op-buttons .stSelectbox [data-baseweb="select"] > div {{
        background-color: white !important;
    }}
    .file-op-buttons .stSelectbox [data-baseweb="select"] > div > div {{
        background-color: white !important;
    }}
    .file-op-buttons .stSelectbox [data-baseweb="select"] input {{
        background-color: white !important;
        color: #1a1a2e !important;
        font-family: 'Courier New', monospace !important;
    }}
    .file-op-buttons .stSelectbox [data-baseweb="select"] input:focus {{
        background-color: white !important;
        box-shadow: none !important;
    }}
    .file-op-buttons .stSelectbox [data-baseweb="select"] input::placeholder {{
        color: #757575 !important;
    }}
    .file-op-buttons .stSelectbox [data-baseweb="popover"] {{
        background-color: white !important;
    }}
    .file-op-buttons .stSelectbox [data-baseweb="popover"] [data-baseweb="menu"] {{
        background-color: white !important;
    }}
    .file-op-buttons .stSelectbox [data-baseweb="popover"] [data-baseweb="menu"] > div {{
        background-color: white !important;
    }}

    /* Dialog Section */
    .dialog-section {{
        background-color: {COLOR_CARD};
        padding: 15px;
        margin-top: 10px;
        border: 2px dashed {COLOR_PRIMARY};
    }}

    /* Text Input - Rectangle with blue border (matching results-display) */
    .stTextInput > div > div > input {{
        background-color: white !important;
        border: 2px solid {COLOR_PRIMARY} !important;
        border-radius: 0px !important;
        font-family: 'Courier New', monospace !important;
        font-size: 13px !important;
        padding: 15px !important;
        width: 100% !important;
        box-sizing: border-box !important;
        color: {COLOR_TEXT_DARK} !important;
    }}
    .stTextInput > div {{
        margin-bottom: 0px !important;
    }}

    /* Number Input - White input with blue border, rectangle style */
    .stNumberInput > div {{
        border: 2px solid {COLOR_PRIMARY} !important;
        border-radius: 0px !important;
        background-color: white !important;
        padding: 5px 8px !important;
    }}
    .stNumberInput input {{
        background-color: white !important;
        border: none !important;
        font-family: 'Courier New', monospace !important;
        font-size: 14px !important;
        padding: 0px !important;
        height: auto !important;
        color: {COLOR_TEXT_DARK} !important;
        width: 100% !important;
    }}
    .stNumberInput button {{
        display: none !important;
    }}
    .stNumberInput label {{
        font-family: Arial, sans-serif !important;
        font-size: 15px !important;
        font-weight: bold !important;
        color: {COLOR_TEXT_DARK} !important;
    }}

    @media (max-width: 768px) {{
        .main-header h1 {{ font-size: 16px !important; }}

        /* ========== 响应式：手机端参数输入区域 ========== */
        /* 参数输入区域改为 2-3 列自适应 */
        .param-grid-container {{
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 8px !important;
        }}
        .param-grid-container .stColumn {{
            min-width: 0 !important;
        }}

        /* 参数标签在手机端更小 */
        .param-label {{
            font-size: 12px !important;
        }}

        /* ========== 响应式：手机端样本选择区域 ========== */
        /* 左右布局改为上下堆叠 */
        .sample-section-container {{
            display: flex !important;
            flex-direction: column !important;
            gap: 10px !important;
        }}
        .sample-btn-stack {{
            display: flex !important;
            flex-direction: row !important;
            gap: 8px !important;
            width: 100% !important;
        }}
        .sample-btn-stack > div {{
            flex: 1 !important;
        }}
        .sample-display-col {{
            padding-left: 0 !important;
            padding-top: 10px !important;
        }}

        /* ========== 响应式：手机端文件操作区域 ========== */
        /* 按钮改为 2x2 网格布局 */
        .file-op-btn-container {{
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 8px !important;
        }}

        /* ========== 响应式：所有按钮填满宽度 ========== */
        .stButton > button {{
            width: 100% !important;
            height: auto !important;
            min-height: 50px !important;
            font-size: 12px !important;
            white-space: normal !important;
            word-wrap: break-word !important;
        }}

        /* ========== 响应式：输入框和下拉菜单 ========== */
        .stTextInput > div,
        .stTextArea > div,
        .stSelectbox > div {{
            max-width: 100% !important;
            width: 100% !important;
        }}

        .stTextInput input,
        .stTextArea textarea {{
            width: 100% !important;
            font-size: 14px !important;
        }}

        /* 下拉菜单全宽 */
        [data-baseweb="select"] {{
            width: 100% !important;
            min-width: unset !important;
        }}

        /* ========== 响应式：结果显示区域 ========== */
        .results-display {{
            min-height: 150px !important;
            font-size: 12px !important;
        }}

        /* ========== 响应式：弹窗 ========== */
        .stDialog {{
            width: 95% !important;
            max-width: 95vw !important;
        }}

        /* 错误提示在手机端更醒目 */
        [data-testid="stAlert"] {{
            font-size: 11px !important;
        }}
    }}

    /* ========== 响应式：平板适配 (769px - 1024px) ========== */
    @media (min-width: 769px) and (max-width: 1024px) {{
        /* 保持原有布局，略微调整间距 */
        .stColumn {{
            min-width: 0 !important;
        }}
    }}

    /* ========== 响应式：防止横向滚动 ========== */
    /* 确保页面不会溢出 */
    .stApp {{
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }}

    /* Streamlit 主内容区域限制宽度 */
    .main {{
        max-width: 100% !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }}

    /* 所有容器不超过视口宽度 */
    .stHorizontalBlock {{
        max-width: 100% !important;
        flex-wrap: wrap !important;
    }}

    /* ========== 通用响应式修复 ========== */
    /* 确保列宽不会超出容器 */
    [data-testid="stHorizontalBlock"] > div {{
        max-width: 100% !important;
        min-width: 0 !important;
    }}

    /* 按钮组自适应 */
    [data-testid="stHorizontalBlock"] {{
        gap: 4px !important;
    }}
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """初始化所有 session_state 变量"""
    defaults = {
        'param_values': {'m': None, 'n': None, 'k': None, 'j': None, 's': None},
        'show_manual_dialog': False,
        'last_samples': [],
        'algorithm_results': [],
        'random_btn_clicked': False,
        'manual_btn_clicked': False,
        'execute_btn_clicked': False,
        'run_btn_clicked': False,
        'refresh_btn_clicked': False,
        'delete_btn_clicked': False,
        'param_errors': {'m': None, 'n': None, 'k': None, 'j': None, 's': None},
        'manual_input_error': None,
        'file_error': None,
        'run_error': None,
        'random_success_message': None,
        'random_error': None,
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def validate_param_from_input(key: str, min_val: int, max_val: int):
    """从输入框验证并更新参数值"""
    user_input = st.session_state.get(f"{key}_input", "")

    if not user_input or not user_input.strip():
        st.session_state.param_values[key] = None
        st.session_state.param_errors[key] = None
        return

    try:
        v = int(user_input.strip())
        error_msg = None

        if key == 'j':
            # j 的验证需要从当前 session_state 读取 s 和 k 的值
            s_input = st.session_state.get("s_input", "")
            k_input = st.session_state.get("k_input", "")

            s_val = int(s_input.strip()) if s_input and s_input.strip() else None
            k_val = int(k_input.strip()) if k_input and k_input.strip() else None

            if s_val is not None and k_val is not None:
                if v < s_val or v > k_val:
                    error_msg = f"Error: j must be {s_val}-{k_val}"
                    st.session_state.param_values[key] = None
                else:
                    st.session_state.param_values[key] = v
            else:
                if v < 1:
                    error_msg = f"Error: j >= 1"
                    st.session_state.param_values[key] = None
                else:
                    st.session_state.param_values[key] = v
        else:
            if v < min_val:
                error_msg = f"Error: {key} >= {min_val}"
                st.session_state.param_values[key] = None
            elif v > max_val:
                error_msg = f"Error: {key} <= {max_val}"
                st.session_state.param_values[key] = None
            else:
                st.session_state.param_values[key] = v

        st.session_state.param_errors[key] = error_msg

    except ValueError:
        st.session_state.param_values[key] = None
        st.session_state.param_errors[key] = f"Error: must be integer"


def validate_all_params():
    """验证所有参数 - 先从输入框读取值"""
    # 先验证所有输入框
    validate_param_from_input('m', 45, 54)
    validate_param_from_input('n', 7, 25)
    validate_param_from_input('k', 4, 7)
    validate_param_from_input('s', 3, 7)
    validate_param_from_input('j', 1, 7)  # j 的 min/max 会被动态计算

    p = st.session_state.param_values
    has_empty = False

    for key in ['m', 'n', 'k', 's', 'j']:
        if p[key] is None:
            has_empty = True

    if has_empty:
        return None

    st.session_state.param_errors = {'m': None, 'n': None, 'k': None, 'j': None, 's': None}

    if p['n'] < 7 or p['n'] > 25:
        st.session_state.param_errors['n'] = "Error: n must satisfy 7 ≤ n ≤ 25"
        return None

    if p['j'] < p['s'] or p['j'] > p['k']:
        st.session_state.param_errors['j'] = f"Error: j must satisfy {p['s']} ≤ j ≤ {p['k']}"
        return None

    return (p['m'], p['n'], p['k'], p['j'], p['s'])


def validate_manual_input(user_input: str) -> Optional[str]:
    """验证手动输入的样本"""
    m = st.session_state.param_values['m']
    n = st.session_state.param_values['n']

    if not user_input.strip():
        return "Error: Input cannot be empty."

    try:
        samples = [int(x.strip()) for x in user_input.split(',')]
    except ValueError:
        return "Error: Please use English characters only, numbers separated by commas."

    if n is not None and len(samples) != n:
        return f"Error: Please enter exactly {n} numbers."

    if m is not None:
        invalid_numbers = [x for x in samples if x < 1 or x > m]
        if invalid_numbers:
            return f"Error: Numbers must be between 1 and {m}."

    if len(set(samples)) != len(samples):
        return "Error: Duplicate numbers found."

    st.session_state.last_samples = samples
    return None


def main():
    # 初始化 session_state
    init_session_state()

    db_manager = DatabaseManager()

    # ========== 渲染头部 ==========
    st.markdown('''
    <div class="main-header">
        <h1>An Optimal Samples Selection System</h1>
    </div>
    ''', unsafe_allow_html=True)

    # ========== 参数输入区域 ==========
    st.markdown('<p class="section-header">Parameter Input</p>', unsafe_allow_html=True)

    # 响应式参数布局：使用 expander 包装实现手机端自适应
    # 检测是否为手机端宽度
    params_data = [
        ('m', 'm (45-54):', 45, 54),
        ('n', 'n (7-25):', 7, 25),
        ('k', 'k (4-7):', 4, 7),
        ('s', 's (3-7):', 3, 7),
        ('j', 'j (s≤j≤k):', None, None)
    ]

    # 电脑端：5列横向排列；手机端会自动换行
    # 使用 st.columns 并设置响应式比例
    cols = st.columns([1, 1, 1, 1, 1])

    for i, (key, label, min_val, max_val) in enumerate(params_data):
        with cols[i]:
            st.markdown(f'<span class="param-label">{label}</span>', unsafe_allow_html=True)

            widget_key = f"{key}_input"

            # 直接使用 st.text_input，不设置 value 参数，让 session_state 自动管理
            st.text_input(
                "",
                key=widget_key,
                label_visibility="collapsed"
            )

            # 每次渲染时验证参数
            validate_param_from_input(key, min_val if min_val else 1, max_val if max_val else 999)

            error_msg = st.session_state.param_errors.get(key)
            if error_msg:
                st.markdown(f'<p style="color: #d32f2f; font-size: 16px; font-weight: bold; margin-top: 2px; margin-bottom: 0;">{error_msg}</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="min-height: 14px; margin-top: 2px; margin-bottom: 0;"></p>', unsafe_allow_html=True)

    # ========== 样本选择区域 ==========
    st.markdown('<p class="section-header">Sample Selection & Display</p>', unsafe_allow_html=True)

    samples_str = ""
    if st.session_state.last_samples:
        samples_str = ", ".join(str(s) for s in st.session_state.last_samples)

    # 显示成功消息
    if st.session_state.random_success_message:
        st.success(st.session_state.random_success_message)
        st.session_state.random_success_message = None

    if st.session_state.random_error:
        st.markdown(f'<p style="color: #d32f2f; font-size: 11px; margin-top: 5px;">{st.session_state.random_error}</p>', unsafe_allow_html=True)

    # Sample Selection & Display 区域
    # 整体结构：上方显示框 + 下方按钮（并排横向）
    st.markdown(f'''
    <div style="
        background-color: white;
        border: 2px solid {COLOR_PRIMARY};
        padding: 15px;
        margin-bottom: 10px;
    ">
        <span style="color: {COLOR_TEXT_DARK}; font-size: 15px; font-weight: bold; font-family: Arial; margin-bottom: 5px; display: block;">Selected n Samples:</span>
        <div style="
            font-family: Courier New, monospace;
            font-size: 14px;
            color: {COLOR_TEXT_DARK};
            min-height: 60px;
            padding: 10px;
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            text-align: center;
            line-height: 60px;
        ">{samples_str if samples_str else '<span style="color: #999;">No samples selected</span>'}</div>
    </div>
    ''', unsafe_allow_html=True)

    # 按钮区域：并排横向排列
    col_random, col_manual = st.columns(2)
    with col_random:
        if st.button("Randomly Select", key="randomly_btn", use_container_width=True):
            st.session_state.random_error = None
            result = validate_all_params()
            if result:
                m, n, k, j, s = result
                samples = random.sample(range(1, m + 1), n)
                st.session_state.last_samples = samples
                st.session_state.random_success_message = f"Successfully generated {n} random samples from 1 to {m}!"
                st.rerun()
            else:
                st.session_state.random_error = "Please fill in all valid parameters first."
                st.session_state.random_success_message = None

    with col_manual:
        if st.button("Manually Input", key="manually_btn", use_container_width=True):
            result = validate_all_params()
            if result:
                st.session_state.show_manual_dialog = True
                st.rerun()
            else:
                st.session_state.random_error = "Please fill in all valid parameters first."

    # ========== 手动输入弹窗 ==========
    # 使用 Streamlit 原生弹窗
    @st.dialog("Manual Sample Input")
    def manual_input_dialog():
        n = st.session_state.param_values['n']
        m = st.session_state.param_values['m']
        n_str = str(n) if n is not None else "n"
        m_str = str(m) if m is not None else "m"

        st.markdown(f"Please enter exactly **{n_str}** unique positive integers (from **1** to **{m_str}**), separated by commas.")
        st.markdown(f"<sub style='color: #1565c0;'>Example: 1,3,5,7,9,11,13 (for n={n_str})</sub>", unsafe_allow_html=True)

        if st.session_state.manual_input_error:
            st.error(st.session_state.manual_input_error)

        manual_input = st.text_area(
            "Enter samples:",
            key="manual_input_field",
            height=100,
            placeholder=f"Enter {n_str} numbers separated by commas, e.g., 1,3,5,7,9,11,13"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit", key="manual_submit_btn", use_container_width=True):
                if not manual_input.strip():
                    st.session_state.manual_input_error = "Error: Input cannot be empty. Please enter numbers."
                    st.rerun()
                else:
                    error_msg = validate_manual_input(manual_input)
                    if error_msg:
                        st.session_state.manual_input_error = error_msg
                        st.rerun()
                    else:
                        st.session_state.manual_input_error = None
                        st.session_state.show_manual_dialog = False
                        st.session_state.random_success_message = f"Successfully added {n} manual samples!"
                        st.rerun()

        with col2:
            if st.button("Cancel", key="manual_cancel_btn", use_container_width=True):
                st.session_state.show_manual_dialog = False
                st.session_state.manual_input_error = None
                st.rerun()

    # 显示弹窗
    if st.session_state.show_manual_dialog:
        manual_input_dialog()

    # ========== File Operation ==========
    st.markdown('<p class="section-header">File Operation</p>', unsafe_allow_html=True)

    file_list = db_manager.get_file_list()

    # 文件选择下拉框
    with st.container():
        st.markdown('<div class="file-op-buttons">', unsafe_allow_html=True)

        if file_list:
            st.markdown('<span style="color: #1a1a2e; font-size: 15px; font-weight: bold; font-family: Arial;">Select a DB file:</span>', unsafe_allow_html=True)
            selected_file = st.selectbox(
                "",
                options=file_list,
                index=0,
                key="selected_db_file",
                format_func=lambda x: f"{x}.db",
                label_visibility="collapsed"
            )
        else:
            st.markdown('<div style="background-color: white; border: 2px solid #ccc; padding: 10px; font-family: Courier New, monospace; font-size: 12px; color: #757575; min-height: 60px; margin-top: 5px;">No DB files available</div>', unsafe_allow_html=True)
            st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
            selected_file = None

        # 操作按钮区域 - 响应式 2x2 网格布局
        st.markdown('<div class="file-op-btn-container">', unsafe_allow_html=True)

        # 第一行：Execute Selected | Refresh List
        btn_row1_col1, btn_row1_col2 = st.columns(2)
        with btn_row1_col1:
            if st.button("Execute Selected", key="execute_btn", use_container_width=True):
                st.session_state.execute_btn_clicked = True

        with btn_row1_col2:
            if st.button("Refresh List", key="refresh_btn", use_container_width=True):
                st.session_state.refresh_btn_clicked = True

        # 第二行：Run Algorithm | Delete Selected
        btn_row2_col1, btn_row2_col2 = st.columns(2)
        with btn_row2_col1:
            if st.button("Run Algorithm", key="run_btn", use_container_width=True):
                st.session_state.run_btn_clicked = True

        with btn_row2_col2:
            if st.button("Delete Selected", key="delete_btn", use_container_width=True):
                st.session_state.delete_btn_clicked = True

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.file_error:
        st.markdown(f'<p style="color: #d32f2f; font-size: 11px; margin-top: 5px;">{st.session_state.file_error}</p>', unsafe_allow_html=True)
    if st.session_state.run_error:
        st.markdown(f'<p style="color: #d32f2f; font-size: 11px; margin-top: 5px;">{st.session_state.run_error}</p>', unsafe_allow_html=True)

    # 处理刷新按钮
    if st.session_state.refresh_btn_clicked:
        st.session_state.refresh_btn_clicked = False

    # 处理执行按钮
    if st.session_state.execute_btn_clicked:
        st.session_state.execute_btn_clicked = False
        if not selected_file:
            st.session_state.file_error = "Please select a file first."
        else:
            results = db_manager.execute_file(selected_file)
            if results:
                st.session_state.algorithm_results = results
                st.session_state.file_error = None
                st.success(f"Successfully retrieved results from {selected_file}.db")
            else:
                st.session_state.file_error = "No results found."

    # 处理删除按钮
    if st.session_state.delete_btn_clicked:
        st.session_state.delete_btn_clicked = False
        if not selected_file:
            st.session_state.file_error = "Please select a file first."
        else:
            if db_manager.delete_file(selected_file):
                st.success(f"Successfully deleted {selected_file}.db")
                st.session_state.algorithm_results = []
                st.session_state.file_error = None
            else:
                st.session_state.file_error = "Failed to delete file."

    # 处理运行算法按钮
    if st.session_state.run_btn_clicked:
        st.session_state.run_btn_clicked = False
        result = validate_all_params()
        if result:
            m, n, k, j, s = result
            samples = st.session_state.last_samples
            if not samples:
                st.session_state.run_error = "Please select samples first."
            else:
                try:
                    results, info, filename = run_algorithm(m, n, k, j, s, samples)
                    if results:
                        st.session_state.algorithm_results = results
                        st.session_state.run_error = None
                        st.success(info)
                    else:
                        st.session_state.run_error = info
                except Exception as e:
                    st.session_state.run_error = f"Algorithm Error: {str(e)}"

    # ========== 结果显示区域 ==========
    st.markdown('<p class="section-header">Generated k-Sample Groups Results:</p>', unsafe_allow_html=True)

    if st.session_state.algorithm_results:
        results_text = ""
        for group in st.session_state.algorithm_results:
            if all(isinstance(x, int) and 1 <= x <= 54 for x in group):
                results_text += f"[{', '.join(str(x) for x in group)}]\n\n"
        st.markdown(f'<div class="results-display">{results_text}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="results-display"></div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
