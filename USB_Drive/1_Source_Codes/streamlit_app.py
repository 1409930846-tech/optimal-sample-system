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
        color: white;
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
    }}
    .main-header h1 {{
        margin: 0;
        font-size: 20px;
        font-weight: bold;
        font-family: Arial, sans-serif;
    }}

    /* Section Title - outside card */
    .section-header {{
        color: {COLOR_PRIMARY};
        font-size: 13px;
        font-weight: bold;
        font-family: Arial, sans-serif;
        margin-bottom: 8px;
        margin-top: 0;
    }}

    /* Parameter Input: Tkinter Style */
    .param-label {{
        color: {COLOR_TEXT_DARK};
        font-size: 16px;
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

    /* Text input white background */
    .stTextInput > div > div > input {{
        background-color: white;
        border: 1px solid #ccc;
        color: {COLOR_TEXT_DARK};
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
    .sample-btn-stack a button {{
        width: 100%;
        height: 50px;
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
    .file-op-btn-left a button,
    .file-op-btn-right a button {{
        width: 100%;
        height: 50px;
    }}
    .file-op-btn-inner {{
        display: flex;
        align-items: stretch;
    }}
    .file-op-btn-inner button {{
        width: 100%;
        min-height: 45px;
    }}

    /* HTML Buttons - Tkinter Style Gray */
    .html-btn {{
        padding: 6px 10px;
        font-family: Arial;
        font-weight: bold;
        font-size: 11px;
        border: none;
        border-radius: 0;
        cursor: pointer;
        width: 100%;
        height: 100%;
        display: inline-block;
        text-align: center;
        line-height: 1.4;
        box-sizing: border-box;
    }}
    .html-btn-gray {{
        background-color: {COLOR_GRAY};
        color: white;
    }}
    .html-btn-gray:hover {{
        background-color: #666;
    }}
    .html-btn-orange {{
        background-color: {COLOR_ORANGE};
        color: white;
    }}
    .html-btn-orange:hover {{
        background-color: #e65100;
    }}
    .html-btn-blue {{
        background-color: {COLOR_PRIMARY};
        color: white;
    }}
    .html-btn-blue:hover {{
        background-color: #1976d2;
    }}
    .html-btn-green {{
        background-color: {COLOR_ACCENT};
        color: white;
    }}
    .html-btn-green:hover {{
        background-color: #1b5e20;
    }}

    /* Streamlit Button Override */
    .stButton > button {{
        border-radius: 0px !important;
        font-family: Arial !important;
        font-weight: bold !important;
        padding: 6px 10px !important;
        border: none !important;
        cursor: pointer !important;
        font-size: 11px !important;
        height: auto !important;
    }}

    /* Dialog Section */
    .dialog-section {{
        background-color: {COLOR_CARD};
        padding: 15px;
        margin-top: 10px;
        border: 2px dashed {COLOR_PRIMARY};
    }}

    /* Text Input */
    .stTextInput > div > div > input {{
        border: 2px solid {COLOR_PRIMARY} !important;
        border-radius: 0px !important;
        font-family: 'Courier New', monospace !important;
    }}

    /* Number Input - White input with blue border */
    .stNumberInput > div {{
        border: 2px solid {COLOR_PRIMARY} !important;
        border-radius: 0px !important;
        background-color: white !important;
    }}
    .stNumberInput input {{
        background-color: white !important;
        border: none !important;
        font-family: Arial !important;
        font-size: 12px !important;
        padding: 2px 5px !important;
        height: 22px !important;
        color: {COLOR_TEXT_DARK} !important;
    }}
    .stNumberInput button {{
        display: none !important;
    }}

    @media (max-width: 768px) {{
        .main-header h1 {{ font-size: 16px !important; }}
    }}
</style>
""", unsafe_allow_html=True)


class StreamlitApp:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self._selected_samples: List[int] = []

        if 'param_values' not in st.session_state:
            st.session_state.param_values = {'m': None, 'n': None, 'k': None, 'j': None, 's': None}
        if 'show_manual_dialog' not in st.session_state:
            st.session_state.show_manual_dialog = False
        if 'last_samples' not in st.session_state:
            st.session_state.last_samples = []
        if 'algorithm_results' not in st.session_state:
            st.session_state.algorithm_results = []
        if 'random_btn_clicked' not in st.session_state:
            st.session_state.random_btn_clicked = False
        if 'manual_btn_clicked' not in st.session_state:
            st.session_state.manual_btn_clicked = False
        if 'execute_btn_clicked' not in st.session_state:
            st.session_state.execute_btn_clicked = False
        if 'run_btn_clicked' not in st.session_state:
            st.session_state.run_btn_clicked = False
        if 'refresh_btn_clicked' not in st.session_state:
            st.session_state.refresh_btn_clicked = False
        if 'delete_btn_clicked' not in st.session_state:
            st.session_state.delete_btn_clicked = False

    def render_header(self):
        st.markdown(f'''
        <div class="main-header">
            <h1>An Optimal Samples Selection System</h1>
        </div>
        ''', unsafe_allow_html=True)

    def render_parameter_input(self):
        st.markdown('<p class="section-header">Parameter Input</p>', unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns(5)

        params_data = [
            ('m', 'm (45-54):'),
            ('n', 'n (7-25):'),
            ('k', 'k (4-7):'),
            ('s', 's (3-7):'),
            ('j', 'j (s≤j≤k):')
        ]

        columns = [col1, col2, col3, col4, col5]

        for i, (key, label) in enumerate(params_data):
            with columns[i]:
                st.markdown(f'<span class="param-label">{label}</span>', unsafe_allow_html=True)

                if key == 'j':
                    s_val = st.session_state.param_values['s']
                    k_val = st.session_state.param_values['k']
                    j_val = st.session_state.param_values['j']
                    if s_val is not None and k_val is not None and k_val >= s_val:
                        j_min = s_val if s_val else 1
                        j_max = k_val if k_val else 7
                        if j_val is None or j_val < j_min:
                            j_val = j_min
                        if j_val > j_max:
                            j_val = j_max
                        default_val = str(j_val) if j_val else ""
                    else:
                        default_val = ""
                    st.text_input("", value=default_val, key=f"{key}_input", label_visibility="collapsed", on_change=self._on_param_change, args=(key,))
                elif key == 's':
                    old_s = st.session_state.param_values['s']
                    default_val = str(old_s) if old_s else ""
                    st.text_input("", value=default_val, key=f"{key}_input", label_visibility="collapsed", on_change=self._on_param_change, args=(key,))
                else:
                    val = st.session_state.param_values[key]
                    default_val = str(val) if val else ""
                    st.text_input("", value=default_val, key=f"{key}_input", label_visibility="collapsed", on_change=self._on_param_change, args=(key,))

    def _on_param_change(self, key):
        widget_key = f"{key}_input"
        if widget_key in st.session_state:
            user_input = st.session_state[widget_key]
            if user_input:
                try:
                    v = int(user_input)
                    bounds_map = {
                        'm': (45, 54),
                        'n': (7, 25),
                        'k': (4, 7),
                        's': (3, 7),
                        'j': (st.session_state.param_values.get('s', 1), st.session_state.param_values.get('k', 7))
                    }
                    if key in bounds_map:
                        min_val, max_val = bounds_map[key]
                        if v < min_val:
                            st.session_state.param_values[key] = None
                            st.error(f"Error: {key} value must be >= {min_val}")
                            return
                        elif v > max_val:
                            st.session_state.param_values[key] = None
                            st.error(f"Error: {key} value must be <= {max_val}")
                            return
                    st.session_state.param_values[key] = v
                    if key == 's' and (st.session_state.param_values.get('j') is None or st.session_state.param_values['j'] < v):
                        st.session_state.param_values['j'] = v
                except ValueError:
                    st.session_state.param_values[key] = None
                    st.error(f"Error: {key} must be an integer")

    def validate_parameters(self) -> Optional[tuple]:
        p = st.session_state.param_values
        if any(v is None for v in p.values()):
            st.error("Error: All parameters must be filled in.")
            return None
        if p['j'] < p['s'] or p['j'] > p['k']:
            st.error(f"Validation Error: j must satisfy {p['s']} ≤ j ≤ {p['k']}")
            return None
        return (p['m'], p['n'], p['k'], p['j'], p['s'])

    def render_sample_selection(self):
        st.markdown('<p class="section-header">Sample Selection & Display</p>', unsafe_allow_html=True)

        samples_str = ""
        if st.session_state.last_samples:
            samples_str = ", ".join(str(s) for s in st.session_state.last_samples)
            self._selected_samples = st.session_state.last_samples

        # Process button clicks from query params
        params = st.query_params
        if params.get("random_click") == "1":
            st.session_state.random_btn_clicked = True
        if params.get("manual_click") == "1":
            st.session_state.manual_btn_clicked = True

        # HTML-based layout - Gray buttons, stacked vertically, same size
        st.markdown(f'''
        <div class="sample-section">
            <div class="sample-btn-stack">
                <a href="/?random_click=1" target="_self">
                    <button class="html-btn html-btn-gray">Randomly Select n Samples</button>
                </a>
                <a href="/?manual_click=1" target="_self">
                    <button class="html-btn html-btn-gray">Manually Input n Samples</button>
                </a>
            </div>
            <div class="sample-display-col">
                <span class="param-label" style="font-size: 12px; font-weight: bold;">Selected n Samples:</span>
                <div class="sample-display">{samples_str}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        # Handle clicks
        if st.session_state.random_btn_clicked:
            st.session_state.random_btn_clicked = False
            st.query_params.clear()
            result = self.validate_parameters()
            if result:
                m, n, k, j, s = result
                self._selected_samples = random.sample(range(1, m + 1), n)
                st.session_state.last_samples = self._selected_samples
                st.success(f"Successfully generated {n} random samples from 1 to {m}!")
                st.rerun()

        if st.session_state.manual_btn_clicked:
            st.session_state.manual_btn_clicked = False
            st.query_params.clear()
            st.session_state.show_manual_dialog = True

        if st.session_state.show_manual_dialog:
            self.render_manual_input_dialog()

    def render_manual_input_dialog(self):
        st.markdown('<div class="dialog-section">', unsafe_allow_html=True)
        m = st.session_state.param_values['m']
        n = st.session_state.param_values['n']

        n_str = str(n) if n is not None else "n"
        m_str = str(m) if m is not None else "m"
        st.markdown(f'<p style="color: {COLOR_TEXT_DARK}; font-family: Arial; font-size: 12px;">Please enter exactly {n_str} unique positive integers (from 1 to {m_str}), separated by commas.</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: {COLOR_PRIMARY}; font-family: Arial; font-size: 10px; font-style: italic;">Example: 1,3,5,7,9,11,13 (for n={n_str})</p>', unsafe_allow_html=True)

        manual_input = st.text_input("", key="manual_input_field", placeholder="")

        col_submit, col_cancel = st.columns(2)
        with col_submit:
            submit_btn = st.button("Submit", key="manual_submit_btn", use_container_width=True)
        with col_cancel:
            close_btn = st.button("Cancel", key="manual_cancel_btn", use_container_width=True)

        if close_btn:
            st.session_state.show_manual_dialog = False
            st.rerun()

        if submit_btn:
            if not manual_input:
                st.error("Error: Input cannot be empty.")
            else:
                error_msg = self._validate_manual_input(manual_input)
                if error_msg:
                    st.error(error_msg)
                else:
                    st.session_state.show_manual_dialog = False
                    st.success(f"Successfully added {n} manual samples!")
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    def _validate_manual_input(self, user_input: str) -> Optional[str]:
        m = st.session_state.param_values['m']
        n = st.session_state.param_values['n']
        if not user_input.strip():
            return "Error: Input cannot be empty."
        try:
            samples = [int(x.strip()) for x in user_input.split(',')]
        except ValueError:
            return "Error: All inputs must be positive integers separated by commas."
        if n is not None and len(samples) != n:
            return f"Error: Please enter exactly {n} numbers."
        if m is not None:
            invalid_numbers = [x for x in samples if x < 1 or x > m]
            if invalid_numbers:
                return f"Error: Numbers must be between 1 and {m}."
        if len(set(samples)) != len(samples):
            return "Error: Duplicate numbers found."
        st.session_state.last_samples = samples
        self._selected_samples = samples
        return None

    def render_file_operation(self):
        st.markdown('<p class="section-header">File Operation</p>', unsafe_allow_html=True)

        self._file_list = self.db_manager.get_file_list()

        # Process button clicks from query params
        params = st.query_params
        if params.get("execute_click") == "1":
            st.session_state.execute_btn_clicked = True
        if params.get("run_click") == "1":
            st.session_state.run_btn_clicked = True
        if params.get("refresh_click") == "1":
            st.session_state.refresh_btn_clicked = True
        if params.get("delete_click") == "1":
            st.session_state.delete_btn_clicked = True

        file_html = '<div class="file-list">'
        if self._file_list:
            for fname in self._file_list:
                file_html += f'<div class="file-item">{fname}.db</div>'
        file_html += '</div>'

        # HTML-based layout - Gray buttons stacked vertically
        st.markdown(f'''
        <div class="file-op-section">
            <div class="file-op-list-col">
                <span class="param-label" style="font-size: 16px; font-weight: bold;">Available DB Files:</span>
                {file_html}
            </div>
            <div class="file-op-btn-wrapper">
            <div class="file-op-btn-grid">
                <div class="file-op-btn-left">
                    <a href="/?execute_click=1" target="_self">
                        <button class="html-btn html-btn-gray">Execute Selected</button>
                    </a>
                    <a href="/?refresh_click=1" target="_self">
                        <button class="html-btn html-btn-gray">Refresh List</button>
                    </a>
                </div>
                <div class="file-op-btn-right">
                    <a href="/?run_click=1" target="_self">
                        <button class="html-btn html-btn-gray">Run Optimal Grouping Algorithm</button>
                    </a>
                    <a href="/?delete_click=1" target="_self">
                        <button class="html-btn html-btn-gray">Delete Selected</button>
                    </a>
                </div>
            </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        # Handle clicks
        if st.session_state.refresh_btn_clicked:
            st.session_state.refresh_btn_clicked = False
            st.query_params.clear()
            st.rerun()

        if st.session_state.execute_btn_clicked:
            st.session_state.execute_btn_clicked = False
            st.query_params.clear()
            if not self._file_list:
                st.error("No files available.")
            else:
                results = self.db_manager.execute_file(self._file_list[0])
                if results:
                    st.session_state.algorithm_results = results
                    st.success(f"Successfully retrieved results from {self._file_list[0]}.db")
                    st.rerun()
                else:
                    st.error(f"No results found.")

        if st.session_state.delete_btn_clicked:
            st.session_state.delete_btn_clicked = False
            st.query_params.clear()
            if not self._file_list:
                st.error("No files to delete.")
            else:
                if self.db_manager.delete_file(self._file_list[0]):
                    st.success(f"Successfully deleted {self._file_list[0]}.db")
                    st.session_state.algorithm_results = []
                    st.rerun()
                else:
                    st.error("Failed to delete file.")

        if st.session_state.run_btn_clicked:
            st.session_state.run_btn_clicked = False
            st.query_params.clear()
            result = self.validate_parameters()
            if result:
                m, n, k, j, s = result
                samples = st.session_state.last_samples if st.session_state.last_samples else self._selected_samples
                if not samples:
                    st.error("Please select samples first.")
                else:
                    try:
                        results, info, filename = run_algorithm(m, n, k, j, s, samples)
                        if results:
                            st.session_state.algorithm_results = results
                            st.success(info)
                            st.rerun()
                        else:
                            st.error(info)
                    except Exception as e:
                        st.error(f"Algorithm Error: {str(e)}")

    def render_results_display(self):
        st.markdown('<p class="section-header">Generated k-Sample Groups Results:</p>', unsafe_allow_html=True)

        if st.session_state.algorithm_results:
            results_text = ""
            for group in st.session_state.algorithm_results:
                if all(isinstance(x, int) and 1 <= x <= 54 for x in group):
                    results_text += f"[{', '.join(str(x) for x in group)}]\n\n"
            st.markdown(f'<div class="results-display">{results_text}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="results-display"></div>', unsafe_allow_html=True)

    def run(self):
        self.render_header()
        self.render_parameter_input()
        self.render_sample_selection()
        self.render_file_operation()
        self.render_results_display()


def main():
    app = StreamlitApp()
    app.run()


if __name__ == "__main__":
    main()
