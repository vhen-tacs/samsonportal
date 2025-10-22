import os, tkinter.font as font
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as font
from tkinter import messagebox, simpledialog
import random
from PIL import ImageTk, Image, ImageDraw


ADMIN_CREDENTIALS = {"username": "admin", "password": "123"}
REGISTRAR_CREDENTIALS = {"username":"registrar", "password":"pcdrgs"}
ACCOUNTING_CREDENTIALS = {"username":"accounting", "password":"pcdacctg"}
HRMS_CREDENTIALS = {"username":"hrms", "password":"pcdhrms"}

# Global requirements lists
REQUIREMENTS_FRESHMEN = [
    "Form 138 (HS Report Card)",
    "Certificate of Good Moral Character",
    "NSO/PSA Birth Certificate",
    "2x2 ID Pictures",
    "Medical Certificate",
    "Entrance Exam Result",
    "Barangay Clearance"
]

REQUIREMENTS_TRANSFEREE = [
    "Honorable Dismissal / Transfer Credential",
    "Transcript of Records (TOR)",
    "Certificate of Good Moral Character",
    "NSO/PSA Birth Certificate",
    "2x2 ID Pictures",
    "Medical Certificate"
]


#  enrolled student data
student_records = {}

billing_records = {}
#subjects
course_subjects = {
    "BSIT": {
        "1": [("Intro to Programming", 3), ("Math 1", 2), ("English 1", 2), ("PE 1", 2),
              ("Computer Ethics", 2), ("Digital Logic", 3), ("NSTP 1", 2), ("IT Fundamentals", 2)],
        "2": [("Data Structures", 3), ("Math 2", 2), ("English 2", 2), ("PE 2", 2),
              ("Web Dev", 3), ("Computer Architecture", 3), ("NSTP 2", 2), ("OOP", 3), ("Sociology", 2), ("Database", 3)],
        "3": [("Networking", 3), ("Software Eng.", 3), ("Mobile App Dev", 3), ("Thesis 1", 3)],
        "4": [("Capstone", 3), ("Internship", 3), ("Project Management", 2), ("IT Laws", 2)]
    },
    "BSBA": {
        "1": [("Accounting 1", 3), ("Business Math", 2), ("English 1", 2), ("PE 1", 2),
              ("Marketing 1", 3), ("NSTP 1", 2), ("Microeconomics", 3), ("Business Law", 3)],
        "2": [("Accounting 2", 3), ("Business Ethics", 2), ("English 2", 2), ("PE 2", 2),
              ("Marketing 2", 3), ("NSTP 2", 2), ("Macroeconomics", 3), ("Entrepreneurship", 3), ("IT for Business", 2), ("Statistics", 2)],
        "3": [("Strategic Mngmt", 3), ("Business Research", 3), ("Org Behavior", 2), ("Taxation", 3)],
        "4": [("Internship", 3), ("Feasibility Study", 3), ("Business Planning", 2), ("HRM", 2)]
    },
    "HRM": {
        "1": [("Intro to Hospitality", 3), ("Food & Beverage Service 1", 3), ("English 1", 2), ("PE 1", 2),
              ("Kitchen Operations", 3), ("NSTP 1", 2), ("Sanitation & Safety", 2), ("Business Math", 2)],
        "2": [("Food & Beverage Service 2", 3), ("Front Office Mngmt", 3), ("English 2", 2), ("PE 2", 2),
              ("Housekeeping Operations", 3), ("NSTP 2", 2), ("Bakery & Pastry", 3), ("Hospitality Accounting", 2), ("Tourism Principles", 2)],
        "3": [("Event Mngmt", 3), ("Culinary Arts", 3), ("Hospitality Marketing", 3), ("Research in HRM", 3)],
        "4": [("Internship", 3), ("Hospitality Law", 2), ("Facilities Mngmt", 2), ("Strategic HRM", 2)]
    },
    "BSTM": {
        "1": [("Intro to Tourism", 3), ("Tourism Geography", 3), ("English 1", 2), ("PE 1", 2),
              ("Business Math", 2), ("NSTP 1", 2), ("History of Tourism", 2), ("Marketing Principles", 3)],
        "2": [("Tourism Planning", 3), ("Tour Guiding", 3), ("English 2", 2), ("PE 2", 2),
              ("NSTP 2", 2), ("Cultural Tourism", 3), ("Statistics", 2), ("Travel Agency Operations", 3), ("Ecotourism", 2), ("Hospitality Basics", 2)],
        "3": [("Tourism Research", 3), ("Airline & Cruise Operations", 3), ("Event & Convention Mngmt", 3), ("Sustainable Tourism", 3)],
        "4": [("Internship", 3), ("Tourism Law", 2), ("Strategic Tourism Mngmt", 2), ("Entrepreneurship in Tourism", 2)]
    }
}

# default login credentials (username = last name, password = student ID)
student_login = {}# example: "delacruz": "123456"

# enrolled subjects
enrolled_subjects = {}





root = None
main_frame = None 

student_id_counter = 1000
NEXT_STUDENT_ID = 1  
NEXT_RECEIPT_NUMBER = 11000000001


def generate_student_id():
    global NEXT_STUDENT_ID
    student_id = f"{NEXT_STUDENT_ID:06d}"
    NEXT_STUDENT_ID += 1
    return student_id

def generate_receipt_number():
    global NEXT_RECEIPT_NUMBER
    receipt_number = f"RCP-{NEXT_RECEIPT_NUMBER}"
    NEXT_RECEIPT_NUMBER += 1
    return receipt_number

def generate_transaction_number():
    
    number = random.randint(10000000, 99999999)
    return f"TXN-{number}"

def clear_main_frame():
    global main_frame
    if main_frame is not None:
        main_frame.destroy()
        main_frame = None
        
