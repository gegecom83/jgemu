from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QListWidget, QScrollBar, QGridLayout, QWidget, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import configparser
import os
import subprocess
import sys


class jgemu(QMainWindow):
    """
    The main window.
    """
    def __init__(self):
        super().__init__()
        self.main_window_design()
        self.set_main_window_bindings()
        self.load_from_ini()

    def main_window_design(self):
        """
        Design the main window.
        """
        self.setGeometry(100, 100, 900, 600)
        self.setMinimumSize(300, 200)
        self.setWindowIcon(QIcon("icon.ico"))
        self.setWindowTitle("jgemu")

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(2, 3)
        layout.setRowStretch(1, 1)

        # Systems label and list
        self.systems_label = QLabel("Systems", self)
        self.systems_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.systems_label, 0, 0)
        self.systems_list = QListWidget(self)
        self.systems_list.setSelectionMode(QListWidget.SingleSelection)
        layout.addWidget(self.systems_list, 1, 0)

        # Games label and list
        self.games_label = QLabel("Games", self)
        self.games_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.games_label, 0, 2)
        self.games_list = QListWidget(self)
        self.games_list.setSelectionMode(QListWidget.SingleSelection)
        layout.addWidget(self.games_list, 1, 2)

        # Scrollbars
        self.systems_scrollbar = QScrollBar(Qt.Vertical, self)
        layout.addWidget(self.systems_scrollbar, 1, 1)
        self.games_scrollbar = QScrollBar(Qt.Vertical, self)
        layout.addWidget(self.games_scrollbar, 1, 3)

        # Connect scrollbars
        self.systems_list.setVerticalScrollBar(self.systems_scrollbar)
        self.games_list.setVerticalScrollBar(self.games_scrollbar)

        # Set focus to systems list
        self.systems_list.setFocus()

    def set_main_window_bindings(self):
        """
        Set the key bindings of the main window.
        """
        self.systems_list.itemSelectionChanged.connect(self.on_platform_selection)
        self.games_list.itemDoubleClicked.connect(self.on_game_selection)
        self.games_list.keyPressEvent = self.key_press_event

    def key_press_event(self, event):
        """
        Handle key press events for the games list and main window.
        """
        if event.key() == Qt.Key_Return and self.games_list.hasFocus():
            if self.games_list.currentItem():
                self.on_game_selection(self.games_list.currentItem())
        elif event.key() == Qt.Key_R and event.modifiers() == Qt.ControlModifier:
            self.reload_from_ini()
        elif event.key() == Qt.Key_A and event.modifiers() == Qt.ControlModifier:
            self.about_program()
        elif event.key() == Qt.Key_Escape:
            self.quit_program()
        else:
            super(QListWidget, self.games_list).keyPressEvent(event)

    def load_from_ini(self):
        """
        Check if config.ini exists and if it's not empty, then load the program.
        """
        if not os.path.isfile("config.ini"):
            self.show_error(0)
        else:
            self.config = configparser.ConfigParser()
            self.config.read("config.ini")
            self.sections = self.config.sections()

            if not self.sections:
                self.show_error(1)
            else:
                self.display_systems()
                self.default_platform_selection()

    def display_systems(self):
        """
        Display the systems.
        """
        self.systems_list.clear()
        for platform in self.sections:
            self.systems_list.addItem(platform)
        if self.systems_list.count() > 0:
            self.systems_list.setCurrentRow(0)

    def default_platform_selection(self):
        """
        Show the games of the default platform.
        """
        self.platform = self.sections[0]
        self.parameters_separator = ","
        self.parameters_already_split = False
        self.check_options()

    def get_required_options_from_ini(self):
        """
        Get the options from config.ini.
        """
        self.games_folder = self.config.get(self.platform, "games")
        self.executable = self.config.get(self.platform, "executable")
        self.extensions = self.config.get(self.platform, "extensions")
        self.working_dir = self.config.get(self.platform, "working_dir") if self.config.has_option(self.platform, "working_dir") else None

    def check_options(self):
        """
        Check if required options are present.
        """
        if not self.config.has_option(self.platform, "games"):
            self.show_error(2)
        elif not self.config.has_option(self.platform, "executable"):
            self.show_error(3)
        elif not self.config.has_option(self.platform, "extensions"):
            self.show_error(4)
        else:
            self.get_required_options_from_ini()

            if not self.games_folder:
                self.show_error(2)
            elif not self.executable:
                self.show_error(3)
            elif not self.extensions:
                self.show_error(4)
            else:
                self.extensions = [ext.strip() for ext in self.extensions.split(",")]
                self.display_games()

    def display_games(self):
        """
        Show the games in the games list, including those in subfolders.
        """
        self.games_list.clear()
        for root, _, files in os.walk(self.games_folder):
            for file in files:
                _, game_extension = os.path.splitext(file)
                if game_extension in self.extensions:
                    relative_path = os.path.relpath(os.path.join(root, file), self.games_folder)
                    self.games_list.addItem(relative_path)
        if self.games_list.count() > 0:
            self.games_list.setCurrentRow(0)

    def on_platform_selection(self):
        """
        Show the games of the selected platform.
        """
        self.games_list.clear()
        selected_items = self.systems_list.selectedItems()
        if selected_items:
            self.platform = selected_items[0].text()
            self.parameters_separator = ","
            self.parameters_already_split = False
            self.check_options()

    def on_game_selection(self, item):
        """
        Launch the emulator.
        """
        self.game = item.text()
        self.full_path = os.path.join(self.games_folder, self.game)
        self.get_parameters_from_ini()

        try:
            working_dir = self.working_dir if self.working_dir else os.path.dirname(self.executable)
            command = f'"{self.executable}" {" ".join(self.parameters)} "{self.full_path}"'
            print("Command executed:", command)
            print("Working directory:", working_dir)
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                cwd=working_dir,
                shell=True
            )
        except subprocess.CalledProcessError as e:
            print("Execution error (STDERR):", e.stderr)
            print("Execution output (STDOUT):", e.stdout)
            QMessageBox.critical(self, "Error", f"Failed to launch emulator:\nSTDERR: {e.stderr}\nSTDOUT: {e.stdout}")
        except Exception as e:
            print("Unexpected error:", str(e))
            QMessageBox.critical(self, "Error", f"Unexpected error: {str(e)}")

    def get_parameters_from_ini(self):
        """
        Get the parameters from config.ini.
        """
        if not self.parameters_already_split:
            if not self.config.has_option(self.platform, "parameters"):
                self.parameters = ""
            else:
                self.parameters = self.config.get(self.platform, "parameters")
            self.split_parameters()

    def split_parameters(self):
        """
        Split the parameters.
        """
        self.parameters = [param.strip() for param in self.parameters.split(self.parameters_separator)]
        self.parameters_already_split = True

    def reload_from_ini(self):
        """
        Reload information from config.ini.
        """
        self.games_list.clear()
        self.systems_list.clear()
        self.systems_list.setFocus()
        self.load_from_ini()

    def quit_program(self):
        """
        Quit the program.
        """
        self.close()
        QApplication.quit()

    def about_program(self):
        """
        Show an information message.
        """
        QMessageBox.information(
            self,
            "About",
            "jgemu\n"
            "Version: 1.0.2\n"
            "Contact: gegecom83@gmail.com"
        )

    def show_error(self, type_of_error):
        """
        Show an error message.
        """
        self.error_messages = {
            0: "Your config.ini file is missing.",
            1: "Your config.ini file is empty.",
            2: "The selected platform is missing the 'games' option.",
            3: "The selected platform is missing the 'executable' option.",
            4: "The selected platform is missing the 'extensions' option.",
        }
        QMessageBox.critical(self, "Error", self.error_messages[type_of_error])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_gui = jgemu()
    start_gui.show()
    sys.exit(app.exec_())