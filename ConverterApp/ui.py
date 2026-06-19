
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QApplication
)
from PySide6.QtGui import QColor

from PySide6.QtGui import (
    QStandardItemModel,
    QStandardItem,
)

from PySide6.QtCore import (
    Qt,
    QTimer
)

from conversions import (
    UNITS,
    UNIT_TO_CATEGORY,
    CATEGORY_ICONS,
    convert_value,
)


class UnitConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.last_result = ""
        self.last_result_value = ""

        self.setup_window()
        self.build_ui()
        self.connect_signals()

        self.update_to_combo()

    def setup_window(self):
        self.setWindowTitle("Unit Converter")
        self.resize(600, 420)

    def build_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # ======================
        # Title
        # ======================

        title = QLabel("Unit Converter")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(title)

        # ======================
        # Card
        # ======================

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(16)

        # ======================
        # Value Input
        # ======================

        value_label = QLabel("Value")

        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText(
            "Enter a value..."
        )

        card_layout.addWidget(value_label)
        card_layout.addWidget(self.value_input)

        # ======================
        # From / Swap / To
        # ======================

        conversion_row = QHBoxLayout()
        conversion_row.setSpacing(12)

        self.from_combo = QComboBox()
        self.populate_from_combo()

        self.swap_button = QPushButton("⇄")
        self.swap_button.setObjectName("swapButton")

        self.to_combo = QComboBox()

        conversion_row.addWidget(self.from_combo)
        conversion_row.addWidget(self.swap_button)
        conversion_row.addWidget(self.to_combo)

        card_layout.addLayout(conversion_row)

        # ======================
        # Category
        # ======================

        self.category_label = QLabel()
        self.category_label.setObjectName(
            "categoryLabel"
        )

        card_layout.addWidget(self.category_label)

        card.setLayout(card_layout)

        main_layout.addWidget(card)

        # ======================
        # Result Card
        # ======================

        result_card = QFrame()
        result_card.setObjectName("card")

        result_layout = QVBoxLayout()
        result_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        self.result_label = QLabel(
            "Enter a value to begin."
        )


        self.result_label.setObjectName(
            "resultLabel"
        )

        self.result_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.copy_button = QPushButton("📋 Copy Result")
        self.copy_button.setEnabled(False)

        result_layout.addWidget(
            self.result_label
        )

        result_layout.addWidget(
            self.copy_button
        )

        result_card.setLayout(result_layout)

        main_layout.addWidget(result_card)

        main_layout.addStretch()

        self.setLayout(main_layout)

    def connect_signals(self):
        self.from_combo.currentTextChanged.connect(
            self.update_to_combo
        )

        self.to_combo.currentTextChanged.connect(
            self.convert
        )

        self.value_input.textChanged.connect(
            self.convert
        )

        self.swap_button.clicked.connect(
            self.swap_units
        )

        self.copy_button.clicked.connect(
            self.copy_result
        )

    # =====================================
    # Populate From Combo
    # =====================================

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

        # First selectable item
        self.from_combo.setCurrentIndex(1)

    # =====================================
    # Helpers
    # =====================================

    def current_from_unit(self):
        return (
            self.from_combo.currentText()
            .strip()
        )

    # =====================================
    # To Combo
    # =====================================

    def update_to_combo(self):
        from_unit = self.current_from_unit()

        if (
            from_unit
            not in UNIT_TO_CATEGORY
        ):
            return

        category = UNIT_TO_CATEGORY[
            from_unit
        ]

        icon = CATEGORY_ICONS.get(
            category,
            ""
        )

        self.category_label.setText(
            f"{icon} {category}"
        )

        current_to = (
            self.to_combo.currentText()
        )

        model = QStandardItemModel()

        for unit in UNITS[category]:
            item = QStandardItem(unit)

            # Disable same unit
            if unit == from_unit:
                item.setFlags(
                    item.flags()
                    & ~Qt.ItemFlag.ItemIsEnabled
                )
                item.setForeground( QColor("#9aa0a6") )

            model.appendRow(item)

        self.to_combo.blockSignals(True)

        self.to_combo.setModel(model)

        index = self.to_combo.findText(
            current_to
        )

        if index >= 0:
            self.to_combo.setCurrentIndex(
                index
            )
        else:
            for i in range(
                model.rowCount()
            ):
                if (
                    model.item(i).isEnabled()
                ):
                    self.to_combo.setCurrentIndex(
                        i
                    )
                    break

        self.to_combo.blockSignals(False)

        self.convert()

    # =====================================
    # Swap
    # =====================================

    def swap_units(self):
        from_unit = (
            self.current_from_unit()
        )

        to_unit = (
            self.to_combo.currentText()
        )

        if (
            from_unit
            not in UNIT_TO_CATEGORY
        ):
            return

        if (
            to_unit
            not in UNIT_TO_CATEGORY
        ):
            return

        model = self.from_combo.model()

        for row in range(
            model.rowCount()
        ):
            text = (
                model.item(row)
                .text()
                .strip()
            )

            if text == to_unit:
                self.from_combo.setCurrentIndex(
                    row
                )
                break

        self.update_to_combo()

        index = (
            self.to_combo.findText(
                from_unit
            )
        )

        if index >= 0:
            self.to_combo.setCurrentIndex(
                index
            )

        self.convert()

    # =====================================
    # Convert
    # =====================================


    def convert(self):
        text = (
            self.value_input.text()
            .strip()
        )

        try:
            value = float(text)

        except ValueError:
            # Lenient behavior:
            # keep previous result
            return

        from_unit = (
            self.current_from_unit()
        )

        to_unit = (
            self.to_combo.currentText()
        )

        if (
            from_unit
            not in UNIT_TO_CATEGORY
        ):
            return

        if (
            to_unit
            not in UNIT_TO_CATEGORY
        ):
            return

        result = convert_value(
            value,
            from_unit,
            to_unit
        )

        def format_number(number):
            return f"{number:.4f}".rstrip("0").rstrip(".")
        
        result_text = (
            f"{format_number(value)} {from_unit}\n"
            f"=\n"
            f"{format_number(result)} {to_unit}"
        )

        self.last_result = result_text

        self.last_result_value = f"{format_number(result)}"

        self.result_label.setText(
            result_text
        )

        self.copy_button.setEnabled(True)

    def copy_result(self):
        if not self.last_result:
            return
        
        clipboard = (
            QApplication.clipboard()
        )

        clipboard.setText(
            self.last_result_value
        )

        self.copy_button.setText(
            "✓ Copied!"
        )

        QTimer.singleShot(
            1500,
            lambda: self.copy_button.setText(
                "📋 Copy Result"
            )
        )