import tkinter as tk
from tkinter import messagebox
from datetime import datetime

BG = "#1e1e2e"
PANEL = "#2a2a3d"
FIELD = "#3a3a52"
SLIP_BG = "#14141f"
ACCENT = "#00d4aa"
TEXT = "#f0f0f0"
MUTED = "#9a9ab0"
DANGER = "#ff5c7a"
GOLD = "#ffc857"
DARK_FG = "#10101a"

DATA_FILE = "payslips.txt"
SLIP_WIDTH = 44
PLACEHOLDER_TEXT = (
    "\n  Welcome to Payroll Pro!\n\n"
    "  1. Enter employee details on the left.\n"
    "  2. Click 'Calculate' (or press Enter) to preview the payslip.\n"
    "  3. Click 'Save' to store the record in payslips.txt.\n"
    "  4. Click any saved record below to view or delete it."
)

FIELDS = [
    ("Employee Name", "name"),
    ("Employee ID", "id"),
    ("Basic Salary (Rs.)", "basic"),
    ("Total Working Days", "total"),
    ("Days Present", "present"),
    ("HRA %", "hra"),
    ("DA %", "da"),
    ("PF %", "pf"),
    ("Tax %", "tax"),
]

DEFAULT_VALUES = {"total": "30", "hra": "20", "da": "10", "pf": "12", "tax": "10"}

records = []
entries = {}


def calculate_payroll(basic, total_days, days_present, hra_pct, da_pct, pf_pct, tax_pct):
    earned_basic = (basic / total_days) * days_present
    hra_amt = earned_basic * hra_pct / 100
    da_amt = earned_basic * da_pct / 100
    gross_salary = earned_basic + hra_amt + da_amt

    pf_amt = earned_basic * pf_pct / 100
    tax_amt = gross_salary * tax_pct / 100
    total_deductions = pf_amt + tax_amt
    net_salary = gross_salary - total_deductions

    return {
        "earned_basic": earned_basic,
        "hra": hra_amt,
        "da": da_amt,
        "gross": gross_salary,
        "pf": pf_amt,
        "tax": tax_amt,
        "deductions": total_deductions,
        "net": net_salary,
    }


def format_row(label, amount):
    amount_text = f"Rs. {amount:,.2f}"
    return f"  {label:<24}{amount_text:>18}\n"


def format_payslip(name, emp_id, present, total, hra_pct, da_pct, pf_pct, tax_pct, pay):
    line = "=" * SLIP_WIDTH
    thin = "-" * SLIP_WIDTH
    date_str = datetime.now().strftime("%d %b %Y, %I:%M %p")

    return (
        f"{line}\n"
        f"{'SALARY PAYSLIP'.center(SLIP_WIDTH)}\n"
        f"{line}\n"
        f"Name        : {name}\n"
        f"Employee ID : {emp_id}\n"
        f"Date        : {date_str}\n"
        f"Attendance  : {present} / {total} days\n"
        f"{thin}\n"
        f"EARNINGS\n"
        + format_row("Basic (Earned)", pay["earned_basic"])
        + format_row(f"HRA ({hra_pct:g}%)", pay["hra"])
        + format_row(f"DA ({da_pct:g}%)", pay["da"])
        + format_row("Gross Salary", pay["gross"])
        + f"{thin}\n"
        f"DEDUCTIONS\n"
        + format_row(f"Provident Fund ({pf_pct:g}%)", pay["pf"])
        + format_row(f"Income Tax ({tax_pct:g}%)", pay["tax"])
        + format_row("Total Deductions", pay["deductions"])
        + f"{line}\n"
        + format_row("NET SALARY", pay["net"])
        + f"{line}\n"
    )


def read_and_validate_inputs():
    name = entries["name"].get().strip()
    emp_id = entries["id"].get().strip()

    if not name or not emp_id:
        messagebox.showerror("Missing Data", "Please enter both Employee Name and Employee ID.")
        return None

    try:
        basic = float(entries["basic"].get().strip())
        total = int(entries["total"].get().strip())
        present = int(entries["present"].get().strip())
        hra = float(entries["hra"].get().strip())
        da = float(entries["da"].get().strip())
        pf = float(entries["pf"].get().strip())
        tax = float(entries["tax"].get().strip())
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numbers in all fields.\n"
            "(Use whole numbers for Total Working Days and Days Present.)",
        )
        return None

    if not (0 < basic < 1e12):
        messagebox.showerror("Invalid Salary", "Basic Salary must be a positive number.")
        return None

    if total <= 0 or present < 0 or present > total:
        messagebox.showerror(
            "Invalid Attendance",
            "Total Working Days must be greater than 0,\n"
            "and Days Present must be between 0 and Total Working Days.",
        )
        return None

    if not (0 <= hra <= 200 and 0 <= da <= 200):
        messagebox.showerror("Invalid Allowance", "HRA % and DA % must be between 0 and 200.")
        return None

    if not (0 <= pf <= 100 and 0 <= tax <= 100):
        messagebox.showerror("Invalid Deduction", "PF % and Tax % must be between 0 and 100.")
        return None

    pay = calculate_payroll(basic, total, present, hra, da, pf, tax)
    if pay["net"] < 0:
        messagebox.showerror(
            "Invalid Deductions",
            "Total deductions exceed Gross Salary, resulting in a negative Net Salary.",
        )
        return None

    slip = format_payslip(name, emp_id, present, total, hra, da, pf, tax, pay)
    return {"id": emp_id, "name": name, "net": pay["net"], "slip": slip}


