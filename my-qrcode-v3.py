import sys
import qrcode
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt


class QRCodeGeneratorApp(QWidget):
    """
    QR Code Generator (GUI version)

    Features:
    - Enter a URL to encode
    - Choose a QR code color
    - Set the output filename
    - Save as a PNG image with user-defined path
    - Simple graphical interface with PyQt5

    Usage:
    Run this script with Python 3 and PyQt5 installed:
        python my_qrcode-v3.py
    """

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("QR Code Generator")
        self.setGeometry(100, 100, 400, 280)

        main_layout = QVBoxLayout()

        # URL Input
        url_layout = QHBoxLayout()
        url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter the URL for the QR code")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        main_layout.addLayout(url_layout)

        # Output Filename Input
        filename_layout = QHBoxLayout()
        filename_label = QLabel("Output Filename:")
        self.filename_input = QLineEdit()
        self.filename_input.setPlaceholderText("e.g., my_qrcode.png")
        filename_layout.addWidget(filename_label)
        filename_layout.addWidget(self.filename_input)
        main_layout.addLayout(filename_layout)

        # QR Code Color Selector
        color_layout = QHBoxLayout()
        color_label = QLabel("QR Code Color:")
        self.color_selector = QComboBox()
        self.color_selector.addItems(["Black", "White", "Green", "Blue", "Red", "Yellow"])
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_selector)
        main_layout.addLayout(color_layout)

        # Spacer
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Buttons (Generate & Quit)
        button_layout = QHBoxLayout()
        generate_button = QPushButton("Generate QR Code")
        generate_button.clicked.connect(self.generate_qr_code)

        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.close)

        button_layout.addWidget(generate_button)
        button_layout.addWidget(quit_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def generate_qr_code(self):
        url = self.url_input.text().strip()
        output_filename = self.filename_input.text().strip()
        selected_color = self.color_selector.currentText()

        if not url:
            QMessageBox.warning(self, "Input Error", "Please enter a URL.")
            return

        if not output_filename:
            QMessageBox.warning(self, "Input Error", "Please enter an output filename.")
            return

        if not output_filename.lower().endswith(".png"):
            output_filename += ".png"

        color_map = {
            "Black": "black",
            "White": "white",
            "Green": "green",
            "Blue": "blue",
            "Red": "red",
            "Yellow": "yellow",
        }

        # Invert background and foreground if white is selected
        if selected_color == "White":
            fill_color = "white"
            back_color = "black"
        else:
            fill_color = color_map[selected_color]
            back_color = "white"

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color=fill_color, back_color=back_color)

            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save QR Code", output_filename, "PNG Images (*.png)"
            )

            if save_path:
                img.save(save_path)
                QMessageBox.information(self, "Success", f"QR code saved as: {save_path}")
            else:
                QMessageBox.information(self, "Canceled", "QR code generation canceled.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeGeneratorApp()
    window.show()
    sys.exit(app.exec_())