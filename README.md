# Employee Payroll Management System (Payroll Pro)

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![GUI](https://img.shields.io/badge/GUI-Tkinter%20(Standard%20Library)-00D4AA?style=flat-square)
![Dependencies](https://img.shields.io/badge/External%20Dependencies-None-FFC857?style=flat-square)
![Course](https://img.shields.io/badge/B.Tech%20CSE%20(AI)-3rd%20Semester-4C566A?style=flat-square)

An academic desktop application developed in **Python** using exclusively the built-in **`tkinter`** GUI toolkit (along with Python's standard `datetime` module for timestamps) to automate employee salary computation, attendance-based pro-rating, formatted payslip generation, and local payroll record management.

---

## Academic Submission Details

| Attribute | Details |
| :--- | :--- |
| **Project Title** | Payroll Pro — Employee Payroll Management System |
| **Author** | Aryan Pankaj Kumar |
| **Program** | B.Tech in Computer Science & Engineering (Artificial Intelligence) |
| **Semester** | 3rd Semester |
| **Subject** | Python Programming Assignment |
| **Faculty Mentor** | Bijay Sir |
| **Implementation Stack** | Python 3, `tkinter` (GUI), Standard Text File I/O (`payslips.txt`) |

---

## 1. Objective & Overview

Manual payroll computation is repetitive and prone to arithmetic and formatting errors. **Payroll Pro** addresses this by providing a lightweight, zero-dependency desktop interface where operators can enter employee details, attendance figures, and configurable allowance/deduction percentages to immediately compute earnings, deductions, and net payable salary.

The codebase is intentionally structured around clean, modular functions without third-party frameworks, making it straightforward to read, maintain, audit, and evaluate in an academic setting.

---

## 2. Core Features

- **Standard-Library Architecture**: Built purely with Python's built-in `tkinter` module (`tkinter.messagebox`, layout frames, scrollable text/list widgets) and `datetime`, requiring zero `pip` installations.
- **Pro-Rated Attendance Calculation**: Dynamically computes earned basic pay from *Days Present* relative to *Total Working Days*.
- **Configurable Allowances & Deductions**: Supports customizable **HRA %**, **DA %**, **PF %**, and **Income Tax %** with sensible pre-filled defaults (`30` days, `20%` HRA, `10%` DA, `12%` PF, `10%` Tax).
- **Read-Only Formatted Payslip Preview**: Renders an aligned, fixed-width (44-column) monospace payslip with a vertical scrollbar and Indian Rupee (`Rs.`) currency formatting.
- **Synchronized File Persistence**: Persists all generated payslips to `payslips.txt` in UTF-8 encoding, reloads existing records automatically on application startup, and synchronizes disk storage on every save, update, and deletion.
- **Record Integrity Controls**:
  - Case-insensitive duplicate Employee ID detection with an in-place update confirmation prompt.
  - Explicit confirmation dialog prior to deleting any stored record.
  - Real-time footer summary displaying total saved employees and cumulative net payout.
- **Ergonomic Desktop Interface**: Centered dark-mode layout, responsive button hover feedback, `Enter`-key calculation shortcut, and preserved list selection across focus changes.

---

## 3. Mathematical Model

Let $B$ denote Basic Salary, $D_t$ Total Working Days, $D_p$ Days Present, and $r_{\text{HRA}}, r_{\text{DA}}, r_{\text{PF}}, r_{\text{Tax}}$ the respective percentage rates.

| Component | Formula |
| :--- | :--- |
| **Earned Basic** | $\text{Basic}_{\text{earned}} = \left(\dfrac{B}{D_t}\right) \times D_p$ |
| **House Rent Allowance (HRA)** | $\text{HRA} = \text{Basic}_{\text{earned}} \times \dfrac{r_{\text{HRA}}}{100}$ |
| **Dearness Allowance (DA)** | $\text{DA} = \text{Basic}_{\text{earned}} \times \dfrac{r_{\text{DA}}}{100}$ |
| **Gross Salary** | $\text{Gross} = \text{Basic}_{\text{earned}} + \text{HRA} + \text{DA}$ |
| **Provident Fund (PF)** | $\text{PF} = \text{Basic}_{\text{earned}} \times \dfrac{r_{\text{PF}}}{100}$ |
| **Income Tax** | $\text{Tax} = \text{Gross} \times \dfrac{r_{\text{Tax}}}{100}$ |
| **Total Deductions** | $\text{Deductions} = \text{PF} + \text{Tax}$ |
| **Net Salary** | $\text{Net} = \text{Gross} - \text{Deductions}$ |

---

## 4. Input Validation Rules

| Field(s) | Validation Constraint | Error Handling |
| :--- | :--- | :--- |
| **Employee Name, Employee ID** | Must be non-empty after whitespace trimming | Blocks calculation with `Missing Data` dialog |
| **All Numeric Fields** | Valid floating-point numbers (`int` required for working days) | Blocks calculation with `Invalid Input` dialog |
| **Basic Salary** | Strictly positive finite value ($0 < B < 10^{12}$) | Blocks calculation with `Invalid Salary` dialog |
| **Working Days & Attendance** | $D_t > 0$ and $0 \le D_p \le D_t$ | Blocks calculation with `Invalid Attendance` dialog |
| **HRA %, DA %** | $0 \le r \le 200$ | Blocks calculation with `Invalid Allowance` dialog |
| **PF %, Tax %** | $0 \le r \le 100$ | Blocks calculation with `Invalid Deduction` dialog |
| **Net Salary** | $\text{Net} \ge 0$ (deductions cannot exceed gross salary) | Blocks calculation with `Invalid Deductions` dialog |

---

## 5. Sample Payslip Output

For an employee with Basic Salary `Rs. 50,000`, Attendance `28 / 30 days`, HRA `20%`, DA `10%`, PF `12%`, and Income Tax `10%`:

```text
============================================
               SALARY PAYSLIP
============================================
Name        : Aryan Pankaj Kumar
Employee ID : EMP001
Date        : 24 Nov 2026, 01:10 AM
Attendance  : 28 / 30 days
--------------------------------------------
EARNINGS
  Basic (Earned)               Rs. 46,666.67
  HRA (20%)                     Rs. 9,333.33
  DA (10%)                      Rs. 4,666.67
  Gross Salary                 Rs. 60,666.67
--------------------------------------------
DEDUCTIONS
  Provident Fund (12%)          Rs. 5,600.00
  Income Tax (10%)              Rs. 6,066.67
  Total Deductions             Rs. 11,666.67
============================================
  NET SALARY                   Rs. 49,000.00
============================================
```

---

## 6. Repository Structure

```text
employee-payroll-management-system/
├── payroll_pro.py      # Complete Tkinter GUI, payroll engine, and file persistence
├── payslips.txt        # Runtime-generated UTF-8 file storing saved payslips (gitignored)
├── .gitignore          # Excludes Python bytecode, virtualenvs, IDE files, and runtime data
└── README.md           # Academic & technical project documentation
```

---

## 7. Functional Architecture

| Module / Function Group | Key Functions | Responsibility |
| :--- | :--- | :--- |
| **Computation & Formatting** | `calculate_payroll`, `format_row`, `format_payslip` | Computes salary components and produces fixed-width payslips |
| **Input Validation** | `read_and_validate_inputs` | Parses form entries and enforces domain and range constraints |
| **Persistence Layer** | `write_records_to_file`, `parse_saved_slip`, `load_records_from_file` | Reads and synchronizes employee payslip records with `payslips.txt` |
| **Application Actions** | `calculate`, `save`, `delete`, `clear`, `on_select`, `update_total` | Handles user interactions, duplicate ID resolution, and summary updates |
| **Interface Construction** | `make_button`, `apply_defaults`, `build_gui` | Constructs the Tkinter layout, event bindings, and startup state |

---

## 8. Installation & Execution

### Prerequisites

- **Python 3.8 or higher**
- **Tkinter** (bundled by default with Python on Windows and macOS; on Debian/Ubuntu Linux install via `sudo apt-get install python3-tk`)

### Running Locally

```bash
git clone https://github.com/dat1aryan/employee-payroll-management-system.git
cd employee-payroll-management-system
python payroll_pro.py
```

---

## 9. User Guide

1. **Enter Employee Data**: Provide *Employee Name*, *Employee ID*, *Basic Salary*, and *Days Present*. Adjust *Total Working Days* or allowance/deduction percentages as required.
2. **Calculate**: Click **Calculate** (or press `Enter`) to validate inputs and inspect the formatted payslip in the preview panel.
3. **Save / Update**: Click **Save** to add the record to the *Saved Records* panel and write it to `payslips.txt`. Re-saving an existing Employee ID prompts to update that record in place.
4. **Inspect, Delete, or Reset**:
   - Select any item in **Saved Records** to display its stored payslip.
   - Click **Delete** to remove the selected record (with confirmation) and update `payslips.txt`.
   - Click **Clear** to reset all input fields to their default state.

---

## 10. Limitations & Future Scope

- **Current Scope**: Records are stored in a flat human-readable text file (`payslips.txt`) without external database engines to strictly adhere to standard-library-only constraints.
- **Planned Enhancements**:
  - Search and filter controls across saved employee records.
  - Export of payroll summaries to CSV and individual payslips to PDF.
  - Overtime hours, bonus allowances, and multi-month payroll history tracking.

---

## Acknowledgement

Developed and submitted as a **3rd Semester Python Programming Assignment** for **B.Tech CSE (Artificial Intelligence)**.  
Sincere gratitude to **Bijay Sir** for his guidance, mentorship, and instruction throughout the course.

**Author:** [Aryan Pankaj Kumar](https://www.linkedin.com/in/aryanpankajkumar/)
