import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLineEdit, QPushButton, QGridLayout,
    QVBoxLayout, QLabel, QMenuBar, QMenu, QMessageBox, QHBoxLayout, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction

class ScientificCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scientific Calculator - PyQt6")
        self.setFixedSize(960, 568)
        self.setStyleSheet("background-color: #121212; color: white;")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.scientific_buttons = []
        self.history = []

        self.total = 0
        self.current = ''
        self.input_value = True
        self.check_sum = False
        self.op = ''
        self.result = False

        self.init_ui()
        self.create_menu()

    def init_ui(self):
        """Setup display, buttons, and layout"""

        # Main horizontal layout: left (calculator) + right (history)
        self.main_layout = QHBoxLayout()
        self.central_widget.setLayout(self.main_layout)

        # ---------------- Left panel: Calculator ----------------
        self.left_panel = QVBoxLayout()
        self.main_layout.addLayout(self.left_panel)  # add left panel to main layout

        # Display
        self.display = QLineEdit("0")
        self.display.setFont(QFont("Helvetica", 24))
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet(
            "background-color: black; color: white; padding: 10px; border-radius: 5px;"
        )
        self.left_panel.addWidget(self.display)  # <-- add to left panel

        # Title
        self.lbl_title = QLabel("Scientific Calculator")
        self.lbl_title.setFont(QFont("Helvetica", 28, QFont.Weight.Bold))
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_panel.addWidget(self.lbl_title)  # <-- add to left panel

        # Grid layout for buttons
        self.button_layout = QGridLayout()
        self.left_panel.addLayout(self.button_layout)  # <-- add to left panel

        # ---------------- Right panel: History ----------------
        self.history_panel = QTextEdit()
        self.history_panel.setReadOnly(True)
        self.history_panel.setStyleSheet(
            "background-color: #1E1E1E; color: #AAAAAA; padding: 10px; border-radius: 5px;"
        )
        self.history_panel.setFixedWidth(250)
        self.main_layout.addWidget(self.history_panel)  # <-- stays in main layout

        # Number buttons
        self.numbers = [
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2),
            ("0", 5, 0)
        ]

        for text, row, col in self.numbers:
            self.add_button(text, row, col, self.number_enter)

        # Operation buttons
        operations = [
            ("+", 1, 3, "add"), ("-", 2, 3, "sub"), 
            ("x", 3, 3, "multi"), ("/", 4, 3, "divide")
        ]

        for text, row, col, op in operations:
            self.add_button(text, row, col, lambda _, x=op: self.operation(x))

        # Special buttons
        specials = [
            ("C", 1, 0, self.clear_entry),
            ("CE", 1, 1, self.all_clear),
            ("=", 5, 3, self.sum_of_total),
            (".", 5, 1, lambda _: self.number_enter(".")),
            ("±", 5, 2, self.plus_minus),
            ("\u221A", 1, 2, self.squared),
        ]

        for text, row, col, func in specials:
            self.add_button(text, row, col, func)

        # Scientific buttons row 1
        sci_row1 = [
            ("pi", 1, 4, self.pi), ("Cos", 1, 5, self.cos),
            ("tan", 1, 6, self.tan), ("sin", 1, 7, self.sin)
        ]
        for text, row, col, func in sci_row1:
            btn = self.add_button(text, row, col, func)
            self.scientific_buttons.append(btn)

        # Scientific buttons row 2
        sci_row2 = [
            ("2pi", 2, 4, self.tau), ("Cosh", 2, 5, self.cosh),
            ("Tanh", 2, 6, self.tanh), ("Sinh", 2, 7, self.sinh)
        ]
        for text, row, col, func in sci_row2:
            btn = self.add_button(text, row, col, func)
            self.scientific_buttons.append(btn)

        # Scientific buttons row 3
        sci_row3 = [
            ("log", 3, 4, self.log),
            ("exp", 3, 5, self.exp),
            ("e", 3, 7, self.e),
            ("Mod", 3, 6, lambda _: self.operation("mod"))
        ]
        for text, row, col, func in sci_row3:
            btn = self.add_button(text, row, col, func)
            self.scientific_buttons.append(btn)

        # More scientific buttons
        sci_row4 = [
            ("log10", 4, 4, self.log10),
            ("log1p", 4, 5, self.log1p),
            ("expm1", 4, 6, self.expm1),
            ("gamma", 4, 7, self.lgamma)
        ]
        for text, row, col, func in sci_row4:
            btn = self.add_button(text, row, col, func)
            self.scientific_buttons.append(btn)

        sci_row5 = [
            ("log2", 5, 4, self.log2),
            ("deg", 5, 5, self.degrees),
            ("acosh", 5, 6, self.acosh),
            ("asinh", 5, 7, self.asinh)
        ]
        for text, row, col, func in sci_row5:
            btn = self.add_button(text, row, col, func)
            self.scientific_buttons.append(btn)

    def add_button(self, text, row, col, func):
        btn = QPushButton(text)
        btn.setFixedSize(80, 60)
        btn.setFont(QFont("Helvetica", 16))
        btn.setStyleSheet(
            "QPushButton { background-color: #1E1E1E; color: white; border-radius: 5px; }"
            "QPushButton:hover { background-color: #333333; }"
        )
        btn.clicked.connect(lambda _, x=text: func(x))
        self.button_layout.addWidget(btn, row, col)
        return btn  # <-- return the button object
    
    def show_scientific(self, show: bool):
        for btn in self.scientific_buttons:
            btn.setVisible(show)

    # ---------------- Calculator Logic ----------------
    def number_enter(self, num):
        self.result = False
        firstnum = self.display.text()
        secondnum = str(num)
        if self.input_value:
            self.current = secondnum
            self.input_value = False
        else:
            if secondnum == "." and "." in firstnum:
                return
            self.current = firstnum + secondnum
        self.update_display(self.current)

    def sum_of_total(self, _=None):
        self.result = True
        self.current = float(self.current)
        if self.check_sum:
            self.valid_function()
        else:
            self.total = float(self.display.text())

    def update_display(self, value):
        self.display.setText(str(value))

    def valid_function(self):
        if self.op == "add":
            self.total += self.current
            expression = f"{self.total - self.current} + {self.current} = {self.total}"
        elif self.op == "sub":
            self.total -= self.current
            expression = f"{self.total + self.current} - {self.current} = {self.total}"
        elif self.op == "multi":
            self.total *= self.current
            expression = f"{self.total / self.current} x {self.current} = {self.total}"
        elif self.op == "divide":
            self.total /= self.current
            expression = f"{self.total * self.current} ÷ {self.current} = {self.total}"
        elif self.op == "mod":
            self.total %= self.current
            expression = f"{self.total + self.current * (self.total // self.current)} mod {self.current} = {self.total}"

        # Update history
        self.history.append(expression)
        if len(self.history) > 5:  # Keep only last 5
            self.history.pop(0)
        self.history_panel.setText("\n".join(self.history))
        self.history_panel.verticalScrollBar().setValue(self.history_panel.verticalScrollBar().maximum())

        self.input_value = True
        self.check_sum = False
        self.update_display(self.total)

    def operation(self, op):
        self.current = float(self.current)
        if self.check_sum:
            self.valid_function()
        elif not self.result:
            self.total = self.current
            self.input_value = True
        self.check_sum = True
        self.op = op
        self.result = False

    def clear_entry(self, _=None):
        self.result = False
        self.current = "0"
        self.update_display(0)
        self.input_value = True

    def all_clear(self, _=None):
        self.clear_entry()
        self.total = 0

    def plus_minus(self, _=None):
        self.result = False
        self.current = -float(self.display.text())
        self.update_display(self.current)

    def squared(self, _=None):
        self.result = False
        self.current = math.sqrt(float(self.display.text()))
        self.update_display(self.current)

    # ---------------- Scientific Functions ----------------
    def pi(self, _=None):
        self.result = False
        self.current = math.pi
        self.update_display(self.current)

    def tau(self, _=None):
        self.result = False
        self.current = math.tau
        self.update_display(self.current)

    def e(self, _=None):
        self.result = False
        self.current = math.e
        self.update_display(self.current)

    def sin(self, _=None):
        self.result = False
        self.current = math.sin(math.radians(float(self.display.text())))
        self.update_display(self.current)

    def cos(self, _=None):
        self.result = False
        self.current = math.cos(math.radians(float(self.display.text())))
        self.update_display(self.current)

    def tan(self, _=None):
        self.result = False
        self.current = math.tan(math.radians(float(self.display.text())))
        self.update_display(self.current)

    def sinh(self, _=None):
        self.result = False
        self.current = math.sinh(math.radians(float(self.display.text())))
        self.update_display(self.current)

    def cosh(self, _=None):
        self.result = False
        self.current = math.cosh(math.radians(float(self.display.text())))
        self.update_display(self.current)

    def tanh(self, _=None):
        self.result = False
        self.current = math.tanh(math.radians(float(self.display.text())))
        self.update_display(self.current)

    def log(self, _=None):
        self.result = False
        self.current = math.log(float(self.display.text()))
        self.update_display(self.current)

    def exp(self, _=None):
        self.result = False
        self.current = math.exp(float(self.display.text()))
        self.update_display(self.current)

    def log10(self, _=None):
        self.result = False
        self.current = math.log10(float(self.display.text()))
        self.update_display(self.current)

    def log1p(self, _=None):
        self.result = False
        self.current = math.log1p(float(self.display.text()))
        self.update_display(self.current)

    def expm1(self, _=None):
        self.result = False
        self.current = math.expm1(float(self.display.text()))
        self.update_display(self.current)

    def lgamma(self, _=None):
        self.result = False
        self.current = math.lgamma(float(self.display.text()))
        self.update_display(self.current)

    def log2(self, _=None):
        self.result = False
        self.current = math.log2(float(self.display.text()))
        self.update_display(self.current)

    def degrees(self, _=None):
        self.result = False
        self.current = math.degrees(float(self.display.text()))
        self.update_display(self.current)

    def acosh(self, _=None):
        self.result = False
        self.current = math.acosh(float(self.display.text()))
        self.update_display(self.current)

    def asinh(self, _=None):
        self.result = False
        self.current = math.asinh(float(self.display.text()))
        self.update_display(self.current)

    # ---------------- Menu ----------------
    def create_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        view_menu = menubar.addMenu("View")
        help_menu = menubar.addMenu("Help")

        # File menu actions
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_app)
        file_menu.addAction(exit_action)

        # View menu actions
        standard_action = QAction("Standard", self)
        standard_action.triggered.connect(lambda: [self.resize_calculator(480, 568), self.show_scientific(False)])
        scientific_action = QAction("Scientific", self)
        scientific_action.triggered.connect(lambda: [self.resize_calculator(960, 568), self.show_scientific(True)])
        view_menu.addAction(standard_action)
        view_menu.addAction(scientific_action)

    def resize_calculator(self, width, height):
        self.setFixedSize(width, height)

    def exit_app(self):
        reply = QMessageBox.question(
            self, "Exit", "Do you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScientificCalculator()
    window.show()
    sys.exit(app.exec())
