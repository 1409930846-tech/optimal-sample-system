"""
An Optimal Samples Selection System - Streamlit Web Version
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
<style>
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    .stApp {{
        background-color: {COLOR_BG};
    }}

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

    .section-header {{
        color: {COLOR_PRIMARY};
        font-size: 16px;
        font-weight: bold;
        font-family: Arial, sans-serif;
        margin-bottom: 5px;
    }}

    .param-label {{
        color: {COLOR_TEXT_DARK};
        font-size: 15px;
        font-weight: bold;
        font-family: Arial, sans-serif;
    }}

    .stAlert {{
        font-size: 11px;
    }}
    .stAlert > div {{
        font-size: 11px;
    }}

    .stTextInput > div > div > input {{
        background-color: white;
        border: 2px solid {COLOR_PRIMARY};
        border-radius: 0px;
        color: {COLOR_TEXT_DARK};
    }}

    .stTextArea > div > div > textarea {{
        background-color: white;
        border: 2px solid {COLOR_PRIMARY};
        border-radius: 0px;
        color: {COLOR_TEXT_DARK};
        font-family: 'Courier New', monospace !important;
    }}

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

    .file-op-buttons {{
        margin-bottom: -100px;
        padding-top: 0;
    }}

    .file-op-buttons button {{
        background-color: {COLOR_PRIMARY} !important;
        color: white !important;
    }}
    .file-op-buttons button:hover {{
        background-color: #1976d2 !important;
    }}

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

    .stApp {{
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }}

    .main {{
        max-width: 100% !important;
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
    }}

    [data-testid="stHorizontalBlock"] {{
        gap: 4px !important;
    }}
</style>
""", unsafe_allow_html=True)


def init_session_state():
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


def validate_all_params():
    validate_param_from_input('m', 45, 54)
    validate_param_from_input('n', 7, 25)
    validate_param_from_input('k', 4, 7)
    validate_param_from_input('s', 3, 7)
    validate_param_from_input('j', 1, 7)

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
    init_session_state()

    db_manager = DatabaseManager()

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
        ('s', 's (3-7):', 3, 7),
        ('j', 'j (s≤j≤k):', None, None)
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
                st.markdown(f'<p style="color: #d32f2f; font-size: 16px; font-weight: bold; margin-top: 2px; margin-bottom: 0;">{error_msg}</p>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="min-height: 14px; margin-top: 2px; margin-bottom: 0;"></p>', unsafe_allow_html=True)

    st.markdown('<p class="section-header">Sample Selection & Display</p>', unsafe_allow_html=True)

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

    if st.session_state.show_manual_dialog:
        manual_input_dialog()

    st.markdown('<p class="section-header">File Operation</p>', unsafe_allow_html=True)

    file_list = db_manager.get_file_list()

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

        st.markdown('<div class="file-op-btn-container">', unsafe_allow_html=True)

        btn_row1_col1, btn_row1_col2 = st.columns(2)
        with btn_row1_col1:
            if st.button("Execute Selected", key="execute_btn", use_container_width=True):
                st.session_state.execute_btn_clicked = True

        with btn_row1_col2:
            if st.button("Refresh List", key="refresh_btn", use_container_width=True):
                st.session_state.refresh_btn_clicked = True

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

    if st.session_state.refresh_btn_clicked:
        st.session_state.refresh_btn_clicked = False

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