def add_student_to_records(student_id, name, course, year_level, units):
    student_records[student_id] = {
        "name": name,
        "course": course,
        "year_level": year_level
    }

    tuition_fee = units * 500
    charges = {
        f"Tuition Fee (500 x {units})": tuition_fee,
        "Athletics Fee": 500.00,
        "Library Fee": 750.00,
        "Internet Fee": 300.00
    }

    billing_records[student_id] = {
        "name": name,
        "student_id": student_id,
        "course": course,
        "year_level": year_level,
        "units": units,
        "charges": charges,
        "paid": 0.0
    }
    for sid, student in student_records.items():
        if sid not in billing_records:
            add_student_to_records(sid, student['name'], student['course'], student['year_level'], 0)
    

def show_start_mainportal_frame():
    clear_main_frame()
    global main_frame
    
    main_frame = Frame(root)
    main_frame.place(x=0, y=0, relwidth=1, relheight=1)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, "frontbgfinal.png")
    image = Image.open(image_path)
    image = image.resize((1400, 800), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    background_label = Label(main_frame, image=photo)
    background_label.image = photo  
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    login_entry_font = font.Font(family="Helvetica", size=18, slant="italic")

    # Student ID entry
    student_login = tk.Entry(main_frame, font=login_entry_font, width=15,bg="#1E90FF", fg="white", insertbackground="white",relief="flat", highlightthickness=2, highlightbackground="#4682B4")
    student_login.place(x=570,y=347)

    # Hover effect helper
    def add_hover_effect(widget, base_color, hover_color):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_color))
        widget.bind("<Leave>", lambda e: widget.config(bg=base_color))

    # Function to validate student login
    def student_login_enter():
        student_id = student_login.get().strip()
        if student_id in billing_records:
            username = student_records[student_id]['last_name'].lower()
            open_student_login(username_prefill=username, student_id_expected=student_id)
        else:
            messagebox.showerror("Error", "Student ID not found.")

    # Student Enter button
    enter1 = tk.Button(main_frame, text="Enter", font=("Garamond", 16),
                       width=15, height=1, bg="#1E90FF", fg="blue",
                       relief="flat", command=student_login_enter)
    enter1.place(x=578, y=460)
    add_hover_effect(enter1, "#1E90FF", "#4682B4")

    # Administrator login button
    enter2 = tk.Button(main_frame, text="Administrator", font=("Garamond", 16),
                       width=20, height=2, bg="#20B2AA", fg="blue",
                       relief="flat", command=show_login_frame)
    enter2.place(x=558,y=570)
    add_hover_effect(enter2, "#20B2AA", "#3CB371")
    
def student_view(student_id):
    clear_main_frame()
    global main_frame

    main_frame = ttk.LabelFrame(root, text="Student Information", padding=20)
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    balance = show_billing(main_frame, student_id)

    if balance is None:
        Button(main_frame, text="Go Back", command=show_start_mainportal_frame).pack(pady=10)
        return

    
    if balance > 0:
        ttk.Label(main_frame, text="Enter Payment Amount:").pack(pady=(10, 0))
        payment_entry = ttk.Entry(main_frame)
        payment_entry.pack()

        def make_payment():
            try:
                amount = float(payment_entry.get())
                if amount <= 0:
                    messagebox.showerror("Error", "Enter a positive amount.")
                    return

                billing_records[student_id]["paid"] += amount
                billing_records[student_id]["receipt_no"] = generate_receipt_number()
                billing_records[student_id]["trans_no"] = generate_transaction_number()

                messagebox.showinfo("Success", f"Payment of ₱{amount:.2f} recorded successfully.")
                student_view(student_id)  
            except ValueError:
                messagebox.showerror("Error", "Enter a valid number.")

        ttk.Button(main_frame, text="Pay", command=make_payment).pack(pady=5)

    elif balance < 0:
        change_amount = abs(balance)
        ttk.Label(main_frame, text=f"Change: ₱{change_amount:.2f}", foreground="green").pack(pady=5)
        

    else:
        ttk.Label(main_frame, text="Your balance is fully paid.").pack(pady=5)

    ttk.Button(main_frame, text="View Receipt", command=lambda: show_receipt_frame(student_id)).pack(pady=5)
    ttk.Button(main_frame, text="Go Back", command=lambda: open_student_portal(student_id)).pack(pady=10)



