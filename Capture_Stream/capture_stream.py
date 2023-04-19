import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog, QComboBox, QGroupBox
from PyQt5.QtCore import QProcess, QTimer, QTime
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtCore import QUrl
from datetime import datetime

class StreamCaptureGUI(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the user interface
        self.init_ui()

        # Initialize the capture process
        self.capture_process = None

        # Initialize the pulse timer
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self.update_pulse)
        self.pulse_value = 0
        self.pulse_direction = 1

        # Initialize the elapsed time
        self.elapsed_time = QTime(0, 0)

    def init_ui(self):
        # Create a vertical layout
        layout = QVBoxLayout()

        # Advanced options group
        self.advanced_options_group = QGroupBox()
        advanced_options_layout = QVBoxLayout()

        # Input stream field
        self.input_stream_field = QLineEdit()
        self.input_stream_field.setText("https://stream.openbroadcaster.com:8043/CJUC")
        #self.input_stream_field.hide()
        layout.addWidget(QLabel("Input Stream:"))
        layout.addWidget(self.input_stream_field)

        # Output directory field
        self.output_dir_field = QLineEdit()
        self.output_dir_field.setText("C:/Users/Brett/Desktop/Capture_Stream")
        #self.output_dir_field.hide()
        layout.addWidget(QLabel("Output Directory:"))
        layout.addWidget(self.output_dir_field)

        # Browse button for output directory
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_output_dir)
        #self.browse_button.hide()
        layout.addWidget(self.browse_button)

        # Open output directory button
        self.open_output_dir_button = QPushButton("Open Output Directory")
        self.open_output_dir_button.clicked.connect(self.open_output_directory)
        layout.addWidget(self.open_output_dir_button)

        # Output file name field
        self.output_file_name_field = QLineEdit()
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H%M%S")+".mp3"
        self.output_file_name_field.setText(current_datetime)
        #self.output_file_name_field.hide()
        layout.addWidget(QLabel("Output Filename:"))
        layout.addWidget(self.output_file_name_field)

        # Bitrate field
        self.bitrate_field = QComboBox()
        self.bitrate_field.addItems(["64", "128", "256", "320"])
        self.bitrate_field.setCurrentText("256")
        #self.bitrate_field.hide()
        layout.addWidget(QLabel("Bitrate (kbps):"))
        layout.addWidget(self.bitrate_field)

        # Duration field
        self.duration_field = QLineEdit()
        #self.duration_field.hide()
        layout.addWidget(QLabel("Duration in minutes (optional):"))
        layout.addWidget(self.duration_field)

        # Advanced settings button
        self.advanced_button = QPushButton("Advanced settings")
        self.advanced_button.clicked.connect(self.toggle_advanced_options)
        self.advanced_button.hide()
        layout.addWidget(self.advanced_button)


        # Start and stop buttons
        buttons_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Recording", self)
        self.start_button.clicked.connect(self.start_button_clicked)
        self.start_button.setStyleSheet("""
            QPushButton {
                font: bold 16px;
                border-radius: 30px;
                height: 60px;
                border: 1px solid black;
                background-color: white;
            }
            QPushButton:hover {
                background-color: #6D0000;
            }
        """)


        buttons_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Recording", self)
        self.stop_button.clicked.connect(self.stop_stream_capture)

        self.stop_button.hide() #Hide the button initially
        buttons_layout.addWidget(self.stop_button)

        layout.addLayout(buttons_layout)

        # Set the layout for the widget
        self.setLayout(layout)

        # Set the window title
        self.setWindowTitle("Icecast Stream Capture")

        # Set a fixed window size
        self.setFixedSize(600, 400) #width 600, height 400


    # Run this when the start button is clicked
    def start_button_clicked(self):
        if self.validate_fields():
            self.start_stream_capture()

    # Check to see if input fields are valid
    def validate_fields(self):
        input_stream = self.input_stream_field.text().strip()
        output_dir = self.output_dir_field.text().strip()
        output_file_name = self.output_file_name_field.text().strip()

        if not input_stream or not output_dir or not output_file_name:
            QMessageBox.warning(self, "Validation Error", "Input Stream, Output Directory, and Output Filename cannot be empty.")
            return False

        return True


    def start_stream_capture(self):
        input_stream = self.input_stream_field.text()
        output_dir = self.output_dir_field.text()
        output_file_name = self.output_file_name_field.text()
        bitrate = self.bitrate_field.currentText()

        duration_text = self.duration_field.text()
        duration_string =""

        output_file = os.path.join(output_dir, output_file_name).replace(".mp3", "") +".mp3"


        # Check if the duration field has a value
        if duration_text:
            duration_minutes = float(self.duration_field.text())  # Get the duration in minutes
            duration_seconds = int(duration_minutes * 60)  # Convert the duration to seconds

            self.capture_process = subprocess.Popen([
            "ffmpeg", "-i", input_stream, "-acodec", "libmp3lame", "-ab", f"{bitrate}k", "-t", str(duration_seconds), "-vn", "-y", output_file
        ])

        else:
            print("")
            self.capture_process = subprocess.Popen([
                "ffmpeg", "-i", input_stream, "-acodec", "libmp3lame", "-ab", f"{bitrate}k", "-vn", "-y", output_file
            ])

        # Hide the start button and show the stop button
        self.start_button.hide()
        self.stop_button.show()

        # Start the pulse timer
        self.pulse_timer.start(20)

        # Reset and start the elapsed time
        self.elapsed_time.setHMS(0, 0, 0)
        self.elapsed_time.start()


    def stop_stream_capture(self):
        if hasattr(self, "capture_process"):
            self.capture_process.terminate()

        # Show the start button and hide the stop
        self.stop_button.hide()
        self.start_button.show()

        # Stop the pulse timer
        self.pulse_timer.stop()

    def update_pulse(self):
        self.pulse_value += self.pulse_direction * 10
        if self.pulse_value >= 255 or self.pulse_value <= 0:
            self.pulse_direction *= -1

        elapsed_seconds = self.elapsed_time.elapsed() // 1000
        hours = elapsed_seconds // 3600
        minutes = (elapsed_seconds % 3600) // 60
        seconds = elapsed_seconds % 60
        elapsed_time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.stop_button.setText(f"Stop Recording ({elapsed_time_str})")
        self.stop_button.setStyleSheet("QPushButton{background-color: #8B0000;font:bold 16px;height:60px;border 1px solid white;}")


    def browse_output_dir(self):
        output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if output_dir:
            self.output_dir_field.setText(output_dir)

    def open_output_directory(self):
        output_dir = self.output_dir_field.text()
        QDesktopServices.openUrl(QUrl.fromLocalFile(output_dir))

    def toggle_advanced_options(self):

        self.input_stream_field.show()
        self.output_dir_field.show()
        self.browse_button.show()
        self.output_file_name_field.show()
        self.bitrate_field.show()
        self.duration_field.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = StreamCaptureGUI()
    gui.show()
    sys.exit(app.exec_())