def write_records_to_file():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            for record in records:
                file.write(record["slip"] + "\n")
        return True
    except OSError as err:
        messagebox.showerror("File Error", f"Could not write to {DATA_FILE}:\n{err}")
        return False


def parse_saved_slip(block):
    name, emp_id, net = "", "", None
    for line in block.splitlines():
        if line.startswith("Name        :"):
            name = line.split(":", 1)[1].strip()
        elif line.startswith("Employee ID :"):
            emp_id = line.split(":", 1)[1].strip()
        elif "NET SALARY" in line and "Rs." in line:
            amount_part = line.split("Rs.", 1)[1].strip().replace(",", "")
            try:
                net = float(amount_part)
            except ValueError:
                net = None

    if name and emp_id and net is not None:
        return {"id": emp_id, "name": name, "net": net, "slip": block.strip() + "\n"}
    return None


def load_records_from_file():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            content = file.read().strip()
    except OSError:
        return

    for block in content.split("\n\n"):
        parsed = parse_saved_slip(block)
        if parsed:
            records.append(parsed)
            listbox.insert(tk.END, format_list_entry(parsed))
    update_total()


def format_list_entry(record):
    return f"{record['name']} ({record['id']})  -  Rs. {record['net']:,.2f}"


def show_slip(text):
    slip_box.config(state=tk.NORMAL)
    slip_box.delete("1.0", tk.END)
    slip_box.insert(tk.END, text)
    slip_box.config(state=tk.DISABLED)


def update_total():
    total_pay = sum(record["net"] for record in records)
    total_label.config(text=f"Employees: {len(records)}   |   Total Payout: Rs. {total_pay:,.2f}")


def find_record_index_by_id(emp_id):
    for idx, record in enumerate(records):
        if record["id"].lower() == emp_id.lower():
            return idx
    return None


def calculate(event=None):
    record = read_and_validate_inputs()
    if record:
        show_slip(record["slip"])


def save():
    record = read_and_validate_inputs()
    if record is None:
        return

    existing_idx = find_record_index_by_id(record["id"])
    if existing_idx is not None:
        should_update = messagebox.askyesno(
            "Duplicate Employee ID",
            f"Employee ID '{record['id']}' already exists.\n"
            "Do you want to update the existing record?",
        )
        if not should_update:
            return
        records[existing_idx] = record
        listbox.delete(existing_idx)
        listbox.insert(existing_idx, format_list_entry(record))
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(existing_idx)
        status_msg = f"Updated payslip for {record['name']} ({record['id']}) in {DATA_FILE}."
    else:
        records.append(record)
        listbox.insert(tk.END, format_list_entry(record))
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(tk.END)
        status_msg = f"Payslip saved to {DATA_FILE}."

    show_slip(record["slip"])
    update_total()
    if write_records_to_file():
        messagebox.showinfo("Saved", status_msg)


def on_select(event):
    selection = listbox.curselection()
    if selection:
        show_slip(records[selection[0]]["slip"])


def delete():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("No Selection", "Please select a saved record to delete.")
        return

    idx = selection[0]
    record = records[idx]
    if not messagebox.askyesno("Confirm Delete", f"Delete payslip for {record['name']} ({record['id']})?"):
        return

    listbox.delete(idx)
    records.pop(idx)
    show_slip(PLACEHOLDER_TEXT)
    update_total()
    write_records_to_file()


def apply_defaults():
    for key, value in DEFAULT_VALUES.items():
        entries[key].insert(0, value)


def clear():
    for entry in entries.values():
        entry.delete(0, tk.END)
    apply_defaults()
    listbox.selection_clear(0, tk.END)
    show_slip(PLACEHOLDER_TEXT)
    entries["name"].focus()


def make_button(parent, text, color, command, width=12):
    btn = tk.Button(
        parent, text=text, font=("Segoe UI", 11, "bold"), bg=color, fg=DARK_FG,
        activebackground=TEXT, activeforeground=DARK_FG, bd=0, padx=10, pady=8,
        width=width, cursor="hand2", command=command,
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=TEXT))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    return btn


