import tkinter as tk
from tkinter import messagebox

TABLE_SIZE = 10
EMPTY = None
DELETED = object()

class HashSetTable:
    def __init__(self):
        self.table = [EMPTY] * TABLE_SIZE
        self.count = 0
    def _hash(self, value):
        return value % TABLE_SIZE
    def search(self, value):
        index = self._hash(value)

        for _ in range(TABLE_SIZE):
            current = self.table[index]

            if current is EMPTY:
                return False
            if current is not DELETED and current == value:
                return True
            index = (index + 1) % TABLE_SIZE

        return False

    def add(self, value):
        if self.search(value):
            return False, "already exists"

        index = self._hash(value)
        first_deleted = None
        for _ in range(TABLE_SIZE):
            current = self.table[index]

            if current is DELETED and first_deleted is None:
                first_deleted = index
            elif current is EMPTY:
                target = first_deleted if first_deleted is not None else index
                self.table[target] = value
                self.count += 1
                return True, "successfully added"

            index = (index + 1) % TABLE_SIZE
        if first_deleted is not None:
            self.table[first_deleted] = value
            self.count += 1
            return True, "successfully added"

        return False, "hash table is full"

    def remove(self, value):
        index = self._hash(value)
        for _ in range(TABLE_SIZE):
            current = self.table[index]

            if current is EMPTY:
                return False
            if current is not DELETED and current == value:
                self.table[index] = DELETED
                self.count -= 1
                return True

            index = (index + 1) % TABLE_SIZE

        return False

    def values(self):
        return [
            value for value in self.table
            if value is not EMPTY and value is not DELETED
        ]

    def clear(self):
        self.table = [EMPTY] * TABLE_SIZE
        self.count = 0