def open_student_login(username_prefill=None, student_id_expected=None):
    clear_main_frame()
    global main_frame
    main_frame = Frame(root)
    main_frame.place(x=0, y=0, relwidth=1, relheight=1)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, "studentlogin.png")
    image = Image.open(image_path)
    image = image.resize((1400, 800), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    background_label = Label(main_frame, image=photo)
    background_label.image = photo  
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    login_font = font.Font(family="Georgia", size=25)
    button_font = font.Font(family="Garamond", size=15)

    def attempt_login():
        uname = username_entry.get().lower()
        pwd = password_entry.get()
        if (uname == username_prefill) and (pwd == student_id_expected):
            open_student_portal(student_id_expected)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")


    
    username_entry = tk.Entry(main_frame, font=login_font, width = 15)
    username_entry.place(x=550, y=225)
    if username_prefill:
        username_entry.insert(0, username_prefill)
        username_entry.config(state='readonly')

    
    password_entry = tk.Entry(main_frame, show="*", font=login_font, width=15)
    password_entry.place(x=550,y=351)

    tk.Button(main_frame, text="Login", command=attempt_login,font=button_font, height=2, width=7).place(x=500, y=450)
    tk.Button(main_frame, text="Go Back", command=lambda: [show_start_mainportal_frame()], font=button_font, height=2, width=7).place(x=750, y=450)
    

def open_student_portal(student_id):
    global main_frame
    clear_main_frame()
    
    if student_id not in student_records:
        messagebox.showerror("Error", "Student record not found.")
        return

    student = student_records[student_id]
    enrolled = enrolled_subjects.get(student_id, [])
    
    main_frame = ttk.LabelFrame(root, text=f"Student Portal - {student.get('name', student.get('last_name', ''))}", padding=20)
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # student info
    info_frame = ttk.LabelFrame(main_frame, text="Student Information", padding=15)
    info_frame.pack(fill="x", pady=(0, 15))
    
    # student details
    details = [
        ("Full Name", student.get("name", f"{student.get('last_name', '')}, {student.get('first_name', '')} {student.get('middle_name', '')}").strip()),
        ("Student ID", student_id),
        ("Course", student.get("course", "")),
        ("Year Level", student.get("year_level", "")),
        ("Gender", student.get("gender", "")),
        ("Address", student.get("address", "")),
        ("Birthdate", student.get("birthdate", "")),
        ("Age", student.get("age", ""))
    ]

    for label, value in details:
        ttk.Label(info_frame, text=f"{label}: {value}").pack(anchor="w")

    # enrolled subjects treeview
    tree_frame = ttk.LabelFrame(main_frame, text="Enrolled Subjects", padding=15)
    tree_frame.pack(fill="both", expand=True, pady=(0, 15))
    
    tree = ttk.Treeview(tree_frame, columns=("Subject", "Units"), show="headings", height=8)
    tree.heading("Subject", text="Subject")
    tree.heading("Units", text="Units")
    tree.column("Subject", anchor=W, width=300)
    tree.column("Units", anchor=CENTER, width=80)
    tree.pack(fill="both", expand=True)

    # tree with enrolled subjects
    for subject, units in enrolled:
        tree.insert("", "end", values=(subject, units))


    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(fill="x", pady=(0, 10))

    def enroll_subjects():
        # enrollment window to choose subjects to add
        enroll_window = tk.Toplevel(root)
        enroll_window.title("Enroll Subjects")
        enroll_window.geometry("480x400")
        enroll_window.grab_set()

        available_subjects = []
        course = student.get("course", "")
        year_level_raw = student.get("year_level", "1")
        # convert year_level to string number
        year_level = year_level_raw.strip().lower()
        if year_level in ("1st", "1"):
            year_level = "1"
        elif year_level in ("2nd", "2"):
            year_level = "2"
        elif year_level in ("3rd", "3"):
            year_level = "3"
        elif year_level in ("4th", "4"):
            year_level = "4"
        else:
            year_level = "1"
        available_subjects = course_subjects.get(course, {}).get(year_level, [])

        # subjects already enrolled
        current_subjects = enrolled_subjects.get(student_id, [])
        current_subj_names = [s[0] for s in current_subjects]
        subjects_to_enroll = [sub for sub in available_subjects if sub[0] not in current_subj_names]

        if not subjects_to_enroll:
            messagebox.showinfo("Info", "No new subjects available to enroll.")
            enroll_window.destroy()
            return

        # listbox for subjects selection
        label = ttk.Label(enroll_window, text="Select subjects to enroll (Ctrl+Click for multiple):")
        label.pack(pady=10)

        listbox = tk.Listbox(enroll_window, selectmode=tk.MULTIPLE, height=15)
        for subj, units in subjects_to_enroll:
            listbox.insert(tk.END, f"{subj} ({units} units)")
        listbox.pack(fill="both", expand=True, padx=20)

        def confirm_enroll():
            selected_subs = listbox.curselection()
            if not selected_subs:
                messagebox.showwarning("No Selection", "Please select at least one subject to enroll.")
                return
            for idx in selected_subs:
                subj_text = listbox.get(idx)
                if "(" in subj_text and "units)" in subj_text:
                    subj_name = subj_text.split(" (")[0]
                    units_str = subj_text.split("(")[1].split(" ")[0]
                    try:
                        units = int(units_str)
                    except:
                        units = 0
                    # append to enrolled list
                    if student_id not in enrolled_subjects:
                        enrolled_subjects[student_id] = []
                    if (subj_name, units) not in enrolled_subjects[student_id]:
                        enrolled_subjects[student_id].append((subj_name, units))
                        tree.insert("", "end", values=(subj_name, units))

            messagebox.showinfo("Enrollment", "Selected subject(s) enrolled successfully.")
            enroll_window.destroy()

        btn_confirm = ttk.Button(enroll_window, text="Enroll", command=confirm_enroll)
        btn_confirm.pack(pady=10)

    def drop_subjects():
        selected_items = tree.selection()
        if not selected_items:
            messagebox.showwarning("No Selection", "Please select subjects to drop.")
            return
        confirm = messagebox.askyesno("Confirm Drop", "Are you sure you want to drop the selected subjects?")
        if not confirm:
            return
        enrolled = enrolled_subjects.get(student_id, [])
        for item in selected_items:
            subj = tree.item(item, "values")[0]
            enrolled[:] = [s for s in enrolled if s[0] != subj]
            tree.delete(item)
        enrolled_subjects[student_id] = enrolled
        messagebox.showinfo("Dropped", "Selected subject(s) dropped successfully.")

    def logout():
        clear_main_frame()
        show_start_mainportal_frame()

    btn_padding = {'padx': 10, 'pady': 5, 'expand': True}

    btn_enroll = ttk.Button(btn_frame, text="Enroll Subjects", command=enroll_subjects)
    btn_enroll.pack(side=LEFT, **btn_padding)

    btn_pay = ttk.Button(btn_frame, text="Pay Balance", command=lambda: student_view(student_id))
    btn_pay.pack(side=LEFT, **btn_padding)

    btn_receipt = ttk.Button(btn_frame, text="View Receipt", command=lambda: show_receipt_frame(student_id))
    btn_receipt.pack(side=LEFT, **btn_padding)

    btn_drop = ttk.Button(btn_frame, text="Drop Subjects", command=drop_subjects)
    btn_drop.pack(side=LEFT, **btn_padding)

    btn_logout = ttk.Button(btn_frame, text="Logout", command=logout)
    btn_logout.pack(side=LEFT, **btn_padding)

def show_receipt_frame(student_id):
    data = billing_records.get(student_id)
    if not data:
        messagebox.showerror("Error", f"No billing record found for Student ID: {student_id}")
        return

    total_charge = sum(data['charges'].values())
    amount_paid = data['paid']
    balance_due = max(0, total_charge - amount_paid)
    change_due = amount_paid - total_charge if amount_paid > total_charge else 0.0

    # Create a new Toplevel window instead of clearing main_frame
    receipt_win = tk.Toplevel(root)
    receipt_win.title("Official Receipt")
    receipt_win.geometry("650x850")
    receipt_win.configure(bg="white")

    card = tk.Frame(receipt_win, bg="white", bd=2, relief="ridge")
    card.pack(padx=20, pady=20, fill="both", expand=True)

    # fonts
    header_font = font.Font(family="Arial", size=20, weight="bold")
    subheader_font = font.Font(family="Arial", size=14)
    body_font = font.Font(family="Arial", size=11)
    body_bold_font = font.Font(family="Arial", size=11, weight="bold")
    italic_font = font.Font(family="Arial", size=10, slant="italic")
    positive_font = font.Font(family="Arial", size=11, weight="bold")
    negative_font = font.Font(family="Arial", size=11, weight="bold")

    # header Labels
    tk.Label(card, text="Samson Polytechnic", font=header_font, bg="white", fg="black").pack(pady=(20, 5))
    tk.Label(card, text="Official School Receipt", font=subheader_font, bg="white", fg="black").pack(pady=(0, 20))

    # receipt & Transaction numbers frame
    num_frame = tk.Frame(card, bg="white")
    num_frame.pack(fill="x", padx=20, pady=(0, 15))
    tk.Label(num_frame, text=f"Receipt No: {data.get('receipt_no', 'N/A')}", font=body_font, bg="white", fg="black")\
        .pack(side="left", anchor="w")
    tk.Label(num_frame, text=f"Transaction No: {data.get('trans_no', 'N/A')}", font=body_font, bg="white", fg="black")\
        .pack(side="right", anchor="e")

    # student Information
    info_frame = tk.Frame(card, bg="white")
    info_frame.pack(fill="x", padx=20, pady=(0, 35))

    student_info_data = {
        "Name": data['name'],
        "Student ID": student_id,
        "Course": data['course'],
        "Year Level": data['year_level'],
        "Units Enrolled": data['units'],
    }

    for label_text, value_text in student_info_data.items():
        row = tk.Frame(info_frame, bg="white")
        row.pack(fill="x", pady=3)
        tk.Label(row, text=f"{label_text}:", font=body_font, bg="white", width=15, anchor="w")\
            .pack(side="left")
        tk.Label(row, text=value_text, font=body_font, bg="white", anchor="w", justify="left", wraplength=400)\
            .pack(side="left", fill="x", expand=True)

    # horizontal separator 
    tk.Frame(card, bg="black", height=2).pack(fill="x", padx=20, pady=(0, 25))

    # charges headers
    charges_header = tk.Frame(card, bg="white")
    charges_header.pack(fill="x", padx=20)
    tk.Label(charges_header, text="Description", font=body_bold_font, bg="white").pack(side="left", anchor="w")
    tk.Label(charges_header, text="Amount (₱)", font=body_bold_font, bg="white").pack(side="right", anchor="e")

    # charges list
    for desc, amount in data["charges"].items():
        row = tk.Frame(card, bg="white")
        row.pack(fill="x", padx=20, pady=3)
        tk.Label(row, text=desc, font=body_font, bg="white", anchor="w").pack(side="left", fill="x", expand=True)
        tk.Label(row, text=f"{amount:,.2f}", font=body_font, bg="white", anchor="e", width=12).pack(side="right")

    # bottom separator
    tk.Frame(card, bg="black", height=2).pack(fill="x", padx=20, pady=(25, 15))

    # summary section
    summary_frame = tk.Frame(card, bg="white")
    summary_frame.pack(fill="x", padx=20)

    def create_summary_row(label_text, value_text, font_style):
        row = tk.Frame(summary_frame, bg="white")
        row.pack(fill="x", pady=6)
        tk.Label(row, text=label_text, font=font_style, bg="white").pack(side="left", anchor="w")
        tk.Label(row, text=value_text, font=font_style, bg="white").pack(side="right", anchor="e")

    create_summary_row("Total:", f"₱{total_charge:,.2f}", body_bold_font)
    create_summary_row("Amount Paid:", f"₱{amount_paid:,.2f}", body_bold_font)

    if change_due > 0:
        create_summary_row("Change:", f"₱{change_due:,.2f}", positive_font)
    else:
        create_summary_row("Balance Due:", f"₱{balance_due:,.2f}", negative_font)

    # thank you message
    tk.Label(card, text="Thank you for your payment!\nHave a great day!", 
             font=italic_font, bg="white", justify="center").pack(pady=(35, 30), fill="x")

    # back button (closes window)
    tk.Button(card, text="Close", font=body_bold_font, command=receipt_win.destroy, padx=15, pady=7)\
        .pack(pady=(0, 20))

def show_billing(frame, student_id):
    data = billing_records.get(student_id)
    if not data:
        messagebox.showerror("Error", "No billing record found for this student ID.")
        return None

    ttk.Label(frame, text=f"Student Name: {data['name']}").pack(anchor="w", padx=10)
    ttk.Label(frame, text=f"Student ID: {student_id}").pack(anchor="w", padx=10)
    ttk.Label(frame, text=f"Course: {data['course']}").pack(anchor="w", padx=10)
    ttk.Label(frame, text=f"Year Level: {data['year_level']}").pack(anchor="w", padx=10)
    ttk.Label(frame, text=f"Number of Units: {data['units']}").pack(anchor="w", padx=10)

    tree = ttk.Treeview(frame, columns=("desc", "amount"), show="headings", height=5)
    tree.heading("desc", text="Charge Description")
    tree.heading("amount", text="Amount")
    tree.column("desc", width=250)
    tree.column("amount", anchor="e", width=100)

    total = 0
    for charge, amount in data['charges'].items():
        tree.insert('', 'end', values=(charge, f"{amount:,.2f}"))
        total += amount
    tree.pack(pady=10)

    paid = data.get("paid", 0.0)
    balance = total - paid

    display_balance = max(0.0, balance)

    ttk.Label(frame, text=f"Amount Paid: ₱{paid:,.2f}", font=("Arial", 10)).pack()
    ttk.Label(frame, text=f"Total Balance: ₱{display_balance:,.2f}", font=("Arial", 12, "bold")).pack()

    if balance < 0:
        change_amount = abs(balance)
        ttk.Label(frame, text=f"Change: ₱{change_amount:,.2f}", font=("Arial", 12, "bold"), foreground="green").pack()
    return balance


    
def admin_front_page():
    clear_main_frame()
    global main_frame
    def make_transparent_button(w, h, color, alpha, text, cmd, font):
        """Create a button with a semi-transparent background."""
        img = Image.new("RGBA", (w, h), color + (alpha,))
        photo = ImageTk.PhotoImage(img)

        btn = tk.Button(
            btn_box,
            image=photo,
            text=text,
            compound="center",
            font=font,
            fg="white",
            borderwidth=0,
            highlightthickness=0,
            command=cmd
        )
        btn.image = photo  # prevent garbage collection
        return btn


    # Main frame with background image
    main_frame = tk.Frame(root)
    main_frame.place(x=0, y=0, relwidth=1, relheight=1)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(base_dir, "adminpanel.png")
    image = Image.open(image_path).resize((1400, 800), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    background_label = Label(main_frame, image=photo)
    background_label.image = photo  
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    button_font = font.Font(family="Garamond", size=18)

    # Function to add hover glow effect
    def add_hover_effect(widget, base_color, hover_color):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_color))
        widget.bind("<Leave>", lambda e: widget.config(bg=base_color))

    # Registrar button
    registrar_btn = tk.Button(main_frame, text="Registrar", font=button_font, width=18, height=2,
                              bg="#1E90FF", fg="black", activeforeground="blue", relief="flat",
                              command=registrar_login)
    registrar_btn.place(x=580, y=220)
    add_hover_effect(registrar_btn, "#1E90FF", "#4682B4")  # glow on hover

    # Accounting button
    accounting_btn = tk.Button(main_frame, text="Accounting", font=button_font, width=18, height=2,
                               bg="#20B2AA", fg="black", activeforeground="blue", relief="flat",
                               command=accounting_login)
    accounting_btn.place(x=580, y=280)
    add_hover_effect(accounting_btn, "#20B2AA", "#3CB371")

    # Human resource button
    hrs_btn = tk.Button(main_frame, text="Human Resource", font=button_font, width=18, height=2,
                               bg="#20B2AA", fg="black", activeforeground="blue", relief="flat",
                               command=hrs_login)
    hrs_btn.place(x=580, y=350)
    add_hover_effect(hrs_btn, "#20B2AA", "#3CB371")

    # Go Back button
    back_btn = tk.Button(main_frame, text="Go Back", font=button_font, width=15, height=2,
                         bg="#B22222", fg="black", activeforeground="red", relief="flat",
                         command=show_start_mainportal_frame)
    back_btn.place(x=600, y= 470)
    add_hover_effect(back_btn, "#B22222", "#CD5C5C")

    
