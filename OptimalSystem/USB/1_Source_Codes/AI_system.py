"""
An Optimal Samples Selection System
A Tkinter-based GUI application for sample selection and optimal grouping.

This module provides a graphical interface for:
1. Parameter input with validation (m, n, k, j, s)
2. Random and manual sample selection
3. Display of selected samples and algorithm results
4. File operations for database integration

Python Version: 3.x with Tkinter standard library only
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
from typing import Dict, List, Optional
from algorithm_core import run_algorithm
from db_manager import DatabaseManager


class OptimalSamplesSelectionSystem:
    """Main application class for the Optimal Samples Selection System."""

    def __init__(self, root: tk.Tk):
        self.root = root

        self.root.title("An Optimal Samples Selection System")
        self.root.geometry("1000x800")
        self.root.resizable(False, False)

        self.COLOR_BG = '#e8f4f8'
        self.COLOR_PRIMARY = '#1565c0'
        self.COLOR_SECONDARY = '#ff6f00'
        self.COLOR_ACCENT = '#2e7d32'
        self.COLOR_TEXT_DARK = '#1a1a2e'
        self.COLOR_CARD = '#ffffff'

        self.root.configure(bg=self.COLOR_BG)

        self._configure_ttk_styles()

        self.db_manager = DatabaseManager()

        self._selected_samples: List[int] = []
        self._validation_trace = False

        self._build_ui()

    # ------------------------------------------------------------------ #
    #  ttk Button Style Configuration                                     #
    # ------------------------------------------------------------------ #
    def _configure_ttk_styles(self) -> None:
        """Create ttk styles for all colored button types."""
        style = ttk.Style(self.root)
        style.theme_use('default')

        style.layout('Colored.TButton', [
            ('Button.button', {'sticky': 'nswe', 'children': [
                ('Button.padding', {'sticky': 'nswe', 'children': [
                    ('Button.label', {'sticky': 'nswe'})
                ]})
            ]})
        ])
        style.element_create('colored.button', 'from', 'default')
        style.element_create('colored.padding', 'from', 'default')

        for color_name, color_hex in [
            ('Orange.TButton', self.COLOR_SECONDARY),
            ('Green.TButton',  self.COLOR_ACCENT),
            ('Blue.TButton',  self.COLOR_PRIMARY),
            ('Gray.TButton',  '#757575'),
        ]:
            s = ttk.Style(self.root)
            s.theme_settings('default', {
                f'{color_name}.TButton': {
                    'configure': {
                        'background': color_hex,
                        'foreground': 'white',
                        'font': ('Arial', 11, 'bold'),
                        'padding': [12, 8],
                    },
                    'layout': [
                        ('Button.button', {'sticky': 'nswe', 'border': '0', 'children': [
                            ('Button.padding', {'sticky': 'nswe', 'border': '0', 'children': [
                                ('Button.label', {'sticky': 'nswe'})
                            ]})
                        ]})
                    ],
                    'map': {
                        'background': [('active', color_hex), ('pressed', color_hex)],
                        'foreground': [('active', 'white'), ('pressed', 'white')],
                    }
                }
            })

        for color_name, color_hex, font_size in [
            ('OrangeLarge.TButton', self.COLOR_SECONDARY, 12),
            ('GreenLarge.TButton',  self.COLOR_ACCENT,   12),
        ]:
            s = ttk.Style(self.root)
            s.theme_settings('default', {
                f'{color_name}.TButton': {
                    'configure': {
                        'background': color_hex,
                        'foreground': 'white',
                        'font': ('Arial', font_size, 'bold'),
                        'padding': [20, 15],
                    },
                    'layout': [
                        ('Button.button', {'sticky': 'nswe', 'border': '0', 'children': [
                            ('Button.padding', {'sticky': 'nswe', 'border': '0', 'children': [
                                ('Button.label', {'sticky': 'nswe'})
                            ]})
                        ]})
                    ],
                    'map': {
                        'background': [('active', color_hex), ('pressed', color_hex)],
                        'foreground': [('active', 'white'), ('pressed', 'white')],
                    }
                }
            })

    # ------------------------------------------------------------------ #
    #  UI Building                                                         #
    # ------------------------------------------------------------------ #
    def _build_ui(self) -> None:
        """Build the complete user interface layout."""
        self._create_title_section()

        self.main_container = tk.Frame(self.root, bg=self.COLOR_BG)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self._create_parameter_input_frame()
        self._create_sample_selection_display_frame()
        self._create_file_operation_frame()
        self._create_result_display_frame()

    def _create_title_section(self) -> None:
        """Create the title section with primary blue background."""
        self.title_frame = tk.Frame(self.root, bg=self.COLOR_PRIMARY, height=70)
        self.title_frame.pack(fill=tk.X)
        self.title_frame.pack_propagate(False)

        self.title_label = tk.Label(
            self.title_frame,
            text="An Optimal Samples Selection System",
            font=("Arial", 20, "bold"),
            fg="white",
            bg=self.COLOR_PRIMARY,
            anchor=tk.CENTER,
            pady=15
        )
        self.title_label.pack(fill=tk.BOTH, expand=True)

    def _create_parameter_input_frame(self) -> None:
        """Create the Parameter Input Frame with 5 parameter inputs."""
        self.param_outer_frame = tk.Frame(
            self.main_container,
            bg=self.COLOR_BG,
            bd=0,
            relief=tk.FLAT
        )
        self.param_outer_frame.pack(fill=tk.X, pady=(0, 12))

        param_title = tk.Label(
            self.param_outer_frame,
            text="Parameter Input",
            font=("Arial", 13, "bold"),
            bg=self.COLOR_BG,
            fg=self.COLOR_PRIMARY,
            anchor=tk.W,
            padx=5
        )
        param_title.pack(fill=tk.X, pady=(0, 8))

        self.param_inner_frame = tk.Frame(
            self.param_outer_frame, bg=self.COLOR_CARD, padx=20, pady=15
        )
        self.param_inner_frame.pack(fill=tk.X)

        param_groups_container = tk.Frame(self.param_inner_frame, bg=self.COLOR_CARD)
        param_groups_container.pack(fill=tk.X)

        self.param_entries: Dict[str, tk.Entry] = {}

        self.param_specs = {
            'm': ('m (45-54):', 45, 54),
            'n': ('n (7-25):', 7, 25),
            'k': ('k (4-7):', 4, 7),
            'j': ('j (s ≤ j ≤ k):', 1, 7),
            's': ('s (3-7):', 3, 7)
        }

        for key in ['m', 'n', 'k', 'j', 's']:
            self._create_param_group(param_groups_container, key)

        self._bind_validation_events()

    def _create_param_group(self, parent: tk.Widget, param_key: str) -> None:
        """Create a single parameter input group."""
        label_text, min_val, max_val = self.param_specs[param_key]

        group_frame = tk.Frame(parent, bg=self.COLOR_CARD)
        group_frame.pack(side=tk.LEFT, padx=15, pady=5)

        label = tk.Label(
            group_frame,
            text=label_text,
            font=("Arial", 11),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT_DARK,
            anchor=tk.W
        )
        label.pack(fill=tk.X)

        entry = tk.Entry(
            group_frame,
            font=("Arial", 12),
            width=8,
            justify=tk.LEFT,
            bd=2,
            relief=tk.SOLID,
            highlightbackground=self.COLOR_PRIMARY,
            highlightthickness=1,
            bg='white'
        )
        entry.pack(fill=tk.X, pady=(3, 0))

        self.param_entries[param_key] = entry

    def _bind_validation_events(self) -> None:
        """Bind validation events to parameter entry fields."""
        self.param_entries['s'].bind('<FocusOut>', lambda e: self._on_param_change('s'))
        self.param_entries['s'].bind('<KeyRelease>', lambda e: self._on_param_change('s'))
        self.param_entries['k'].bind('<FocusOut>', lambda e: self._on_param_change('k'))
        self.param_entries['k'].bind('<KeyRelease>', lambda e: self._on_param_change('k'))
        self.param_entries['j'].bind('<FocusOut>', lambda e: self._validate_j_param())
        self.param_entries['j'].bind('<KeyRelease>', lambda e: self._validate_j_param())

    def _on_param_change(self, changed_param: str) -> None:
        """Handle parameter change events."""
        self._validate_j_param()

    def _validate_j_param(self) -> bool:
        """Validate the j parameter dynamically against current s and k values."""
        try:
            j_value = int(self.param_entries['j'].get())
            s_value = int(self.param_entries['s'].get())
            k_value = int(self.param_entries['k'].get())

            if j_value < s_value or j_value > k_value:
                self.param_entries['j'].delete(0, tk.END)
                messagebox.showerror(
                    "Validation Error",
                    f"Parameter j must satisfy: s ≤ j ≤ k\n"
                    f"Current valid range: {s_value} ≤ j ≤ {k_value}\n\n"
                    f"Please enter a value within this range.",
                    parent=self.root,
                )
                return False
            return True
        except ValueError:
            return True

    def _validate_parameter(self, key: str) -> Optional[int]:
        """Validate a single parameter and return its integer value."""
        min_val, max_val = self.param_specs[key][1], self.param_specs[key][2]
        entry = self.param_entries[key]

        try:
            value = int(entry.get())
            if value < min_val or value > max_val:
                messagebox.showerror(
                    "Input Error",
                    f"Parameter {key} must be between {min_val} and {max_val}.\n"
                    f"Please enter a valid positive integer.",
                    parent=self.root,
                )
                entry.delete(0, tk.END)
                entry.focus()
                return None
            return value
        except ValueError:
            messagebox.showerror(
                "Input Error",
                f"Parameter {key} must be a positive integer.\n"
                f"Please enter a valid number.",
                parent=self.root,
            )
            entry.delete(0, tk.END)
            entry.focus()
            return None

    def _validate_m_n(self) -> Optional[tuple]:
        """Validate m and n parameters specifically."""
        m = self._validate_parameter('m')
        if m is None:
            return None
        n = self._validate_parameter('n')
        if n is None:
            return None
        return (m, n)

    def _create_sample_selection_display_frame(self) -> None:
        """Create the Sample Selection & Display Frame."""
        self.sample_outer_frame = tk.Frame(
            self.main_container,
            bg=self.COLOR_BG,
            bd=0,
            relief=tk.FLAT
        )
        self.sample_outer_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))

        sample_title = tk.Label(
            self.sample_outer_frame,
            text="Sample Selection & Display",
            font=("Arial", 13, "bold"),
            bg=self.COLOR_BG,
            fg=self.COLOR_PRIMARY,
            anchor=tk.W,
            padx=5
        )
        sample_title.pack(fill=tk.X, pady=(0, 8))

        self.sample_inner_frame = tk.Frame(
            self.sample_outer_frame, bg=self.COLOR_CARD
        )
        self.sample_inner_frame.pack(fill=tk.BOTH, expand=True)

        self.sample_inner_frame.grid_rowconfigure(0, weight=1)
        self.sample_inner_frame.grid_columnconfigure(0, weight=0)
        self.sample_inner_frame.grid_columnconfigure(1, weight=1)

        self.selection_left_frame = tk.Frame(
            self.sample_inner_frame, bg=self.COLOR_CARD, bd=0
        )
        self.selection_left_frame.grid(row=0, column=0, sticky='nswe', padx=(0, 10))

        self.selection_left_frame.grid_rowconfigure(0, weight=1, uniform='vdist')
        self.selection_left_frame.grid_rowconfigure(1, weight=2, uniform='vdist')
        self.selection_left_frame.grid_rowconfigure(2, weight=2, uniform='vdist')
        self.selection_left_frame.grid_rowconfigure(3, weight=1, uniform='vdist')
        self.selection_left_frame.grid_columnconfigure(0, weight=1)

        self.random_btn = ttk.Button(
            self.selection_left_frame,
            text="Randomly Select n Samples",
            style='OrangeLarge.TButton',
            command=self._on_random_select
        )
        self.random_btn.grid(row=1, column=0, sticky='ew', padx=15, pady=5)

        self.manual_btn = ttk.Button(
            self.selection_left_frame,
            text="Manually Input n Samples",
            style='GreenLarge.TButton',
            command=self._on_manual_input
        )
        self.manual_btn.grid(row=2, column=0, sticky='ew', padx=15, pady=5)

        self.selection_right_frame = tk.Frame(
            self.sample_inner_frame, bg=self.COLOR_CARD, bd=0
        )
        self.selection_right_frame.grid(row=0, column=1, sticky='nswe')

        display_label = tk.Label(
            self.selection_right_frame,
            text="Selected n Samples:",
            font=("Arial", 11, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT_DARK,
            anchor=tk.W,
            padx=10
        )
        display_label.pack(fill=tk.X, pady=(10, 5))

        self.sample_text = scrolledtext.ScrolledText(
            self.selection_right_frame,
            font=("Courier New", 14),
            height=6,
            bg='white',
            fg=self.COLOR_TEXT_DARK,
            state=tk.DISABLED,
            relief=tk.SUNKEN,
            bd=2,
            wrap=tk.WORD,
            padx=10,
            pady=10
        )
        self.sample_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

    def _on_random_select(self) -> None:
        """Handle the 'Randomly Select n Samples' button click."""
        result = self._validate_m_n()
        if result is None:
            return

        m, n = result
        samples = random.sample(range(1, m + 1), n)
        self._selected_samples = samples
        self._display_samples(samples)

        messagebox.showinfo(
            "Success",
            f"Successfully generated {n} random samples from 1 to {m}.\n"
            f"Samples are displayed in the Sample Display area.",
            parent=self.root,
        )

    def _on_manual_input(self) -> None:
        """Handle the 'Manually Input n Samples' button click."""
        result = self._validate_m_n()
        if result is None:
            return
        self._open_manual_input_dialog()

    def _open_manual_input_dialog(self) -> None:
        """Open a dialog window for manual sample input."""
        n = int(self.param_entries['n'].get())
        m = int(self.param_entries['m'].get())

        dialog = tk.Toplevel(self.root)
        dialog.title("Manual Sample Input")
        dialog.geometry("500x280")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (280 // 2)
        dialog.geometry(f"500x280+{x}+{y}")

        dialog_frame = tk.Frame(dialog, bg=self.COLOR_CARD)
        dialog_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        instructions = tk.Label(
            dialog_frame,
            text=f"Please enter exactly {n} unique positive integers "
                 f"(from 1 to {m}), separated by commas.",
            font=("Arial", 12),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT_DARK,
            wraplength=450,
            justify=tk.LEFT
        )
        instructions.pack(anchor=tk.W, pady=(0, 15))

        example = tk.Label(
            dialog_frame,
            text=f"Example: 1,3,5,7,9,11,13 (for n={n})",
            font=("Arial", 10, "italic"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_PRIMARY
        )
        example.pack(anchor=tk.W, pady=(0, 10))

        entry_frame = tk.Frame(dialog_frame, bg=self.COLOR_CARD)
        entry_frame.pack(fill=tk.X, pady=(0, 15))

        entry = tk.Entry(
            entry_frame,
            font=("Courier New", 16),
            justify=tk.CENTER,
            bd=2,
            relief=tk.SOLID,
            bg='white',
            highlightbackground=self.COLOR_PRIMARY
        )
        entry.pack(fill=tk.X)
        entry.focus()

        error_label = tk.Label(
            dialog_frame,
            text="",
            font=("Arial", 10),
            fg='#c62828',
            bg='#ffcdd2',
            wraplength=450
        )
        error_label.pack(pady=(0, 10))

        def submit_input():
            """Validate and submit the manual input."""
            error_label.config(text="")
            user_input = entry.get().strip()

            if not user_input:
                error_label.config(
                    text="Error: Input cannot be empty. Please enter numbers."
                )
                return

            try:
                samples = [int(x.strip()) for x in user_input.split(',')]
            except ValueError:
                error_label.config(
                    text="Error: All inputs must be positive integers "
                         "separated by commas."
                )
                return

            if len(samples) != n:
                error_label.config(
                    text=f"Error: Please enter exactly {n} numbers.\n"
                         f"You entered {len(samples)} number(s)."
                )
                return

            invalid_numbers = [
                x for x in samples
                if not isinstance(x, int) or x < 1 or x > m
            ]
            if invalid_numbers:
                error_label.config(
                    text=f"Error: Numbers must be between 1 and {m}.\n"
                         f"Invalid values found: {invalid_numbers}"
                )
                return

            if len(set(samples)) != len(samples):
                duplicates = [x for x in set(samples) if samples.count(x) > 1]
                error_label.config(
                    text=f"Error: Duplicate numbers found: {duplicates}\n"
                         f"All numbers must be unique."
                )
                return

            self._selected_samples = samples
            self._display_samples(samples)
            dialog.destroy()

            messagebox.showinfo(
                "Success",
                f"Successfully added {n} manual samples.\n"
                f"Samples are displayed in the Sample Display area.",
                parent=self.root,
            )

        def cancel_input():
            dialog.destroy()

        button_frame = tk.Frame(dialog_frame, bg=self.COLOR_CARD)
        button_frame.pack(pady=(10, 0))

        submit_btn = ttk.Button(
            button_frame,
            text="Submit",
            style='Orange.TButton',
            command=submit_input
        )
        submit_btn.grid(row=0, column=0, padx=10)

        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            style='Gray.TButton',
            command=cancel_input
        )
        cancel_btn.grid(row=0, column=1, padx=10)

        entry.bind('<Return>', lambda e: submit_input())

    def _display_samples(self, samples: List[int]) -> None:
        """Display the selected samples in the sample display area."""
        self.sample_text.config(state=tk.NORMAL)
        self.sample_text.delete(1.0, tk.END)
        samples_str = ", ".join(str(s) for s in samples)
        self.sample_text.insert(tk.END, samples_str)
        self.sample_text.config(state=tk.DISABLED)

    def _create_file_operation_frame(self) -> None:
        """Create the File Operation Frame with file list."""
        self.file_outer_frame = tk.Frame(
            self.main_container,
            bg=self.COLOR_BG,
            bd=0,
            relief=tk.FLAT
        )
        self.file_outer_frame.pack(fill=tk.X, pady=(0, 12))

        file_title = tk.Label(
            self.file_outer_frame,
            text="File Operation",
            font=("Arial", 13, "bold"),
            bg=self.COLOR_BG,
            fg=self.COLOR_PRIMARY,
            anchor=tk.W,
            padx=5
        )
        file_title.pack(fill=tk.X, pady=(0, 8))

        file_inner_frame = tk.Frame(self.file_outer_frame, bg=self.COLOR_CARD)
        file_inner_frame.pack(fill=tk.X, padx=10, pady=10)

        list_frame = tk.Frame(file_inner_frame, bg=self.COLOR_CARD)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        list_label = tk.Label(
            list_frame,
            text="Available DB Files:",
            font=("Arial", 10, "bold"),
            bg=self.COLOR_CARD,
            fg=self.COLOR_TEXT_DARK
        )
        list_label.pack(anchor=tk.W)

        self.file_listbox = tk.Listbox(
            list_frame,
            height=4,
            font=("Courier New", 10),
            bg='white',
            selectmode=tk.SINGLE,
            relief=tk.SUNKEN,
            bd=1
        )
        self.file_listbox.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        btn_grid_frame = tk.Frame(file_inner_frame, bg=self.COLOR_CARD)
        btn_grid_frame.pack(side=tk.RIGHT, padx=(10, 0))

        btn_grid_frame.grid_columnconfigure(0, weight=1)
        btn_grid_frame.grid_columnconfigure(1, weight=1)

        self.run_algorithm_btn = ttk.Button(
            btn_grid_frame,
            text="Run Algorithm",
            style='Blue.TButton',
            command=self._on_run_algorithm
        )
        self.run_algorithm_btn.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        self.refresh_btn = ttk.Button(
            btn_grid_frame,
            text="Refresh List",
            style='Blue.TButton',
            command=self._refresh_file_list
        )
        self.refresh_btn.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.execute_btn = ttk.Button(
            btn_grid_frame,
            text="Execute Selected",
            style='Orange.TButton',
            command=self.execute_from_db
        )
        self.execute_btn.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        self.delete_btn = ttk.Button(
            btn_grid_frame,
            text="Delete Selected",
            style='Green.TButton',
            command=self.delete_from_db
        )
        self.delete_btn.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        self._refresh_file_list()

    def _create_result_display_frame(self) -> None:
        """Create the Result Display Frame."""
        self.result_outer_frame = tk.Frame(
            self.main_container,
            bg=self.COLOR_BG,
            bd=0,
            relief=tk.FLAT
        )
        self.result_outer_frame.pack(fill=tk.BOTH, expand=True)

        result_title = tk.Label(
            self.result_outer_frame,
            text="Generated k-Sample Groups Results:",
            font=("Arial", 13, "bold"),
            bg=self.COLOR_BG,
            fg=self.COLOR_PRIMARY,
            anchor=tk.W,
            padx=5
        )
        result_title.pack(fill=tk.X, pady=(0, 8))

        text_container = tk.Frame(self.result_outer_frame, bg=self.COLOR_BG)
        text_container.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.result_text = scrolledtext.ScrolledText(
            text_container,
            font=("Courier New", 12),
            bg='white',
            fg=self.COLOR_TEXT_DARK,
            state=tk.DISABLED,
            relief=tk.SUNKEN,
            bd=2,
            wrap=tk.WORD,
            padx=15,
            pady=15
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

        self.result_text.tag_configure(
            "group", foreground=self.COLOR_PRIMARY
        )
        self.result_text.tag_configure(
            "empty", foreground='#757575', font=("Arial", 11, "italic")
        )

        clear_container = tk.Frame(
            self.result_outer_frame, bg=self.COLOR_CARD
        )
        clear_container.pack(fill=tk.X, padx=15, pady=10)

        spacer = tk.Label(clear_container, text="", bg=self.COLOR_CARD)
        spacer.pack(side=tk.LEFT, expand=True)

        self.clear_btn = ttk.Button(
            clear_container,
            text="Clear Results",
            style='Blue.TButton',
            command=self._clear_results
        )
        self.clear_btn.pack(side=tk.RIGHT)

    def _clear_results(self) -> None:
        """Clear all content in the result text widget."""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)

    # ------------------------------------------------------------------ #
    #  Reserved Module Interaction Interfaces                             #
    # ------------------------------------------------------------------ #

    def _refresh_file_list(self) -> None:
        """Refresh the file listbox with current DB files."""
        self.file_listbox.delete(0, tk.END)
        file_list = self.db_manager.get_file_list()
        for file_name in file_list:
            self.file_listbox.insert(tk.END, file_name)

    def _on_run_algorithm(self) -> None:
        """Handle the 'Run Optimal Grouping Algorithm' button click."""
        m = self._validate_parameter('m')
        if m is None:
            return
        n = self._validate_parameter('n')
        if n is None:
            return
        k = self._validate_parameter('k')
        if k is None:
            return
        j = self._validate_parameter('j')
        if j is None:
            return
        s = self._validate_parameter('s')
        if s is None:
            return
        if not self._selected_samples:
            messagebox.showerror(
                "Error",
                "Please select samples first (Randomly or Manually).",
                parent=self.root
            )
            return
        try:
            results, info, filename = run_algorithm(
                m, n, k, j, s, self._selected_samples
            )

            if results:
                self.display_results(results)
                messagebox.showinfo("Algorithm Complete", info, parent=self.root)
                self._refresh_file_list()
            else:
                messagebox.showerror("Algorithm Error", info, parent=self.root)
        except Exception as e:
            messagebox.showerror("Algorithm Error", f"Error running algorithm: {str(e)}", parent=self.root)

    def execute_from_db(self) -> None:
        """Execute (Retrieve Results) from DB File."""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning(
                "No Selection",
                "Please select a file from the list first.",
                parent=self.root
            )
            return

        filename = self.file_listbox.get(selection[0])
        results = self.db_manager.execute_file(filename)

        if results:
            self.display_results(results)
            messagebox.showinfo(
                "Execute Successful",
                f"Successfully retrieved results from {filename}.db",
                parent=self.root
            )
        else:
            messagebox.showwarning(
                "No Results",
                f"No results found in {filename}.db",
                parent=self.root
            )

    def delete_from_db(self) -> None:
        """Delete Results from DB File."""
        selection = self.file_listbox.curselection()
        if not selection:
            messagebox.showwarning(
                "No Selection",
                "Please select a file from the list first.",
                parent=self.root
            )
            return

        filename = self.file_listbox.get(selection[0])

        if messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete {filename}.db?",
            parent=self.root
        ):
            success = self.db_manager.delete_file(filename)
            if success:
                messagebox.showinfo(
                    "Delete Successful",
                    f"Successfully deleted {filename}.db",
                    parent=self.root
                )
                self._refresh_file_list()
                self._clear_results()
            else:
                messagebox.showerror(
                    "Delete Failed",
                    f"Failed to delete {filename}.db",
                    parent=self.root
                )

    def get_parameters(self) -> Dict[str, int]:
        """Get the current input values of all parameters."""
        params = {}
        for key in self.param_specs.keys():
            value = self.param_entries[key].get()
            params[key] = int(value) if value else 0
        return params

    def get_selected_samples(self) -> List[int]:
        """Get the currently selected n samples."""
        return self._selected_samples.copy()

    def set_algorithm_results(self, results: List[List[int]]) -> None:
        """Accept and display the k-sample group results from the algorithm."""
        self.display_results(results)

    def display_results(self, results: List[List[int]]) -> None:
        """Display the k-sample group results in the Result Display Area."""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)

        if not results:
            self.result_text.insert(tk.END, "No results to display.", "empty")
        else:
            for i, group in enumerate(results):
                if all(isinstance(x, int) and 1 <= x <= 54 for x in group):
                    group_str = f"[{', '.join(str(x) for x in group)}]"
                    self.result_text.insert(tk.END, group_str, "group")
                    if i < len(results) - 1:
                        self.result_text.insert(tk.END, "\n\n")
                else:
                    print(f"Warning: Skipping invalid group at index {i}: {group}")

        self.result_text.config(state=tk.DISABLED)


# ======================================================================= #
#  Main Entry Point                                                         #
# ======================================================================= #

def main():
    """Main entry point for the Optimal Samples Selection System application."""
    root = tk.Tk()
    app = OptimalSamplesSelectionSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
