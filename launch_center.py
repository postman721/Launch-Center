#Media Launcher
#Copyright (c) 2024 JJ Posti <techtimejourney.net>
#This program comes with ABSOLUTELY NO WARRANTY; for details see: [GNU GPL](http://www.gnu.org/copyleft/gpl.html).  
#This is free software, and you are welcome to redistribute it under GPL Version 2, June 1991.

import sys
import webbrowser
import subprocess

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QGridLayout, QPushButton, QScrollArea,
    QLabel, QComboBox, QGraphicsDropShadowEffect
)


def get_installed_browsers():
    """
    Check and return a list of installed browsers.
    Includes 'Default Browser' plus some popular commands.
    """
    possible = ["Default Browser", "firefox", "google-chrome", "chromium", "midori"]
    installed = []
    for b in possible:
        if b == "Default Browser":
            installed.append(b)
        else:
            try:
                webbrowser.get(b)
                installed.append(b)
            except webbrowser.Error:
                pass
    return installed


class MultiPlatformApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Launcher")

        # Media/Streaming services with URLs or 'steam' command
        self.platform_data = {
            "Netflix": "https://www.netflix.com/",
            "Hulu": "https://www.hulu.com/",
            "HBO Max": "https://play.hbomax.com/",
            "YouTube": "https://www.youtube.com/",
            "Spotify": "https://www.spotify.com/",
            "Disney+": "https://www.disneyplus.com/",
            "Amazon Prime": "https://www.primevideo.com/",
            "Apple TV": "https://tv.apple.com/",
            "SkyShowtime": "https://www.skyshowtime.com/",
            "Yle Areena": "https://areena.yle.fi/",
            "Steam": "steam",  # Launch with 'steam' command
        }

        self.browsers = get_installed_browsers()

        # Keep track of the service buttons
        self.service_buttons = []
        # Track which button is currently focused (arrow-key navigation)
        self.current_button_index = 0

        self.setup_ui()
        self.set_global_styles()
        self.center_window()  # Center the window after setup

    def setup_ui(self):
        # Main layout
        central = QWidget()
        central.setFocusPolicy(Qt.NoFocus)  # Do not focus the central widget
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # Title
        title = QLabel("Media Services")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 36px; font-weight: 800;")

        # Drop shadow for title
        title_shadow = QGraphicsDropShadowEffect(self)
        title_shadow.setBlurRadius(25)
        title_shadow.setColor(QColor(0, 0, 0, 180))
        title_shadow.setOffset(0, 2)
        title.setGraphicsEffect(title_shadow)
        title.setFocusPolicy(Qt.NoFocus)
        main_layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Use KDE Connect's Remote Input (arrows + Enter) or click with mouse")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #CCCCCC; font-size: 18px; margin-bottom: 15px;")
        subtitle.setFocusPolicy(Qt.NoFocus)
        main_layout.addWidget(subtitle)

        # Browser selection row
        browser_layout = QHBoxLayout()
        browser_label = QLabel("Browser:")
        browser_label.setStyleSheet("color: white; font-size: 16px; font-weight: 600;")
        browser_label.setFocusPolicy(Qt.NoFocus)
        browser_layout.addWidget(browser_label)

        self.browser_combo = QComboBox()
        # Focus only on mouse click, not arrow keys
        self.browser_combo.setFocusPolicy(Qt.ClickFocus)
        self.browser_combo.addItems(self.browsers)
        if "firefox" in self.browsers:
            self.browser_combo.setCurrentText("firefox")
        browser_layout.addWidget(self.browser_combo)
        main_layout.addLayout(browser_layout)

        # Scrollable area for grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(Qt.NoFocus)
        main_layout.addWidget(scroll_area)

        container = QWidget()
        container.setFocusPolicy(Qt.NoFocus)
        scroll_area.setWidget(container)

        self.grid_layout = QGridLayout(container)
        self.grid_layout.setSpacing(30)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)

        # Create service buttons in a 4-column grid
        for i, (name, link) in enumerate(self.platform_data.items()):
            btn = QPushButton(name)
            btn.setMinimumHeight(60)
            # Enable arrow-key focus
            btn.setFocusPolicy(Qt.StrongFocus)

            if name == "Steam":
                btn.clicked.connect(self.launch_steam)
            else:
                btn.clicked.connect(lambda _, url=link: self.open_link(url))

            self.service_buttons.append(btn)

            row, col = divmod(i, 4)
            self.grid_layout.addWidget(btn, row, col)

        # Focus first button if available
        if self.service_buttons:
            self.current_button_index = 0
            self.service_buttons[0].setFocus()

    def set_global_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(
                    spread: pad,
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 rgba(20, 20, 20, 1),
                    stop: 0.4 rgba(30, 30, 30, 1),
                    stop: 0.8 rgba(10, 10, 10, 1),
                    stop: 1 rgba(5, 5, 5, 1)
                );
            }

            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
            }

            QPushButton {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                border-radius: 20px;
                padding: 15px;
                font-size: 18px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.4);
            }
            QPushButton:focus {
                outline: 2px solid rgba(255, 255, 255, 0.6);
            }

            QComboBox {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                padding: 6px 12px;
                font-size: 16px;
                font-weight: 500;
            }
            QComboBox:hover {
                background-color: rgba(255, 255, 255, 0.2);
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox QAbstractItemView {
                background-color: rgba(50, 50, 50, 1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                selection-background-color: rgba(255, 255, 255, 0.3);
                selection-color: white;
            }
        """)

    def center_window(self):
        """
        Centers the window on the screen.
        """
        frame_geometry = self.frameGeometry()
        screen = QApplication.primaryScreen()
        center_point = screen.availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def open_link(self, url):
        """Open a link in chosen or default browser."""
        choice = self.browser_combo.currentText()
        if choice == "Default Browser":
            webbrowser.open(url)
        else:
            try:
                browser = webbrowser.get(choice)
                browser.open(url)
            except webbrowser.Error:
                # Fallback to system default
                webbrowser.open(url)

    def launch_steam(self):
        """Launch Steam with 'steam' command."""
        try:
            subprocess.Popen(["steam"], shell=False)
        except FileNotFoundError:
            print("Error: Steam is not installed or not in PATH.")
        except Exception as e:
            print("Unexpected error:", e)

    def keyPressEvent(self, event):
        """
        Override to handle arrow key navigation among the service_buttons.
        KDE Connect's Remote Input typically sends these as well.
        """
        if not self.service_buttons:
            return

        key = event.key()
        total = len(self.service_buttons)
        cols = 4  # number of columns in the grid

        if key == Qt.Key_Left:
            new_index = max(0, self.current_button_index - 1)
            self.set_focus_to_button(new_index)

        elif key == Qt.Key_Right:
            new_index = min(total - 1, self.current_button_index + 1)
            self.set_focus_to_button(new_index)

        elif key == Qt.Key_Up:
            new_index = self.current_button_index - cols
            if new_index >= 0:
                self.set_focus_to_button(new_index)

        elif key == Qt.Key_Down:
            new_index = self.current_button_index + cols
            if new_index < total:
                self.set_focus_to_button(new_index)

        elif key in (Qt.Key_Return, Qt.Key_Enter):
            self.service_buttons[self.current_button_index].click()

        elif key == Qt.Key_Escape:
            # If user presses back/escape, do nothing or close
            pass

        # Otherwise, ignore or pass to super
        # super().keyPressEvent(event)

    def set_focus_to_button(self, new_index):
        """Focus the button at new_index in the service_buttons list."""
        self.current_button_index = new_index
        self.service_buttons[new_index].setFocus()


def main():
    app = QApplication(sys.argv)
    win = MultiPlatformApp()
    win.resize(1000, 700)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