def build_gui():
    global root, slip_box, listbox, total_label

    root = tk.Tk()
    root.title("Payroll Pro - Employee Payroll Management System")
    root.configure(bg=BG)

    win_w, win_h = 1080, 690
    pos_x = max((root.winfo_screenwidth() - win_w) // 2, 0)
    pos_y = max((root.winfo_screenheight() - win_h) // 2 - 20, 0)
    root.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
    root.minsize(1000, 660)
    root.bind("<Return>", calculate)

    header = tk.Frame(root, bg=BG)
    header.pack(fill=tk.X, pady=(10, 8))
    tk.Label(header, text="PAYROLL PRO", font=("Segoe UI", 22, "bold"), bg=BG, fg=ACCENT).pack()
    tk.Label(header, text="Employee Payroll Management System", font=("Segoe UI", 11), bg=BG, fg=MUTED).pack()

    main = tk.Frame(root, bg=BG)
    main.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 16))

    left = tk.Frame(main, bg=PANEL, padx=20, pady=15)
    left.pack(side=tk.LEFT, fill=tk.Y)
    tk.Label(left, text="Employee Details", font=("Segoe UI", 14, "bold"),
             bg=PANEL, fg=GOLD).grid(row=0, column=0, columnspan=2, pady=(0, 12))

    for row_idx, (label_text, key) in enumerate(FIELDS, start=1):
        tk.Label(left, text=label_text, font=("Segoe UI", 11), bg=PANEL, fg=TEXT,
                 anchor="w", width=18).grid(row=row_idx, column=0, pady=4, sticky="w")
        entry = tk.Entry(left, font=("Segoe UI", 11), bg=FIELD, fg=TEXT,
                         insertbackground=ACCENT, bd=0, width=19, relief=tk.FLAT)
        entry.grid(row=row_idx, column=1, pady=4, ipady=5, padx=(8, 0))
        entries[key] = entry

    apply_defaults()

    btn_frame = tk.Frame(left, bg=PANEL)
    btn_frame.grid(row=len(FIELDS) + 1, column=0, columnspan=2, pady=(20, 0))
    make_button(btn_frame, "Calculate", ACCENT, calculate).grid(row=0, column=0, padx=5, pady=5)
    make_button(btn_frame, "Save", GOLD, save).grid(row=0, column=1, padx=5, pady=5)
    make_button(btn_frame, "Clear", MUTED, clear).grid(row=1, column=0, padx=5, pady=5)
    make_button(btn_frame, "Delete", DANGER, delete).grid(row=1, column=1, padx=5, pady=5)

    right = tk.Frame(main, bg=PANEL, padx=16, pady=15)
    right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(16, 0))
    tk.Label(right, text="Payslip Preview", font=("Segoe UI", 14, "bold"),
             bg=PANEL, fg=GOLD).pack(anchor="w", pady=(0, 8))

    slip_frame = tk.Frame(right, bg=SLIP_BG)
    slip_frame.pack(fill=tk.BOTH, expand=True)
    slip_scroll = tk.Scrollbar(slip_frame)
    slip_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    slip_box = tk.Text(
        slip_frame, font=("Consolas", 10), bg=SLIP_BG, fg=ACCENT, bd=0,
        height=22, width=48, padx=14, pady=10, state=tk.DISABLED,
        yscrollcommand=slip_scroll.set,
    )
    slip_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    slip_scroll.config(command=slip_box.yview)

    bottom = tk.Frame(right, bg=PANEL, pady=6)
    bottom.pack(fill=tk.X, pady=(10, 0))
    tk.Label(bottom, text="Saved Records  (click any record to view)",
             font=("Segoe UI", 11, "bold"), bg=PANEL, fg=GOLD).pack(anchor="w")

    list_frame = tk.Frame(bottom, bg=PANEL)
    list_frame.pack(fill=tk.X, pady=6)
    list_scroll = tk.Scrollbar(list_frame)
    list_scroll.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(
        list_frame, font=("Segoe UI", 10), bg=FIELD, fg=TEXT,
        selectbackground=ACCENT, selectforeground=DARK_FG, bd=0, height=4,
        exportselection=False, activestyle="none", yscrollcommand=list_scroll.set,
    )
    listbox.pack(fill=tk.X)
    list_scroll.config(command=listbox.yview)
    listbox.bind("<<ListboxSelect>>", on_select)

    total_label = tk.Label(bottom, text="Employees: 0   |   Total Payout: Rs. 0.00",
                           font=("Segoe UI", 11, "bold"), bg=PANEL, fg=ACCENT)
    total_label.pack(anchor="e", pady=(2, 0))

    show_slip(PLACEHOLDER_TEXT)
    load_records_from_file()
    entries["name"].focus()
    root.mainloop()


if __name__ == "__main__":
    build_gui()
