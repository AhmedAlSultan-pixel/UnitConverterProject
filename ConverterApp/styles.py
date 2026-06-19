
APP_STYLE = """
/* =========================
   Main Window
   ========================= */

QWidget {
    background-color: #f5f6fa;
    font-family: "Segoe UI", "Arial";
    font-size: 10pt;
    color: #2f3640;
}


/* =========================
   Labels
   ========================= */

QLabel {
    background: transparent;
}

QLabel#titleLabel {
    font-size: 20pt;
    font-weight: 600;
    color: #2f3640;
}

QLabel#categoryLabel {
    font-size: 11pt;
    font-weight: 600;
    color: #4b6584;
}

QLabel#resultLabel {
    font-size: 18pt;
    font-weight: 600;
    color: #192a56;
    padding: 12px;
}


/* =========================
   Card Container
   ========================= */

QFrame#card {
    background-color: white;
    border: 1px solid #dcdde1;
    border-radius: 16px;
}


/* =========================
   Input Controls
   ========================= */

QLineEdit,
QComboBox {
    background-color: white;
    border: 1px solid #c8d6e5;
    border-radius: 10px;

    padding-left: 12px;
    padding-right: 12px;

    min-height: 40px;

    selection-background-color: #4a69bd;
}

QLineEdit:focus,
QComboBox:focus {
    border: 2px solid #4a69bd;
}


/* =========================
   Combo Box Dropdown
   ========================= */

QComboBox::drop-down {
    border: none;
    width: 30px;
}

QComboBox QAbstractItemView {
    background: white;
    border: 1px solid #dcdde1;
    outline: none;
    padding: 4px;
}


/* =========================
   Buttons
   ========================= */

QPushButton {
    background-color: white;
    border: 1px solid #c8d6e5;
    border-radius: 10px;

    min-height: 40px;

    padding-left: 12px;
    padding-right: 12px;
}

QPushButton:hover {
    background-color: #eef2ff;
}

QPushButton:pressed {
    background-color: #dfe6ff;
}


/* =========================
   Swap Button
   ========================= */

QPushButton#swapButton {
    border-radius: 20px;

    min-width: 40px;
    max-width: 40px;

    min-height: 40px;
    max-height: 40px;

    font-size: 16pt;
    font-weight: bold;
}

QPushButton#swapButton:hover {
    background-color: #e8f0fe;
}

QPushButton#swapButton:pressed {
    background-color: #d6e4ff;
}
"""