def accounting_login():
    main_frame = Frame(root)
    main_frame.place(x=0, y=0, relwidth=1, relheight=1)
    image_path = "login.png"
    image = Image.open(image_path)
    image = image.resize((1400, 800), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    background_label = Label(main_frame, image=photo)
    background_label.image = photo  
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
   

    login_font = font.Font(family="Georgia", size=25)
    button_font = font.Font(family="Garamond", size=15)
    #login entry boxes
    username_entry = ttk.Entry(main_frame, font=login_font,width = 15)
    username_entry.place(x=550, y=225)

    password_entry = ttk.Entry(main_frame, font=login_font, width = 15)
    password_entry.place(x=550, y=351)

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if username == ACCOUNTING_CREDENTIALS["username"] and password == ACCOUNTING_CREDENTIALS["password"]:
            messagebox.showinfo("Login", "Login successful!")
            accounting()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    tk.Button(main_frame, text="Login", command=login, font=button_font, height=2, width=7).place(x=500, y=450)
    tk.Button(main_frame, text="Cancel", command=show_start_mainportal_frame, font=button_font, height=2, width=7).place(x=750, y=450)


def accounting():
    clear_main_frame()
    global main_frame
    main_frame = ttk.LabelFrame(root, text="Accounting Department", padding=20)
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    button_font = font.Font(family="Garamond", size=15)

    # --- Student list ---
    columns = ("Student ID", "Name", "Course", "Year Level", "Units", "Total Fee", "Balance", "Status")
    student_list = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)

    for col in columns:
        student_list.heading(col, text=col)

    student_list.column("Student ID", width=100, anchor=CENTER)
    student_list.column("Name", width=150, anchor=W)
    student_list.column("Course", width=100, anchor=CENTER)
    student_list.column("Year Level", width=80, anchor=CENTER)
    student_list.column("Units", width=60, anchor=CENTER)
    student_list.column("Total Fee", width=100, anchor=CENTER)
    student_list.column("Balance", width=100, anchor=CENTER)
    student_list.column("Status", width=100, anchor=CENTER)
    
    # populate the list
    for student_id, record in billing_records.items():
        stud_info = student_records.get(student_id, {})
        course = record.get("course", stud_info.get("course", ""))
        year_level = record.get("year_level", stud_info.get("year_level", ""))
        units = record.get("units", 0)
        
        # Calculate total fee
        total_fee = sum(record.get("charges", {}).values())
        
        # Determine payment status
        paid_amount = record.get("paid", 0)
        balance = max(0, total_fee - paid_amount)
        status = "Paid" if paid_amount >= total_fee else "Unpaid"
        
        student_list.insert("", "end", values=(
            student_id,
            record.get("name", ""),
            course,
            year_level,
            units,
            f"₱{total_fee:,.2f}",
            f"₱{balance:,.2f}",
            status
        ))

    student_list.pack(pady=10, fill="both", expand=True)
    
    
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(fill="x", pady=10)
    
    def view_receipt():
        selected = student_list.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a student first.")
            return

        values = student_list.item(selected, "values")
        if not values:
            messagebox.showwarning("No Selection", "Please select a valid student row.")
            return

        student_id = values[0]  # Student ID is the first column

        # Basic validation
        data = billing_records.get(student_id)
        if not data:
            messagebox.showerror("Error", f"No billing record found for Student ID: {student_id}")
            return

        # OPTIONAL: if you want to require payment to view a receipt, uncomment:
        if data.get("paid", 0) <= 0:
             messagebox.showerror("No Payment", "This student has not made any payments yet.")
             return

        # Call the global receipt viewer that uses billing_records
        show_receipt_frame(student_id)
    
               

   
    tk.Button(
        btn_frame,
        text="Go Back",
        command=admin_front_page,
        font=button_font,
        width=15
    ).pack(side="right", padx=10)
    
    tk.Button(
        btn_frame,
        text="View Receipt",
        command=view_receipt,
        font=button_font,
        width=15
    ).pack(side="left", padx=10)


