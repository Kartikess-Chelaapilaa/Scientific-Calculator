import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLineEdit, QPushButton, QGridLayout,
    QVBoxLayout, QLabel, QMenuBar, QMenu, QMessageBox, QHBoxLayout, QTextEdit,
    QSplitter, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction

class ScientificCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scientific Calculator - PyQt6")
        # start in scientific size but allow resizing
        self.resize(960, 568)
        self.setMinimumSize(420, 400)
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

        # Main layout contains a horizontal splitter
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(8, 8, 8, 8)
        self.central_widget.setLayout(main_layout)

        # Splitter: left = calculator area, right = history
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self.splitter)

        # ---------------- Left widget: Calculator ----------------
        self.left_widget = QWidget()
        self.left_panel = QVBoxLayout(self.left_widget)
        self.left_panel.setSpacing(8)
        self.left_panel.setContentsMargins(0, 0, 0, 0)
        self.splitter.addWidget(self.left_widget)

        # Display
        self.display = QLineEdit("0")
        self.display.setFont(QFont("Helvetica", 24))
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet(
            "background-color: black; color: white; padding: 10px; border-radius: 5px;"
        )
        self.left_panel.addWidget(self.display)

        # Title
        self.lbl_title = QLabel("Scientific Calculator")
        self.lbl_title.setFont(QFont("Helvetica", 28, QFont.Weight.Bold))
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.left_panel.addWidget(self.lbl_title)

        # Grid layout for buttons
        self.button_layout = QGridLayout()
        self.button_layout.setHorizontalSpacing(6)
        self.button_layout.setVerticalSpacing(6)
        self.left_panel.addLayout(self.button_layout)

        # ---------------- Right widget: History ----------------
        self.history_panel = QTextEdit()
        self.history_panel.setReadOnly(True)
        self.history_panel.setStyleSheet(
            "background-color: #1E1E1E; color: #AAAAAA; padding: 10px; border-radius: 5px;"
        )
        # give it flexible sizing instead of fixed
        self.history_panel.setMinimumWidth(200)
        self.history_panel.setMaximumWidth(400)
        self.history_panel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.splitter.addWidget(self.history_panel)

        # Initial splitter sizes: left bigger than history
        self.splitter.setSizes([700, 260])

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

        # make '0' span two columns so layout looks nicer
        zero_button = self.button_layout.itemAtPosition(5, 0)
        if zero_button is not None:
            btn_widget = zero_button.widget()
            if btn_widget:
                self.button_layout.addWidget(btn_widget, 5, 0, 1, 2)

    def add_button(self, text, row, col, func):
        btn = QPushButton(text)
        btn.setFixedSize(80, 60)
        btn.setFont(QFont("Helvetica", 16))
        btn.setStyleSheet(
            "QPushButton { background-color: #1E1E1E; color: white; border-radius: 5px; }"
            "QPushButton:hover { background-color: #333333; }"
        )
        # keep your functions compatible with receiving a parameter
        btn.clicked.connect(lambda _, x=text: func(x))
        self.button_layout.addWidget(btn, row, col)
        return btn  # return the button object

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
        # keep behaviour same as your code (no logic changes)
        try:
            self.current = float(self.current)
        except Exception:
            # if conversion fails, try display text
            try:
                self.current = float(self.display.text())
            except Exception:
                self.current = 0.0
        if self.check_sum:
            self.valid_function()
        else:
            try:
                self.total = float(self.display.text())
            except Exception:
                self.total = 0.0

    def update_display(self, value):
        self.display.setText(str(value))

    def valid_function(self):
        # use previous value to build expression for history
        prev = self.total
        cur = self.current
        expression = ""
        try:
            if self.op == "add":
                self.total = prev + cur
                expression = f"{prev} + {cur} = {self.total}"
            elif self.op == "sub":
                self.total = prev - cur
                expression = f"{prev} - {cur} = {self.total}"
            elif self.op == "multi":
                self.total = prev * cur
                expression = f"{prev} x {cur} = {self.total}"
            elif self.op == "divide":
                self.total = prev / cur
                expression = f"{prev} ÷ {cur} = {self.total}"
            elif self.op == "mod":
                self.total = prev % cur
                expression = f"{prev} mod {cur} = {self.total}"
        except ZeroDivisionError:
            expression = "Error: Division by zero"
            self.handle_error("Divide by 0")
            return
        except Exception:
            expression = "Error"
            self.handle_error()
            return

        # Update history
        self.history.append(expression)
        if len(self.history) > 5:
            self.history.pop(0)
        self.history_panel.setText("\n".join(self.history))
        self.history_panel.verticalScrollBar().setValue(self.history_panel.verticalScrollBar().maximum())

        self.input_value = True
        self.check_sum = False
        self.update_display(self.total)

    def operation(self, op):
        try:
            self.current = float(self.current)
        except Exception:
            try:
                self.current = float(self.display.text())
            except Exception:
                self.current = 0.0
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
        try:
            self.current = -float(self.display.text())
        except Exception:
            self.current = 0.0
        self.update_display(self.current)

    def squared(self, _=None):
        self.result = False
        try:
            self.current = math.sqrt(float(self.display.text()))
        except Exception:
            self.handle_error()
            return
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
        try:
            self.current = math.sin(math.radians(float(self.display.text())))
        except Exception:
            self.handle_error()
            return
        self.update_display(self.current)

    def cos(self, _=None):
        self.result = False
        try:
            self.current = math.cos(math.radians(float(self.display.text())))
        except Exception:
            self.handle_error()
            return
        self.update_display(self.current)

    def tan(self, _=None):
        self.result = False
        try:
            self.current = math.tan(math.radians(float(self.display.text())))
        except Exception:
            self.handle_error()
            return
        self.update_display(self.current)

    def sinh(self, _=None):
        self.result = False
        try:
            # keep original behaviour (you may want to remove radians here later)
            self.current = math.sinh(math.radians(float(self.display.text())))
        except Exception:
            self.handle_error()
            return
        self.update_display(self.current)

    def cosh(self, _=None):
        self.result = False
        try:
            self.current = math.cosh(math.radians(float(self.display.text())))
        except Exception:
            self.handle_error()
            return
        self.update_display(self.current)

    def tanh(self, _=None):
        self.result = False
        try:
            self.current = math.tanh(math.radians(float(self.display.text())))
        except Exception:
            self.handle_error()
            return
        self.update_display(self.current)

    def log(self, _=None):
        self.result = False
        try:
            self.current = math.log(float(self.display.text()))
        except Exception:
            self.handle_error()
            return
        self.update_display(self.current)

    def exp(self, _=None):
        self.result = False
        try:
            self.current = math.exp(float(self.display.text()))
        except Exception:
            self.handle_error()
            return
        self.update_display(self.current)

    def log10(self, _=None):
        self.result = False
        try:
            self.current = math.log10(float(self.display.text()))
        except Exception:
            self.handle_error()
            return
        self.update_display(self.current)

    def log1p(self, _=None):
        self.result = False
        try:
            self.current = math.log1p(float(self.display.text()))
        except Exception:
            self.handle_error()
            return
        self.update_display(self.current)

    def expm1(self, _=None):
        self.result = False
        try:
            self.current = math.expm1(float(self.display.text()))
        except Exception:
            self.handle_error()
            return
        self.update_display(self.current)

    def lgamma(self, _=None):
        self.result = False
        try:
            self.current = math.lgamma(float(self.display.text()))
        except Exception:
            self.handle_error()
            return
        self.update_display(self.current)

    def log2(self, _=None):
        self.result = False
        try:
            self.current = math.log2(float(self.display.text()))
        except Exception:
            self.handle_error()
            return
        self.update_display(self.current)

    def degrees(self, _=None):
        self.result = False
        try:
            self.current = math.degrees(float(self.display.text()))
        except Exception:
            self.handle_error()
            return
        self.update_display(self.current)

    def acosh(self, _=None):
        self.result = False
        try:
            self.current = math.acosh(float(self.display.text()))
        except Exception:
            self.handle_error()
            return
        self.update_display(self.current)

    def asinh(self, _=None):
        self.result = False
        try:
            self.current = math.asinh(float(self.display.text()))
        except Exception:
            self.handle_error()
            return
        self.update_display(self.current)

    def handle_error(self, msg="Error"):
        # show a friendly message and reset entry state
        self.update_display(msg)
        self.current = ""
        self.input_value = True
        self.check_sum = False
        self.result = False

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
        standard_action.triggered.connect(lambda: self.switch_mode(standard=True))
        scientific_action = QAction("Scientific", self)
        scientific_action.triggered.connect(lambda: self.switch_mode(standard=False))
        view_menu.addAction(standard_action)
        view_menu.addAction(scientific_action)

    def switch_mode(self, standard: bool):
        """Toggle between standard and scientific modes and adjust history visibility"""
        if standard:
            # hide scientific buttons and history (history can be distracting in small width)
            self.show_scientific(False)
            self.history_panel.hide()
            # resize to a reasonable standard calculator size
            self.resize(480, 568)
        else:
            # show scientific buttons and history
            self.show_scientific(True)
            self.history_panel.show()
            # restore to scientific size
            self.resize(960, 568)
            # reset splitter sizes so history gets space again
            self.splitter.setSizes([700, 260])

    def resize_calculator(self, width, height):
        # keep compatibility if other code calls this
        self.resize(width, height)
        # if width is small, hide history else show it
        if width < 600:
            self.history_panel.hide()
        else:
            self.history_panel.show()

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
