"""
An Optimal Samples Selection System - Streamlit Web Version
1:1 Replica of Tkinter AI_system.py - Fixed Layout
"""

import streamlit as st
from streamlit.errors import StreamlitAPIException
import random
from typing import List, Optional
import sys
import os
import io
import csv
import re
from datetime import datetime

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
function logClick(btnName) {{
    console.log('[DEBUG] Button clicked: ' + btnName);
}}

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

    /* Scrollable Results Display */
    .results-scrollable {{
        background-color: white;
        border: 2px solid {COLOR_PRIMARY};
        border-radius: 0px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        color: {COLOR_PRIMARY};
        max-height: 300px;
        overflow-y: auto;
        width: 100%;
        box-sizing: border-box;
    }}

    /* Scrollable Results Display - Page 1 (Shorter) */
    .results-scrollable-page1 {{
        background-color: white;
        border: 2px solid {COLOR_PRIMARY};
        border-radius: 0px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        color: {COLOR_PRIMARY};
        max-height: 150px;
        overflow-y: auto;
        width: 100%;
        box-sizing: border-box;
        text-align: left;
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

        
        
        .file-op-btn-container {{
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 8px !important;
        }}

        
        .stButton > button {{
            width: 100% !important;
            height: auto !important;
            min-height: 50px !important;
            font-size: 12px !important;
            white-space: normal !important;
            word-wrap: break-word !important;
        }}

        
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

        
        [data-baseweb="select"] {{
            width: 100% !important;
            min-width: unset !important;
        }}

        
        .results-display {{
            min-height: 150px !important;
            font-size: 12px !important;
        }}

        
        .stDialog {{
            width: 95% !important;
            max-width: 95vw !important;
        }}
    }}

    
    @media (min-width: 769px) and (max-width: 1024px) {{
        
        .stColumn {{
            min-width: 0 !important;
        }}
    }}

    
    .stApp {{
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }}

    
    .main {{
        max-width: 100% !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }}

    
    .stHorizontalBlock {{
        max-width: 100% !important;
        flex-wrap: wrap !important;
    }}

    
    
    [data-testid="stHorizontalBlock"] > div {{
        max-width: 100% !important;
        min-width: 0 !important;
    }}

    
    [data-testid="stHorizontalBlock"] {{
        gap: 4px !important;
    }}

    /* Action buttons - Blue buttons for main page */
    .action-buttons button {{
        background-color: {COLOR_PRIMARY} !important;
        color: white !important;
        border-radius: 0px !important;
        font-family: Arial !important;
        font-weight: bold !important;
        padding: 10px 5px !important;
        border: none !important;
        cursor: pointer !important;
        font-size: 13px !important;
        height: 50px !important;
    }}
    .action-buttons button:hover {{
        background-color: #1976d2 !important;
    }}
</style>
""", unsafe_allow_html=True)


def generate_unified_report(params, samples, results, groups, exec_time_str=None):
    
    samples_str = ", ".join(str(s) for s in samples) if samples else "N/A"
    results_lines = []
    for idx, group in enumerate(results, 1):
        if all(isinstance(x, int) and 1 <= x <= 54 for x in group):
            results_lines.append(f"{idx}: {' - '.join(str(x) for x in group)}")
    results_str = "\n".join(results_lines) if results_lines else "No results"

    report_id = f"{params.get('m')}-{params.get('n')}-{params.get('k')}-{params.get('j')}-{params.get('s')}-{params.get('t')}-{groups}"

    exec_time_display = exec_time_str if exec_time_str else "N/A"

    txt_content = f"""An Optimal Samples Selection System - Report ID: {report_id}
{'=' * 60}

Parameters:
  m = {params.get('m')}
  n = {params.get('n')}
  k = {params.get('k')}
  j = {params.get('j')}
  s = {params.get('s')}
  t = {params.get('t')}
  Groups = {groups}

Samples:
  {samples_str}

Generated k-Sample Groups Results:
{results_str}