def registrar_login():
    main_frame = Frame(root)
    main_frame.place(x=0, y=0, relwidth=1, relheight=1)
    image_path = "login.png"
    image = Image.open(image_path)
    image = image.resize((1400, 800), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    background_label = Label(main_frame, image=photo)
    background_label.image = photo  
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
   

    login_font = font.Font(family="Georgia", size=25)
    button_font = font.Font(family="Garamond", size=15)
    #login entry boxes
    username_entry = ttk.Entry(main_frame, font=login_font,width = 15)
    username_entry.place(x=550, y=225)

    password_entry = ttk.Entry(main_frame, show="*", font=login_font, width = 15)
    password_entry.place(x=550, y=351)

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if username == REGISTRAR_CREDENTIALS["username"] and password == REGISTRAR_CREDENTIALS["password"]:
            messagebox.showinfo("Login", "Login successful!")
            registrar_front_page()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    tk.Button(main_frame, text="Login", command=login, font=button_font, height=2, width=7).place(x=500, y=450)
    tk.Button(main_frame, text="Cancel", command=show_start_mainportal_frame, font=button_font, height=2, width=7).place(x=750, y=450)

def registrar_front_page():
    clear_main_frame()
    global main_frame
    main_frame = ttk.LabelFrame(root, text="Student List", padding=20)
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    button_font = font.Font(family="Garamond", size=15)

    # --- Student list ---
    columns = ("Student ID", "Name", "Address", "Course", "Year Level", "Units","Requirements", "Status")
    student_list = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)

    for col in columns:
        student_list.heading(col, text=col)

    student_list.column("Student ID", width=100, anchor=CENTER)
    student_list.column("Name", width=150, anchor=W)
    student_list.column("Address", width=200, anchor=W)
    student_list.column("Course", width=100, anchor=CENTER)
    student_list.column("Year Level", width=80, anchor=CENTER)
    student_list.column("Units", width=60, anchor=CENTER)
    student_list.column("Requirements", width=120, anchor=CENTER)
    student_list.column("Status", width=100, anchor=CENTER)
    
    # populate the list
    for student_id, record in billing_records.items():
        stud_info = student_records.get(student_id, {})
        address = record.get("address", stud_info.get("address", ""))
        course = record.get("course", stud_info.get("course", ""))
        year_level = record.get("year_level", stud_info.get("year_level", ""))
        units = record.get("units", 0)

        # determine status
        if stud_info.get("year_level") == "1st":
            status = "Freshman"
        elif stud_info.get("year_level") == "2nd":
            status = "Sophomore"
        elif stud_info.get("year_level") == "3rd":
            status = "Junior"
        elif stud_info.get("year_level") == "4th":
            status = "Senior"
        else:
            status = "Transferee"

        # requirements tracking
        req_status = stud_info.get("requirements_status", "Incomplete")

        
        student_list.insert("", "end", values=(
            student_id,
            record.get("name", ""),
            address,
            course,
            year_level,
            units,
            req_status,
            status
        ))

    student_list.pack(pady=10, fill="both", expand=True)

    def update_requirements():
        selected = student_list.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Select a student first.")
            return
        values = student_list.item(selected, "values")
        sid = values[0]
        student = student_records.get(sid, {})

        year_level = student.get("year_level", "")
        if year_level == "1st":
            reqs = REQUIREMENTS_FRESHMEN
        else:
            reqs = REQUIREMENTS_TRANSFEREE

        win = tk.Toplevel(root)
        win.title("Update Requirements")
        win.geometry("400x450")

        tk.Label(win, text=f"Requirements for {values[1]}", font=("Arial", 14, "bold")).pack(pady=10)

        checks = {}
        for req in reqs:
            var = tk.BooleanVar(value=student.get("requirements_data", {}).get(req, False))
            cb = tk.Checkbutton(win, text=req, variable=var, anchor="w")
            cb.pack(fill="x", padx=20, pady=4)
            checks[req] = var

        def save_reqs():
            req_status = {req: var.get() for req, var in checks.items()}
            student["requirements_data"] = req_status
            student["requirements_status"] = "Complete" if all(req_status.values()) else "Incomplete"
            registrar_front_page()  # refresh list
            win.destroy()

        tk.Button(win, text="Save", command=save_reqs, font=("Arial", 12), width=15).pack(pady=15)

    # --- nested enrollment form ---
    def enrollmentform():
        clear_main_frame()
        global main_frame
        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True)

        labelfont = font.Font(family="Georgia", size=30)
        contfont = font.Font(family="ubuntu", size=15)
        ttk.Label(main_frame, text="Student Enrollment Form", font=labelfont).pack(pady=20)

        main_frame1 = ttk.LabelFrame(main_frame, padding=20)
        main_frame1.pack(padx=20, pady=20)

        # sample form fields
        ttk.Label(main_frame1, text="Last Name", font=contfont).grid(row=0, column=0, padx=5, pady=3, sticky="w")
        entry_lname = ttk.Entry(main_frame1, font=contfont)
        entry_lname.grid(row=0, column=1, pady=3)

        ttk.Label(main_frame1, text="First Name", font=contfont).grid(row=1, column=0, padx=5, pady=3, sticky="w")
        entry_fname = ttk.Entry(main_frame1, font=contfont)
        entry_fname.grid(row=1, column=1, pady=3)

        ttk.Label(main_frame1, text="Middle Name", font=contfont).grid(row=2, column=0, sticky="w", padx=5, pady=3)
        entry_mname = ttk.Entry(main_frame1, font=contfont)
        entry_mname.grid(row=2, column=1, pady=3)

        ttk.Label(main_frame1, text="Age", font=contfont).grid(row=3, column=0, sticky="w", padx=5, pady=3)
        entry_age = ttk.Entry(main_frame1, font=contfont)
        entry_age.grid(row=3, column=1, pady=3)

        ttk.Label(main_frame1, text="Birthdate").grid(row=4, column=0, sticky="w", padx=5, pady=3)
        entry_birth = ttk.Entry(main_frame1, font=contfont)
        entry_birth.grid(row=4, column=1, pady=3)
        
        is_transferee_var = tk.BooleanVar(value=False)
        tk.Checkbutton(main_frame1, text="Transferee", variable=is_transferee_var, font=contfont)\
        .grid(row=6, column=1, pady=3)

        ttk.Label(main_frame1, text="----------- Address -----------", font=contfont).grid(row=0, column=4, sticky="w", padx=5, pady=3)
        ttk.Label(main_frame1, text="Block/House no.", font=contfont).grid(row=1, column=3, sticky="w", padx=5, pady=3)
        entry_block_address = ttk.Entry(main_frame1, font=contfont)
        entry_block_address.grid(row=1, column=4, pady=3)

        ttk.Label(main_frame1, text="Lot/Street/Room no.", font=contfont).grid(row=2, column=3, sticky="w", padx=5, pady=3)
        entry_lot_address = ttk.Entry(main_frame1, font=contfont)
        entry_lot_address.grid(row=2, column=4, pady=3)

        provinces_cities = {
            "Davao de Oro": ["Nabunturan", "Mabini", "Pantukan", "Maragusan", "New Bataan"],
            "Davao del Norte": ["Tagum", "Panabo", "Asuncion", "Braulio E. Dujali", "Kapalong"],
            "Davao del Sur": ["Davao City","Digos", "Bansalan", "Matanao", "Hagonoy", "Santa Cruz"],
            "Davao Occidental": ["Malita", "Don Marcelino", "Jose Abad Santos", "Sarangani", "Santa Maria"],
            "Davao Oriental": ["Mati", "Baganga", "Banaybanay", "Caraga", "Governor Generoso"]
        }
        
        ttk.Label(main_frame1, text="Provinces", font=contfont).grid(row=3, column=3, sticky="w", padx=5, pady=3)
        cb_Province = ttk.Combobox(main_frame1, font=contfont, values=list(provinces_cities.keys()), state="readonly")
        cb_Province.grid(row=3, column=4, pady=3)
        cb_Province.current(0)

        # city combo box
        ttk.Label(main_frame1, text="Cities", font=contfont).grid(row=4, column=3, sticky="w", padx=5, pady=3)
        cb_City = ttk.Combobox(main_frame1, font=contfont, state="readonly")
        cb_City.grid(row=4, column=4, pady=3)

        
        def update_city_combobox(event):
            selected_province = cb_Province.get()
            cities = provinces_cities.get(selected_province, [])
            cb_City['values'] = cities
            if cities:
                cb_City.current(0)  

        cb_Province.bind("<<ComboboxSelected>>", update_city_combobox)
        update_city_combobox(None)  

        ttk.Label(main_frame1, text="Course").grid(row=5, column=3, sticky="w", padx=5, pady=3)
        course_combo = ttk.Combobox(main_frame1, font=contfont, values=["BSIT", "BSBA", "BSHRM", "BSTM"], state="readonly")
        course_combo.grid(row=5, column=4, pady=3)
        course_combo.current(0)

        ttk.Label(main_frame1, text="Year", font=contfont).grid(row=6, column=3, sticky="w", padx=5, pady=3)
        year_var = tk.StringVar()
        tk.Radiobutton(main_frame1,  font=contfont, text="1st", variable=year_var, value="1st").grid(row=6, column=4, sticky="w", pady=3)
        tk.Radiobutton(main_frame1,  font=contfont,text="2nd", variable=year_var, value="2nd").grid(row=6, column=4, sticky="e", pady=3)
        tk.Radiobutton(main_frame1,  font=contfont, text="3rd", variable=year_var, value="3rd").grid(row=7, column=4, sticky="w", pady=3)
        tk.Radiobutton(main_frame1,  font=contfont, text="4th", variable=year_var, value="4th").grid(row=7, column=4, sticky="e", pady=3)

        ttk.Label(main_frame1, text="Gender", font=contfont).grid(row=5, column=0, sticky="w", padx=5, pady=3)
        gender_var = tk.StringVar()
        tk.Radiobutton(main_frame1, text="Male", font=contfont,  variable=gender_var, value="Male").grid(row=5, column=1, sticky="w", pady=3)
        tk.Radiobutton(main_frame1, text="Female", font=contfont,  variable=gender_var, value="Female").grid(row=5, column=1, sticky="e", pady=3)



        def submit_form():
            lname = entry_lname.get().strip()
            fname = entry_fname.get().strip()
            mname = entry_mname.get().strip()
            age = entry_age.get().strip()
            birthdate = entry_birth.get().strip()
            block_address = entry_block_address.get().strip()
            lot_address = entry_lot_address.get().strip()
            province = cb_Province.get()
            city = cb_City.get()
            course = course_combo.get()
            gender = gender_var.get()
            year_level = year_var.get()

            # units
            units_input = tk.simpledialog.askinteger("Units", "Enter number of units (1-50):", minvalue=1, maxvalue=50)
            if units_input is None:
                return  

            if not all([lname, fname, mname, age, birthdate, block_address, lot_address, province, city, course, gender, year_level]):
                messagebox.showwarning("Input Error", "Please fill in all fields.")
                return

            try:
                age_int = int(age)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid age.")
                return

            full_name = f"{lname.upper()}, {fname.upper()} {mname.upper()}"
            address = f"{block_address}, {lot_address}, {city}, {province}"
            student_id = generate_student_id()
            receipt_no = generate_receipt_number()
            trans_no = generate_transaction_number()

            # student info
            student_records[student_id] = {
                "last_name": lname,
                "first_name": fname,
                "middle_name": mname,
                "age": age_int,
                "birthdate": birthdate,
                "address": address,
                "province": province,
                "city": city,
                "course": course,
                "gender": gender,
                "year_level": year_level,
                "is_transferee": is_transferee_var.get(),  
                "requirements_status": "Incomplete",       
                "requirements_data": {}                    
            }

            # charges
            tuition_fee = 500 * units_input
            charges = {
                f"Tuition Fee (500 x {units_input})": tuition_fee,
                "Athletics Fee": 500.00,
                "Library Fee": 750.00,
                "Internet Fee": 300.00
            }

            # billing
            billing_records[student_id] = {
                "name": full_name,
                "receipt_no": receipt_no,
                "trans_no": trans_no,
                "units": units_input,
                "charges": charges,
                "paid": 0.0,
                "course": course,
                "year_level": year_level,
                "address": address
            }

            student_login[lname.lower()] = student_id

            messagebox.showinfo("Success", f"Student {full_name} enrolled with Student ID {student_id}.")
            registrar_front_page()  # go back to registrar page

        ttk.Button(main_frame1, text="Enroll", command=submit_form).grid(row=10, column=0, pady=10)
        ttk.Button(main_frame1, text="Go Back", command=registrar_front_page).grid(row=10, column=1, pady=10)

    # --- Button row ---
    btn_frame = tk.Frame(main_frame)
    btn_frame.pack(fill="x", pady=10)

    # Enroll Student button on the left
    tk.Button(
        btn_frame,
        text="Enroll Student",
        command=enrollmentform,
        font=button_font,
        width=15
    ).pack(side="left", padx=10)

    tk.Button(
    btn_frame,
    text="Update Requirements",
    command=update_requirements,
    font=button_font,
    width=18
    ).pack(side="left", padx=10)


    # spacer
    tk.Label(btn_frame, text="").pack(side="left", expand=True)

   
    tk.Button(
        btn_frame,
        text="Go Back",
        command=admin_front_page,
        font=button_font,
        width=15
    ).pack(side="right", padx=10)


