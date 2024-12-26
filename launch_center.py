#Launch Center
#Copyright (c) 2024 JJ Posti <techtimejourney.net>
#This program comes with ABSOLUTELY NO WARRANTY; for details see: [GNU GPL](http://www.gnu.org/copyleft/gpl.html).  
#This is free software, and you are welcome to redistribute it under GPL Version 2, June 1991.

import sys
import asyncio
from qasync import QEventLoop, asyncSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class MediaLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Launch Center")
        self.resize(800, 600)

        # Center the window on the screen
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        # Main widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Buttons for media platforms
        button_style = """
            QPushButton {
                background-color: #2A2A2A;
                color: #EEEEEE;
                font-family: Arial, Helvetica, sans-serif;
                font-size: 18px;
                padding: 15px;
                border-radius: 8px;
                border: 2px solid #444444;
                text-transform: uppercase;
            }
            QPushButton:hover {
                background-color: #3E3E3E;
                border-color: #666666;
            }
            QPushButton:pressed {
                background-color: #1E1E1E;
                border-color: #888888;
            }
        """

        #Set browser
        self.browser="firefox"
        
        netflix_button = QPushButton("Open Netflix")
        netflix_button.setStyleSheet(button_style)
        netflix_button.clicked.connect(lambda: asyncio.ensure_future(self.open_url("https://www.netflix.com")))
        layout.addWidget(netflix_button)

        yle_button = QPushButton("Open Yle Areena")
        yle_button.setStyleSheet(button_style)
        yle_button.clicked.connect(lambda: asyncio.ensure_future(self.open_url("https://areena.yle.fi")))
        layout.addWidget(yle_button)

        disney_button = QPushButton("Open Disney Plus")
        disney_button.setStyleSheet(button_style)
        disney_button.clicked.connect(lambda: asyncio.ensure_future(self.open_url("https://www.disneyplus.com")))
        layout.addWidget(disney_button)

        apple_button = QPushButton("Open Apple TV")
        apple_button.setStyleSheet(button_style)
        apple_button.clicked.connect(lambda: asyncio.ensure_future(self.open_url("https://tv.apple.com")))
        layout.addWidget(apple_button)

        discovery_button = QPushButton("Open Discovery Plus")
        discovery_button.setStyleSheet(button_style)
        discovery_button.clicked.connect(lambda: asyncio.ensure_future(self.open_url("https://www.discoveryplus.com")))
        layout.addWidget(discovery_button)

        youtube_button = QPushButton("Open YouTube")
        youtube_button.setStyleSheet(button_style)
        youtube_button.clicked.connect(lambda: asyncio.ensure_future(self.open_url("https://www.youtube.com")))
        layout.addWidget(youtube_button)

        steam_button = QPushButton("Open Steam")
        steam_button.setStyleSheet(button_style)
        steam_button.clicked.connect(lambda: asyncio.ensure_future(self.open_steam()))
        layout.addWidget(steam_button)

        # Set layout and background style
        central_widget.setLayout(layout)
        central_widget.setStyleSheet("background-color: #1E1E1E;")
        self.setCentralWidget(central_widget)

    @asyncSlot()
    async def open_steam(self):
        try:
            process = await asyncio.create_subprocess_exec("steam")
            await process.wait()
        except FileNotFoundError:
            print("Steam is not installed or not found in PATH.")
        except Exception as e:
            print(f"Error launching Steam: {e}")

    @asyncSlot()
    async def open_url(self, url):
        try:
            process = await asyncio.create_subprocess_exec(self.browser, url)
            await process.wait()
        except Exception as e:
            print(f"Error opening {url}: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    launcher = MediaLauncher()
    launcher.show()

    with loop:
        loop.run_forever()