Execution Time: {exec_time_display}

{'=' * 60}
"""
    return txt_content, report_id


def init_session_state():
    
    defaults = {
        'param_values': {'m': None, 'n': None, 'k': None, 'j': None, 's': None, 't': None},
        'show_manual_dialog': False,
        'last_samples': [],
        'algorithm_results': [],
        'random_btn_clicked': False,
        'manual_btn_clicked': False,
        'execute_btn_clicked': False,
        'run_btn_clicked': False,
        'refresh_btn_clicked': False,
        'delete_btn_clicked': False,
        'param_errors': {'m': None, 'n': None, 'k': None, 'j': None, 's': None, 't': None},
        'manual_input_error': None,
        'file_error': None,
        'run_error': None,
        'random_success_message': None,
        'random_error': None,
        'current_page': 'main',
        'db_show_results': False,
        'db_success_message': None,
        'db_error_message': None,
        'is_executing': False,
        'show_export_options': False,
        'show_main_export_options': False,
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def show_error(message: str):
    
    st.markdown(f'''
    <div style="
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 4px;
        color: #721c24;
        padding: 10px 15px;
        margin: 5px 0;
        font-size: 11px;
        width: 100%;
        box-sizing: border-box;
    ">{message}</div>
    ''', unsafe_allow_html=True)


def validate_param_from_input(key: str, min_val: int, max_val: int):
    
    user_input = st.session_state.get(f"{key}_input", "")

    if not user_input or not user_input.strip():
        st.session_state.param_values[key] = None
        st.session_state.param_errors[key] = None
        return

    try:
        v = int(user_input.strip())
        error_msg = None

        if key == 'j':
            
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


def combination(n: int, r: int) -> int:
    """Calculate C(n, r) = n! / (r! * (n-r)!)"""
    if r > n or r < 0:
        return 0
    if r == 0 or r == n:
        return 1
    r = min(r, n - r)
    result = 1
    for i in range(r):
        result = result * (n - i) // (i + 1)
    return result


def validate_t_param():
    
    s_input = st.session_state.get("s_input", "")
    j_input = st.session_state.get("j_input", "")

    s_val = int(s_input.strip()) if s_input and s_input.strip() else None
    j_val = int(j_input.strip()) if j_input and j_input.strip() else None

    
    if s_val is not None and j_val is not None and j_val >= s_val:
        max_t = combination(j_val, s_val)
    else:
        max_t = None

    t_input = st.session_state.get("t_input", "")

    
    if s_val is not None and j_val is not None and s_val == j_val:
        st.session_state.t_fixed = True
        if not t_input or not t_input.strip():
            
            st.session_state.param_values['t'] = 1
            st.session_state.param_errors['t'] = None
            st.session_state.t_force_value_1 = True
        elif t_input.strip() == "1":
            st.session_state.param_values['t'] = 1
            st.session_state.param_errors['t'] = None
            st.session_state.t_force_value_1 = False
        else:
            st.session_state.param_values['t'] = None
            st.session_state.param_errors['t'] = "Error: When s=j, t must be 1"
            st.session_state.t_force_value_1 = True
        return

    st.session_state.t_fixed = False

    if not t_input or not t_input.strip():
        st.session_state.param_values['t'] = None
        st.session_state.param_errors['t'] = None
        return

    try:
        v = int(t_input.strip())

        if v < 1:
            st.session_state.param_values['t'] = None
            st.session_state.param_errors['t'] = "Error: t must be a positive integer"
        elif max_t is not None and v > max_t:
            st.session_state.param_values['t'] = None
            st.session_state.param_errors['t'] = f"Error: t max = {max_t} (C({j_val},{s_val})={max_t} s-element subsets)"
        else:
            st.session_state.param_values['t'] = v
            st.session_state.param_errors['t'] = None

    except ValueError:
        st.session_state.param_values['t'] = None
        st.session_state.param_errors['t'] = "Error: t must be a positive integer"


def validate_all_params():
    
    validate_param_from_input('m', 45, 54)
    validate_param_from_input('n', 7, 25)
    validate_param_from_input('k', 4, 7)
    validate_param_from_input('s', 3, 7)
    validate_param_from_input('j', 1, 7) 
    validate_t_param() 

    p = st.session_state.param_values
    has_empty = False

    for key in ['m', 'n', 'k', 's', 'j', 't']:
        if p[key] is None:
            has_empty = True

    if has_empty:
        return None

    st.session_state.param_errors = {'m': None, 'n': None, 'k': None, 'j': None, 's': None, 't': None}

    if p['n'] < 7 or p['n'] > 25:
        st.session_state.param_errors['n'] = "Error: n must satisfy 7 ≤ n ≤ 25"
        return None

    if p['j'] < p['s'] or p['j'] > p['k']:
        st.session_state.param_errors['j'] = f"Error: j must satisfy {p['s']} ≤ j ≤ {p['k']}"
        return None

    return (p['m'], p['n'], p['k'], p['j'], p['s'], p['t'])


def validate_manual_input(user_input: str) -> Optional[str]:
    
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


def show_database_page(db_manager):
    
    st.markdown('''
    <div class="main-header">
        <h1>Data Base Resource</h1>
    </div>
    ''', unsafe_allow_html=True)

   
    records = db_manager.get_all_records()

    
    st.markdown('<p class="section-header" style="margin-top: 10px; margin-bottom: 0px;">Saved Records</p>', unsafe_allow_html=True)

    if records:
        
        record_options = []
        for i, record in enumerate(records):
            record_id, params, results, groups, execution_time = record
            option = record_id
            record_options.append(option)

        selected_record = st.selectbox(
            "",
            options=record_options,
            key="db_record_selector"
        )

        
        selected_idx = record_options.index(selected_record)
        selected_record_data = records[selected_idx]

         
        record_id, params, results, groups, execution_time = selected_record_data

        
        st.markdown(f'''
        <div style="background-color: white; border: 2px solid #1565c0; padding: 10px; margin-bottom: 10px;">
            <p style="color: #1a1a2e; font-size: 14px; font-weight: bold; margin: 0;">Parameters:</p>
            <p style="color: #1565c0; font-size: 13px; font-family: Courier New; margin: 5px 0;">
                m={params.get('m')}, n={params.get('n')}, k={params.get('k')}, j={params.get('j')}, s={params.get('s')}, t={params.get('t')}, groups={groups}
            </p>
        </div>
        ''', unsafe_allow_html=True)

        
        st.markdown('<p class="section-header" style="margin-top: 25px;">Generated k-Sample Groups Results:</p>', unsafe_allow_html=True)
        
        if st.session_state.db_show_results and results:
            results_text = ""
            for idx, group in enumerate(results, 1):
                if all(isinstance(x, int) and 1 <= x <= 54 for x in group):
                    results_text += f"{idx}: {' - '.join(str(x) for x in group)}<br>"
            st.markdown(f'<div class="results-scrollable">{results_text}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="results-scrollable">No results to display. Click "Display" to show results.</div>', unsafe_allow_html=True)
        
        
        st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
        if st.session_state.db_success_message:
            st.success(st.session_state.db_success_message)
            st.session_state.db_success_message = None
        if st.session_state.db_error_message:
            show_error(st.session_state.db_error_message)
            st.session_state.db_error_message = None
    else:
        st.markdown('<div style="background-color: white; border: 2px solid #ccc; padding: 20px; text-align: center; color: #757575;">No saved records found.</div>', unsafe_allow_html=True)
        selected_idx = None

    
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)

    col_display, col_delete, col_back, col_print = st.columns(4)

    with col_display:
        if st.button("Display", key="db_display_btn", use_container_width=True):
            if selected_idx is not None:
                st.session_state.db_show_results = True
                st.session_state.show_export_options = False
                st.rerun()
            else:
                st.warning("Please select a record first.")

    with col_delete:
        if st.button("Delete", key="db_delete_btn", use_container_width=True):
            if selected_idx is not None:
                record_id = records[selected_idx][0]
                if db_manager.delete_record(record_id):
                    st.session_state.db_success_message = "Record deleted successfully!"
                    st.session_state.db_show_results = False
                    st.session_state.show_export_options = False
                    st.rerun()
                else:
                    st.session_state.db_error_message = "Failed to delete record."
                    st.rerun()
            else:
                st.session_state.db_error_message = "Please select a record first."
                st.rerun()

    with col_back:
        if st.button("Back", key="db_back_btn", use_container_width=True):
            st.session_state.db_show_results = False
            st.session_state.show_export_options = False
            st.session_state.current_page = 'main'
            st.rerun()

    with col_print:
        if st.button("Print", key="db_print_btn", use_container_width=True):
            st.session_state.show_export_options = True
            st.rerun()

    
    if st.session_state.get('show_export_options', False) and selected_idx is not None:
        st.markdown('<p class="section-header" style="margin-top: 15px; margin-bottom: 10px;">Export Format</p>', unsafe_allow_html=True)

        record_id, params, results, groups, execution_time = selected_record_data

        
        report_id = record_id.replace('.txt', '')

        
        if execution_time is not None:
            if execution_time < 1:
                exec_time_str = f"{execution_time*1000:.2f} ms"
            elif execution_time < 60:
                exec_time_str = f"{execution_time:.2f} seconds"
            else:
                mins = int(execution_time // 60)
                secs = execution_time % 60
                exec_time_str = f"{mins}m {secs:.2f}s"
        else:
            exec_time_str = "N/A"

        
        samples_str = ", ".join(str(s) for s in st.session_state.last_samples) if st.session_state.last_samples else "N/A"
        results_lines = []
        for idx, group in enumerate(results, 1):
            if all(isinstance(x, int) and 1 <= x <= 54 for x in group):
                results_lines.append(f"{idx}: {' - '.join(str(x) for x in group)}")
        results_str = "\n".join(results_lines) if results_lines else "No results"

        
        col_dl1, col_dl2 = st.columns(2)

        
        with col_dl1:
            txt_content = f"""An Optimal Samples Selection System - Report ID: {report_id}
{'=' * 60}