def hrs_login():
    main_frame = Frame(root)
    main_frame.place(x=0, y=0, relwidth=1, relheight=1)
    image_path = "login.png"
    image = Image.open(image_path)
    image = image.resize((1400, 800), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    background_label = Label(main_frame, image=photo)
    background_label.image = photo  
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
   

    login_font = font.Font(family="Georgia", size=25)
    button_font = font.Font(family="Garamond", size=15)
    #login entry boxes
    username_entry = ttk.Entry(main_frame, font=login_font,width = 15)
    username_entry.place(x=550, y=225)

    password_entry = ttk.Entry(main_frame, show="*", font=login_font, width = 15)
    password_entry.place(x=550, y=351)

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if username == REGISTRAR_CREDENTIALS["username"] and password == REGISTRAR_CREDENTIALS["password"]:
            messagebox.showinfo("Login", "Login successful!")
            registrar_front_page()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    tk.Button(main_frame, text="Login", command=login, font=button_font, height=2, width=7).place(x=500, y=450)
    tk.Button(main_frame, text="Cancel", command=show_start_mainportal_frame, font=button_font, height=2, width=7).place(x=750, y=450)

    
#def human_resource_mainpage():
    
#def human_resource_panel():

#def grading():

#def professor_handler():

#def subject_assign():

#def daily_time_record():
    

def show_student_list():
    clear_main_frame()
    global main_frame
    main_frame = ttk.LabelFrame(root, text="Student List", padding=20)
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)
    button_font = font.Font(family="Garamond", size=15)

    columns = ("Student ID", "Name", "Address", "Course", "Year Level", "Units", "Payment Status")

    student_list = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)
    
    for col in columns:
        student_list.heading(col, text=col)

    student_list.column("Student ID", width=100, anchor=CENTER)
    student_list.column("Name", width=150, anchor=W)
    student_list.column("Address", width=200, anchor=W)
    student_list.column("Course", width=100, anchor=CENTER)
    student_list.column("Year Level", width=80, anchor=CENTER)
    student_list.column("Units", width=60, anchor=CENTER)
    student_list.column("Payment Status", width=100, anchor=CENTER)

    for student_id, record in billing_records.items():
        stud_info = student_records.get(student_id, {})
        address = record.get("address", stud_info.get("address", ""))
        course = record.get("course", stud_info.get("course", ""))
        year_level = record.get("year_level", stud_info.get("year_level", ""))
        units = record.get("units", 0)
        paid = record.get("paid", 0.0)
        total_charges = sum(record.get("charges", {}).values())
        payment_status = "Paid" if paid >= total_charges else "Unpaid"

        student_list.insert("", "end", values=(
            student_id,
            record.get("name", ""),
            address,
            course,
            year_level,
            units,
            payment_status
        ))

    student_list.pack(pady=10, fill="both", expand=True)
    tk.Button(main_frame, text="Go Back", command=admin_front_page, font=button_font).pack(pady=10)