class SetADTGUI:
    OPERATION_C_COLORS = {
        "default": "#F4F6FF",
        "union": "#57D9A3",        
        "intersection": "#6AB0FF", 
        "difference": "#F5B041",   
    }

    OPERATION_C_LABELS = {
        "default": "C",
        "union": "C (Union)",
        "intersection": "C (Intersection)",
        "difference": "C (A - B)",
    }

    ROW_HEIGHT = 28

    def __init__(self, root):
        self.root = root
        self.root.title("SET ADT OPERATIONS")
        self.root.geometry("900x680")
        self.root.minsize(820, 600)
        self.root.configure(bg="#171923")

        self.set_a = HashSetTable()
        self.set_b = HashSetTable()
        self.set_c = HashSetTable()
        self.c_color_mode = "union"  

        for number in (10, 20, 30, 40):
            self.set_a.add(number)

        for number in (30, 40, 50, 60):
            self.set_b.add(number)

        for number in self.set_a.values():
            self.set_c.add(number)
        for number in self.set_b.values():
            self.set_c.add(number)

        self.current_set = tk.StringVar(value="A")
        self.element_var = tk.StringVar()

        self.create_widgets()
        self.refresh_all()

    def make_button(self, parent, text, command, width=13):
        return tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            bg="#3b3b3b",
            fg="#F4F6FF",
            activebackground="#555555",
            activeforeground="#FFFFFF",
            relief="raised",
            bd=2,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="SET ADT OPERATIONS",
            bg="#171923",
            fg="#F4F6FF",
            font=("Arial", 21, "bold")
        )
        title.pack(pady=(15, 10))

        main = tk.Frame(self.root, bg="#171923", width=760)
        main.pack(fill="both", expand=True, padx=20, pady=5)
        main.pack_propagate(False)

        selector = tk.LabelFrame(
            main, text="Select Set to Modify",
            bg="#171923", fg="#F4F6FF",
            font=("Arial", 11, "bold"),
            padx=10, pady=5
        )
        selector.pack(fill="x", pady=5)

        tk.Radiobutton(
            selector, text="Set A", variable=self.current_set,
            value="A", bg="#171923", fg="#F4F6FF",
            selectcolor="#30364A", activebackground="#252B3B",
            activeforeground="#FFFFFF", font=("Arial", 11)
        ).pack(side="left", padx=12)

        tk.Radiobutton(
            selector, text="Set B", variable=self.current_set,
            value="B", bg="#171923", fg="#F4F6FF",
            selectcolor="#30364A", activebackground="#252B3B",
            activeforeground="#FFFFFF", font=("Arial", 11)
        ).pack(side="left", padx=12)

        entry_frame = tk.LabelFrame(
            main, text="Element",
            bg="#171923", fg="#F4F6FF",
            font=("Arial", 11, "bold"),
            padx=10, pady=6
        )
        entry_frame.pack(fill="x", pady=5)

        tk.Label(
            entry_frame, text="Enter integer:",
            bg="#171923", fg="#F4F6FF", font=("Arial", 11)
        ).pack(side="left", padx=(5, 10))

        self.element_entry = tk.Entry(
            entry_frame, textvariable=self.element_var,
            width=20, font=("Arial", 12)
        )
        self.element_entry.pack(side="left", padx=5)
        self.element_entry.bind("<Return>", lambda event: self.add_element())

        # Basic operations
        basic_frame = tk.LabelFrame(
            main, text="Basic Set Operations",
            bg="#171923", fg="#F4F6FF",
            font=("Arial", 11, "bold"),
            padx=10, pady=6
        )
        basic_frame.pack(fill="x", pady=5)

        button_colors = {
            "Add": "#287A62",
            "Delete": "#A84B55",
            "Search": "#356FA8",
            "Display": "#6656A5"
        }

        for label, command in (
            ("Add", self.add_element),
            ("Delete", self.delete_element),
            ("Search", self.search_element),
            ("Display", self.display_sets)
        ):
            button = self.make_button(basic_frame, label, command)
            button.pack(side="left", padx=6, pady=3)
            button.configure(
                bg=button_colors[label],
                activebackground=button_colors[label]
            )

        # Set operations
        set_ops = tk.LabelFrame(
            main, text="Set Operations",
            bg="#171923", fg="#F4F6FF",
            font=("Arial", 11, "bold"),
            padx=10, pady=6
        )
        set_ops.pack(fill="x", pady=5)

        set_op_colors = {
            "Union": "#287A62",
            "Intersection": "#356FA8",
            "Difference (A - B)": "#A87935"
        }

        for label, command in (
            ("Union", self.union_sets),
            ("Intersection", self.intersection_sets),
            ("Difference (A - B)", self.difference_sets)
        ):
            button = self.make_button(set_ops, label, command, width=18)
            button.pack(side="left", padx=6, pady=3)
            button.configure(
                bg=set_op_colors[label],
                activebackground=set_op_colors[label]
            )
        table_frame = tk.LabelFrame(
            main, text="Hash Table Visualization (Linear Probing)",
            bg="#171923", fg="#F4F6FF",
            font=("Arial", 11, "bold"),
            padx=8, pady=5
        )
        table_frame.pack(fill="both", expand=True, pady=7)

        self.header_frame = tk.Frame(table_frame, bg="#444444", height=30)
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)

        self.header_labels = {}
        col_weights = [("index", 1), ("A", 3), ("B", 3), ("C", 3)]
        for idx, (col, weight) in enumerate(col_weights):
            self.header_frame.columnconfigure(idx, weight=weight, uniform="cols")
            lbl = tk.Label(
                self.header_frame,
                text="Index" if col == "index" else col,
                bg="#444444",
                fg="#F4F6FF",
                font=("Arial", 11, "bold")
            )
            lbl.grid(row=0, column=idx, sticky="nsew")
            self.header_labels[col] = lbl

        body_container = tk.Frame(table_frame, bg="#292929")
        body_container.pack(fill="both", expand=True)

        self.table_canvas = tk.Canvas(
            body_container,
            bg="#292929",
            highlightthickness=0,
            height=190
        )
        scrollbar = tk.Scrollbar(
            body_container, orient="vertical", command=self.table_canvas.yview
        )
        self.table_canvas.configure(yscrollcommand=scrollbar.set)

        self.table_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.rows_frame = tk.Frame(self.table_canvas, bg="#292929")
        self.canvas_window = self.table_canvas.create_window(
            (0, 0), window=self.rows_frame, anchor="nw"
        )

        self.rows_frame.bind("<Configure>", self._on_rows_configure)
        self.table_canvas.bind("<Configure>", self._on_canvas_configure)
        self.table_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.table_canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.table_canvas.bind_all("<Button-5>", self._on_mousewheel)

        bottom = tk.Frame(main, bg="#171923")
        bottom.pack(fill="x", pady=(8, 12))

        self.make_button(
            bottom, "Exit", self.root.destroy, width=12
        ).pack(side="right", padx=5)

    def _on_rows_configure(self, event):
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.table_canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        if event.num == 4:
            self.table_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.table_canvas.yview_scroll(1, "units")
        else:
            self.table_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def selected_table(self):
        return self.set_a if self.current_set.get() == "A" else self.set_b

    def selected_name(self):
        return self.current_set.get()

    def get_integer(self):
        raw_value = self.element_var.get().strip()

        if not raw_value:
            messagebox.showwarning("Missing Input", "Please enter an integer.")
            self.element_entry.focus_set()
            return None

        try:
            return int(raw_value)
        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Please enter a valid whole number."
            )
            self.element_entry.focus_set()
            return None

    def add_element(self):
        value = self.get_integer()
        if value is None:
            return

        name = self.selected_name()
        success, message = self.selected_table().add(value)
        if not success:
            messagebox.showinfo("Add Element", f"{value} {message} in Set {name}.")
        self.refresh_all()
        self.element_var.set("")

    def delete_element(self):
        value = self.get_integer()
        if value is None:
            return

        name = self.selected_name()
        success = self.selected_table().remove(value)
        if not success:
            messagebox.showinfo("Delete Element", f"{value} not found in Set {name}.")
        self.refresh_all()
        self.element_var.set("")

    def search_element(self):
        value = self.get_integer()
        if value is None:
            return

        name = self.selected_name()
        found = self.selected_table().search(value)
        status = (
            f"{value} IS in Set {name}."
            if found
            else f"{value} is NOT in Set {name}."
        )
        messagebox.showinfo("Search Result", status)
        self.element_var.set("")

    def display_sets(self):
        msg = (
            f"A: {self.format_set(self.set_a)}\n"
            f"B: {self.format_set(self.set_b)}\n"
            f"C: {self.format_set(self.set_c)}"
        )
        messagebox.showinfo("Set Contents", msg)
        self.refresh_all()

    def union_sets(self):
        result = HashSetTable()
        for value in self.set_a.values():
            result.add(value)
        for value in self.set_b.values():
            result.add(value)

        self.set_c = result
        self.c_color_mode = "union"
        self.refresh_all()

    def intersection_sets(self):
        result = HashSetTable()
        for value in self.set_a.values():
            if self.set_b.search(value):
                result.add(value)

        self.set_c = result
        self.c_color_mode = "intersection"
        self.refresh_all()

    def difference_sets(self):
        result = HashSetTable()
        for value in self.set_a.values():
            if not self.set_b.search(value):
                result.add(value)

        self.set_c = result
        self.c_color_mode = "difference"
        self.refresh_all()

    @staticmethod
    def format_set(hash_set):
        values = hash_set.values()
        return "{ " + ", ".join(str(value) for value in values) + " }"

    @staticmethod
    def cell_value(value):
        if value is EMPTY or value is DELETED:
            return "EMPTY"
        return str(value)

    def refresh_all(self):
        for child in self.rows_frame.winfo_children():
            child.destroy()

        c_color = self.OPERATION_C_COLORS.get(self.c_color_mode, "#F4F6FF")
        c_label = self.OPERATION_C_LABELS.get(self.c_color_mode, "C")

        self.header_labels["C"].config(text=c_label, fg=c_color)
        self.header_labels["index"].config(fg="#F4F6FF")
        self.header_labels["A"].config(fg="#F4F6FF")
        self.header_labels["B"].config(fg="#F4F6FF")

        col_weights = [("index", 1), ("A", 3), ("B", 3), ("C", 3)]
        for idx, (_, weight) in enumerate(col_weights):
            self.rows_frame.columnconfigure(idx, weight=weight, uniform="cols")

        for index in range(TABLE_SIZE):
            row_bg = "#252B3B" if index % 2 == 0 else "#202638"
            values = [
                str(index),
                self.cell_value(self.set_a.table[index]),
                self.cell_value(self.set_b.table[index]),
                self.cell_value(self.set_c.table[index]),
            ]

            for col_idx, text_val in enumerate(values):
                fg_color = c_color if col_idx == 3 else "#F4F6FF"
                cell = tk.Label(
                    self.rows_frame,
                    text=text_val,
                    bg=row_bg,
                    fg=fg_color,
                    font=("Arial", 11),
                    height=1,
                    pady=4
                )
                cell.grid(row=index, column=col_idx, sticky="nsew")


if __name__ == "__main__":
    root = tk.Tk()
    app = SetADTGUI(root)
    root.mainloop()