Parameters:
  m = {params.get('m')}
  n = {params.get('n')}
  k = {params.get('k')}
  j = {params.get('j')}
  s = {params.get('s')}
  t = {params.get('t')}
  Groups = {groups}

Samples:
  {samples_str}

Generated k-Sample Groups Results:
{results_str}

Execution Time: {exec_time_str}

{'=' * 60}
"""
            st.download_button(
                label="Download TXT",
                data=txt_content,
                file_name=f"optimal_report_{report_id}.txt",
                mime="text/plain",
                use_container_width=True
            )

        
        with col_dl2:
            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(['Category', 'Content'])
            writer.writerow(['Report ID', report_id])
            writer.writerow(['m', params.get('m')])
            writer.writerow(['n', params.get('n')])
            writer.writerow(['k', params.get('k')])
            writer.writerow(['j', params.get('j')])
            writer.writerow(['s', params.get('s')])
            writer.writerow(['t', params.get('t')])
            writer.writerow(['Groups', groups])
            writer.writerow(['Samples', samples_str])
            writer.writerow(['Execution Time', exec_time_str])
            writer.writerow([])
            writer.writerow(['Group Index', 'Group Members'])
            for idx, group in enumerate(results, 1):
                if all(isinstance(x, int) and 1 <= x <= 54 for x in group):
                    writer.writerow([idx, ','.join(str(x) for x in group)])

            csv_content = csv_buffer.getvalue()
            csv_buffer.close()

            st.download_button(
                label="Download CSV",
                data=csv_content,
                file_name=f"optimal_report_{report_id}.csv",
                mime="text/csv",
                use_container_width=True
            )

def main():
    
    init_session_state()

    db_manager = DatabaseManager()

    
    if st.session_state.current_page == "Data Base Resource":
        
        st.session_state.saved_input_values = {
            key: st.session_state.get(f'{key}_input', '')
            for key in ['m', 'n', 'k', 'j', 's', 't']
        }
        st.session_state.saved_last_samples = st.session_state.last_samples.copy()
        st.session_state.saved_param_values = st.session_state.param_values.copy()
        show_database_page(db_manager)
        return

    
    if 'saved_input_values' in st.session_state:
        saved = st.session_state.saved_input_values
        for key in ['m', 'n', 'k', 'j', 's', 't']:
            st.session_state[f'{key}_input'] = saved.get(key, '')
        if st.session_state.saved_last_samples:
            st.session_state.last_samples = st.session_state.saved_last_samples.copy()
        if st.session_state.saved_param_values:
            st.session_state.param_values = st.session_state.saved_param_values.copy()
       
        for key in ['saved_input_values', 'saved_last_samples', 'saved_param_values']:
            if key in st.session_state:
                del st.session_state[key]

   
    st.markdown('''
    <div class="main-header">
        <h1>An Optimal Samples Selection System</h1>
    </div>
    ''', unsafe_allow_html=True)

   

  
    st.markdown('<p class="section-header">Parameter Input</p>', unsafe_allow_html=True)

  
    params_data = [
        ('m', 'm (45-54):', 45, 54),
        ('n', 'n (7-25):', 7, 25),
        ('k', 'k (4-7):', 4, 7),
        ('j', 'j (s≤j≤k):', None, None),
        ('s', 's (3-7):', 3, 7)
    ]

   
    cols = st.columns([1, 1, 1, 1, 1])

    for i, (key, label, min_val, max_val) in enumerate(params_data):
        with cols[i]:
            st.markdown(f'<span class="param-label">{label}</span>', unsafe_allow_html=True)

            widget_key = f"{key}_input"

            
            st.text_input(
                "",
                key=widget_key,
                label_visibility="collapsed"
            )

            
            validate_param_from_input(key, min_val if min_val else 1, max_val if max_val else 999)

            error_msg = st.session_state.param_errors.get(key)
            if error_msg:
                show_error(error_msg)
            else:
                st.markdown('<p style="min-height: 14px; margin-top: 2px; margin-bottom: 0;"></p>', unsafe_allow_html=True)

    
    s_input = st.session_state.get("s_input", "")
    j_input = st.session_state.get("j_input", "")
    s_val = int(s_input.strip()) if s_input and s_input.strip() else None
    j_val = int(j_input.strip()) if j_input and j_input.strip() else None

    
    if s_val is not None and j_val is not None and j_val >= s_val:
        max_t = combination(j_val, s_val)
        t_max_hint = f" (max = {max_t}, C({j_val},{s_val}))"
    else:
        max_t = None
        t_max_hint = " (max = C(j,s))"

    
    t_fixed = (s_val is not None and j_val is not None and s_val == j_val)

    
    if t_fixed:
        t_hint = " (When s=j, t must be 1)"
    elif max_t is not None:
        t_hint = f" (t≥1, max=C({j_val},{s_val})={max_t})"
    else:
        t_hint = " (t≥1)"
    
    st.markdown(f'<span class="param-label">At least t s-subsets per j-subset{t_hint}</span>', unsafe_allow_html=True)

    
    validate_t_param()

    
    if t_fixed and st.session_state.get("t_input", "") not in ["", "1"]:
        st.session_state.t_input = "1"

    
    st.text_input(
        "t",
        key="t_input",
        value="1" if t_fixed else "",
        label_visibility="collapsed"
    )

    
    t_error = st.session_state.param_errors.get('t')
    if t_error:
        show_error(t_error)

    
    st.markdown('<p class="section-header">Sample Selection</p>', unsafe_allow_html=True)

    samples_str = ""
    if st.session_state.last_samples:
        samples_str = ", ".join(str(s) for s in st.session_state.last_samples)

    
    if st.session_state.random_success_message:
        st.success(st.session_state.random_success_message)
        st.session_state.random_success_message = None

    if st.session_state.random_error:
        st.markdown(f'<p style="color: #d32f2f; font-size: 11px; margin-top: 5px;">{st.session_state.random_error}</p>', unsafe_allow_html=True)

    
    st.markdown(f'''
    <div style="
        background-color: white;
        border: 2px solid {COLOR_PRIMARY};
        padding: 15px;
        margin-bottom: 10px;
    ">
        <div style="
            font-family: Courier New, monospace;
            font-size: 14px;
            color: {COLOR_TEXT_DARK};
            min-height: 60px;
            padding: 10px;
            text-align: center;
            line-height: 60px;
        ">{samples_str if samples_str else '<span style="color: #999;">No samples selected</span>'}</div>
    </div>
    ''', unsafe_allow_html=True)

    
    col_random, col_manual = st.columns(2)
    with col_random:
        if st.button("Randomly Select", key="randomly_btn", use_container_width=True):
            st.session_state.random_error = None
            st.session_state.show_manual_dialog = False
            result = validate_all_params()
            if result:
                m, n, k, j, s, t = result
                samples = random.sample(range(1, m + 1), n)
                st.session_state.last_samples = samples
                st.rerun()
            else:
                pass
    with col_manual:
        if st.button("Manually Input", key="manually_btn", use_container_width=True):
            result = validate_all_params()
            if result:
                st.session_state.show_manual_dialog = True
                st.rerun()
            else:
                pass

    
    @st.dialog("Manual Sample Input")
    def manual_input_dialog():
        n = st.session_state.param_values['n']
        m = st.session_state.param_values['m']
        n_str = str(n) if n is not None else "n"
        m_str = str(m) if m is not None else "m"

        st.markdown(f"Please enter exactly **{n_str}** unique positive integers (from **1** to **{m_str}**), separated by commas.")
        st.markdown(f"<sub style='color: #1565c0;'>Example: 1,3,5,7,9,11,13 (for n={n_str})</sub>", unsafe_allow_html=True)

        if st.session_state.manual_input_error:
            show_error(st.session_state.manual_input_error)

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

    
    if st.session_state.show_manual_dialog:
        manual_input_dialog()

    
    results_container = st.container(key="results_persistent_container")
    with results_container:
        st.markdown('<p class="section-header">Generated k-Sample Groups Results:</p>', unsafe_allow_html=True)

        
        results_progress_placeholder = st.empty()
        results_status_placeholder = st.empty()

        
        if st.session_state.is_executing:
            
            pass
        elif st.session_state.get('execution_time') is not None:
            results_progress_placeholder.progress(100)
        else:
            
            results_progress_placeholder.progress(0)
        
        if st.session_state.algorithm_results:
            results_text = ""
            for idx, group in enumerate(st.session_state.algorithm_results, 1):
                if all(isinstance(x, int) and 1 <= x <= 54 for x in group):
                    results_text += f"{idx}: {' - '.join(str(x) for x in group)}<br>"
            st.markdown(f'<div class="results-scrollable-page1">{results_text}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="results-scrollable-page1"></div>', unsafe_allow_html=True)

        
        if 'action_success_msg' not in st.session_state:
            st.session_state.action_success_msg = None
        if 'action_error_msg' not in st.session_state:
            st.session_state.action_error_msg = None
        if 'action_warning_msg' not in st.session_state:
            st.session_state.action_warning_msg = None
        if 'execution_time' not in st.session_state:
            st.session_state.execution_time = None
        if 'store_success_msg' not in st.session_state:
            st.session_state.store_success_msg = None
        if 'clear_success_msg' not in st.session_state:
            st.session_state.clear_success_msg = None
        if 'execute_success_msg' not in st.session_state:
            st.session_state.execute_success_msg = None

        
        if st.session_state.get('execution_time') is not None:
            elapsed = st.session_state.execution_time
            if elapsed < 1:
                time_str = f"Execution time: {elapsed*1000:.2f} ms"
            elif elapsed < 60:
                time_str = f"Execution time: {elapsed:.2f} seconds"
            else:
                mins = int(elapsed // 60)
                secs = elapsed % 60
                time_str = f"Execution time: {mins}m {secs:.2f}s"
            
            info = st.session_state.get('action_success_msg', '')
            combined_msg = f"{info}\n{time_str}" if info else time_str
            st.session_state.execute_success_msg = combined_msg
            
            st.markdown(f'<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)

    
    if 'is_executing' not in st.session_state:
        st.session_state.is_executing = False

    
    st.markdown('<div class="action-buttons" style="display: flex; gap: 5px; margin-top: 5px; margin-bottom: 10px;">', unsafe_allow_html=True)

    col_execute, col_store, col_clear, col_print, col_next = st.columns(5)

    
    if st.session_state.is_executing:
        import time
        start_time = time.time()
        
        results_progress_placeholder.progress(10)
        results_status_placeholder.text("Initializing algorithm...")
        
        m, n, k, j, s, t = validate_all_params()
        samples = st.session_state.last_samples
        
        results_progress_placeholder.progress(30)
        results_status_placeholder.text("Processing samples...")
        
        try:
            results, info, filename = run_algorithm(m, n, k, j, s, t, samples)
            
            results_progress_placeholder.progress(80)
            results_status_placeholder.text("Finalizing results...")
            
            if results:
                st.session_state.algorithm_results = results
                st.session_state.run_error = None
                elapsed_time = time.time() - start_time
                st.session_state.execution_time = elapsed_time
                st.session_state.action_success_msg = info
            else:
                st.session_state.run_error = info
        except Exception as e:
            st.session_state.run_error = f"Algorithm Error: {str(e)}"
        
        results_progress_placeholder.progress(100)
        results_status_placeholder.text("Complete!")
        
        st.session_state.is_executing = False
        st.rerun()

    with col_execute:
        if st.button("Execute", key="main_execute_btn", use_container_width=True, disabled=st.session_state.is_executing):
            st.session_state.show_main_export_options = False
            result = validate_all_params()
            if result:
                m, n, k, j, s, t = result
                samples = st.session_state.last_samples
                if not samples:
                    st.session_state.run_error = "Please select samples first."
                else:
                    st.session_state.is_executing = True
                    st.rerun()
            else:
                pass

    with col_store:
        if st.button("Store", key="main_store_btn", use_container_width=True, disabled=st.session_state.is_executing):
            st.session_state.show_main_export_options = False
            st.session_state.execute_success_msg = None
            if st.session_state.algorithm_results:
                try:
                    db_manager.save_result(
                        st.session_state.param_values,
                        st.session_state.algorithm_results,
                        st.session_state.execution_time
                    )
                    st.session_state.action_success_msg = None
                    st.session_state.store_success_msg = "Results saved to database! "
                except Exception as e:
                    st.session_state.store_success_msg = None
                    st.session_state.action_error_msg = f"Failed to save: {str(e)}"
            else:
                st.session_state.store_success_msg = None
                st.session_state.action_warning_msg = "No results to save. Please run Execute first."

    with col_clear:
        if st.button("Clear", key="main_clear_btn", use_container_width=True):
            st.session_state.show_main_export_options = False
            
            for key in ['m', 'n', 'k', 'j', 's', 't']:
                st.session_state.param_values[key] = None
                widget_key = f"{key}_input"
                
                if widget_key in st.session_state:
                    del st.session_state[widget_key]
            for key in st.session_state.param_errors:
                st.session_state.param_errors[key] = None
            st.session_state.last_samples = []
            st.session_state.algorithm_results = []
            st.session_state.run_error = None
            st.session_state.random_error = None
            st.session_state.random_success_message = None
            st.session_state.is_executing = False
            st.session_state.execution_time = None
            st.session_state.action_success_msg = None
            st.session_state.action_error_msg = None
            st.session_state.action_warning_msg = None
            st.session_state.store_success_msg = None
            st.session_state.clear_success_msg = "All data cleared successfully!"

    with col_print:
        if st.button("Print", key="main_print_btn", use_container_width=True):
            st.session_state.show_main_export_options = True
            st.rerun()

    
    if st.session_state.get('show_main_export_options', False) and st.session_state.algorithm_results:
        
        exec_time = st.session_state.get('execution_time')
        if exec_time is not None:
            if exec_time < 1:
                exec_time_str = f"{exec_time*1000:.2f} ms"
            elif exec_time < 60:
                exec_time_str = f"{exec_time:.2f} seconds"
            else:
                mins = int(exec_time // 60)
                secs = exec_time % 60
                exec_time_str = f"{mins}m {secs:.2f}s"
        else:
            exec_time_str = "N/A"

        st.markdown(f'<p class="section-header" style="margin-top: 15px; margin-bottom: 10px;">Export Format</p>', unsafe_allow_html=True)

        params = st.session_state.param_values
        results = st.session_state.algorithm_results
        samples = st.session_state.last_samples
        groups = len(results)

        
        txt_content, report_id = generate_unified_report(params, samples, results, groups, exec_time_str)

        col_dl1, col_dl2 = st.columns(2)

        
        with col_dl1:
            st.download_button(
                label="Download TXT",
                data=txt_content,
                file_name=f"optimal_report_{report_id}.txt",
                mime="text/plain",
                use_container_width=True
            )

        
        with col_dl2:
            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(['Category', 'Content'])
            writer.writerow(['Report ID', report_id])
            writer.writerow(['m', params.get('m')])
            writer.writerow(['n', params.get('n')])
            writer.writerow(['k', params.get('k')])
            writer.writerow(['j', params.get('j')])
            writer.writerow(['s', params.get('s')])
            writer.writerow(['t', params.get('t')])
            writer.writerow(['Groups', groups])
            writer.writerow(['Samples', ", ".join(str(s) for s in samples) if samples else "N/A"])
            writer.writerow(['Execution Time', exec_time_str])
            writer.writerow([])
            writer.writerow(['Group Index', 'Group Members'])
            for idx, group in enumerate(results, 1):
                if all(isinstance(x, int) and 1 <= x <= 54 for x in group):
                    writer.writerow([idx, ','.join(str(x) for x in group)])

            csv_content = csv_buffer.getvalue()
            csv_buffer.close()

            st.download_button(
                label="Download CSV",
                data=csv_content,
                file_name=f"optimal_report_{report_id}.csv",
                mime="text/csv",
                use_container_width=True
            )
    elif st.session_state.get('show_main_export_options', False) and not st.session_state.algorithm_results:
        st.session_state.action_warning_msg = "No results to export. Please run Execute first."
        st.session_state.show_main_export_options = False
        st.rerun()

    with col_next:
        if st.button("Next", key="main_next_btn", use_container_width=True):
            st.session_state.current_page = "Data Base Resource"
            st.rerun()

    
    if st.session_state.get('execute_success_msg'):
        st.success(st.session_state.execute_success_msg)
        st.session_state.execute_success_msg = None
    if st.session_state.get('store_success_msg'):
        st.success(st.session_state.store_success_msg)
        st.session_state.store_success_msg = None
    if st.session_state.get('clear_success_msg'):
        st.success(st.session_state.clear_success_msg)
        st.session_state.clear_success_msg = None
        st.rerun()
    if st.session_state.get('action_error_msg'):
        show_error(st.session_state.action_error_msg)
        st.session_state.action_error_msg = None
    if st.session_state.get('action_warning_msg'):
        st.warning(st.session_state.action_warning_msg)
        st.session_state.action_warning_msg = None

    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