def show_login_frame():
    clear_main_frame()
    global main_frame

    main_frame = Frame(root)
    main_frame.place(x=0, y=0, relwidth=1, relheight=1)
    image_path = "login.png"
    image = Image.open(image_path)
    image = image.resize((1400, 800), Image.LANCZOS)
    photo = ImageTk.PhotoImage(image)
    background_label = Label(main_frame, image=photo)
    background_label.image = photo  
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
   

    login_font = font.Font(family="Georgia", size=25)
    button_font = font.Font(family="Garamond", size=15)
    #login entry boxes
    username_entry = ttk.Entry(main_frame, font=login_font,width = 15)
    username_entry.place(x=550, y=225)

    password_entry = ttk.Entry(main_frame, show="*", font=login_font, width = 15)
    password_entry.place(x=550, y=351)

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if username == ADMIN_CREDENTIALS["username"] and password == ADMIN_CREDENTIALS["password"]:
            messagebox.showinfo("Login", "Login successful!")
            admin_front_page()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    tk.Button(main_frame, text="Login", command=login, font=button_font, height=2, width=7).place(x=500, y=450)
    tk.Button(main_frame, text="Cancel", command=show_start_mainportal_frame, font=button_font, height=2, width=7).place(x=750, y=450)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1400x800")
    root.title("Samsom Polytechnic Information Portal")
    show_start_mainportal_frame()
    root.mainloop()
