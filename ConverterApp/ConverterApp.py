import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QCompleter
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt


# =========================
# Conversion Data
# =========================

TEMPERATURE_UNITS = ["Celsius", "Fahrenheit", "Kelvin"]

CONVERSION_FACTORS = {
    "Length": {
        "Millimeter": 0.001,
        "Centimeter": 0.01,
        "Meter": 1,
        "Kilometer": 1000,
        "Inch": 0.0254,
        "Foot": 0.3048,
        "Yard": 0.9144,
        "Mile": 1609.344
    },

    "Weight": {
        "Milligram": 0.001,
        "Gram": 1,
        "Kilogram": 1000,
        "Ounce": 28.349523125,
        "Pound": 453.59237,
        "Ton": 1_000_000
    },

    "Volume": {
        "Milliliter": 0.001,
        "Liter": 1,
        "Cup": 0.236588,
        "Pint": 0.473176,
        "Quart": 0.946353,
        "Gallon": 3.78541
    },

    "Time": {
        "Millisecond": 0.001,
        "Second": 1,
        "Minute": 60,
        "Hour": 3600,
        "Day": 86400,
        "Week": 604800
    },

    "Area": {
        "Square Millimeter": 0.000001,
        "Square Centimeter": 0.0001,
        "Square Meter": 1,
        "Square Kilometer": 1_000_000,
        "Square Foot": 0.092903,
        "Square Yard": 0.836127,
        "Acre": 4046.8564224,
        "Hectare": 10000
    },

    "Speed": {
        "Meters/Second": 1,
        "Kilometers/Hour": 0.277777778,
        "Miles/Hour": 0.44704,
        "Knot": 0.514444
    },

    "Data Storage": {
        "Byte": 1,
        "Kilobyte": 1024,
        "Megabyte": 1024**2,
        "Gigabyte": 1024**3,
        "Terabyte": 1024**4
    }
}


UNITS = {
    "Temperature": TEMPERATURE_UNITS
}

for category, factors in CONVERSION_FACTORS.items():
    UNITS[category] = list(factors.keys())


UNIT_TO_CATEGORY = {
    unit: category
    for category, units in UNITS.items()
    for unit in units
}


ALL_UNITS = list(UNIT_TO_CATEGORY.keys())


# =========================
# Temperature Conversion
# =========================

def convert_temperature(value, from_unit, to_unit):
    # Convert to Celsius
    if from_unit == "Celsius":
        c = value
    elif from_unit == "Fahrenheit":
        c = (value - 32) * 5 / 9
    else:  # Kelvin
        c = value - 273.15

    # Celsius to target
    if to_unit == "Celsius":
        return c
    elif to_unit == "Fahrenheit":
        return c * 9 / 5 + 32
    else:
        return c + 273.15


# =========================
# General Conversion
# =========================

def convert_value(value, from_unit, to_unit):
    category = UNIT_TO_CATEGORY[from_unit]

    if category == "Temperature":
        return convert_temperature(
            value,
            from_unit,
            to_unit
        )

    factors = CONVERSION_FACTORS[category]

    base_value = value * factors[from_unit]

    return base_value / factors[to_unit]


# =========================
# Main Window
# =========================

class UnitConverter(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Unit Converter")
        self.resize(500, 300)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # Value input
        layout.addWidget(QLabel("Value"))

        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Enter a value")
        layout.addWidget(self.value_input)

        # From / Swap / To row
        row = QHBoxLayout()

        self.from_combo = QComboBox()
        self.populate_from_combo()

        self.from_combo.setEditable(True)

        completer = QCompleter(ALL_UNITS)
        completer.setCaseSensitivity(
            Qt.CaseSensitivity.CaseInsensitive
        )

        self.from_combo.setCompleter(completer)

        swap_button = QPushButton("⇄")
        swap_button.setFixedWidth(40)

        self.to_combo = QComboBox()

        row.addWidget(self.from_combo)
        row.addWidget(swap_button)
        row.addWidget(self.to_combo)

        layout.addLayout(row)

        # Category label
        self.category_label = QLabel("")
        layout.addWidget(self.category_label)

        # Result label
        self.result_label = QLabel("Result:")
        layout.addWidget(self.result_label)

        layout.addStretch()

        self.setLayout(layout)

        # Signals
        self.from_combo.currentTextChanged.connect(
            self.update_to_combo
        )

        self.from_combo.currentTextChanged.connect(
            self.convert
        )

        self.to_combo.currentTextChanged.connect(
            self.convert
        )

        self.value_input.textChanged.connect(
            self.convert
        )

        swap_button.clicked.connect(
            self.swap_units
        )

        self.update_to_combo()

    def populate_from_combo(self):
        model = QStandardItemModel()

        for category, units in UNITS.items():

            header = QStandardItem(
                category.upper()
            )

            header.setFlags(
                Qt.ItemFlag.NoItemFlags
            )

            model.appendRow(header)

            for unit in units:
                item = QStandardItem(
                    "   " + unit
                )

                model.appendRow(item)

        self.from_combo.setModel(model)

        # First selectable unit
        self.from_combo.setCurrentIndex(1)

    def current_from(self):
        return self.from_combo.currentText().strip()

    def update_to_combo(self):
        from_unit = self.current_from()

        if from_unit not in UNIT_TO_CATEGORY:
            return

        category = UNIT_TO_CATEGORY[from_unit]

        self.category_label.setText(
            f"Category: {category}"
        )

        current_to = self.to_combo.currentText()

        self.to_combo.blockSignals(True)

        self.to_combo.clear()
        self.to_combo.addItems(
            UNITS[category]
        )

        index = self.to_combo.findText(
            current_to
        )

        if index >= 0:
            self.to_combo.setCurrentIndex(index)

        self.to_combo.blockSignals(False)

        self.convert()

    def swap_units(self):
        from_unit = self.current_from()
        to_unit = self.to_combo.currentText()

        if (
            from_unit not in UNIT_TO_CATEGORY
            or to_unit not in UNIT_TO_CATEGORY
        ):
            return

        self.select_from_unit(to_unit)

        self.update_to_combo()

        index = self.to_combo.findText(
            from_unit
        )

        if index >= 0:
            self.to_combo.setCurrentIndex(index)

        self.convert()

    def select_from_unit(self, unit):
        model = self.from_combo.model()

        for row in range(model.rowCount()):
            text = model.item(row).text().strip()

            if text == unit:
                self.from_combo.setCurrentIndex(row)
                return

    def convert(self):
        try:
            value = float(
                self.value_input.text()
            )
        except ValueError:
            self.result_label.setText(
                "Result:"
            )
            return

        from_unit = self.current_from()
        to_unit = self.to_combo.currentText()

        if (
            from_unit not in UNIT_TO_CATEGORY
            or not to_unit
        ):
            return

        result = convert_value(
            value,
            from_unit,
            to_unit
        )

        self.result_label.setText(
            f"Result: "
            f"{value:g} {from_unit} = "
            f"{result:.10g} {to_unit}"
        )


# =========================
# Run Application
# =========================

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = UnitConverter()
    window.show()

    sys.exit(app.exec())