### Launch Center


Launch Center is a sleek and user-friendly media launcher application built with Python and PyQt5. It allows you to quickly access your favorite media platforms with just a click, streamlining your entertainment experience.


Features

    Easy Access: Launch popular media platforms like Netflix, Disney Plus, YouTube, and more with a single click.
    Asynchronous Operations: Utilizes asyncio for efficient and responsive UI interactions.
    Customizable Interface: Stylish and modern button designs with hover and press effects.
    Cross-Platform Support: Compatible with Windows, macOS, and Linux.
    Open Source: Released under the GNU GPL v2 license, allowing for free use and distribution.


Usage

After installing the dependencies, you can run the Launch Center application using the following command:

    python launch_center.py


Install Dependencies

    sudo apt install python3-pyqt5 python3-pyqt5.qtwebengine python3-qasync

 Usage

Make executable with: 

    chmod +x launch_center.py

After installing the dependencies, you can run the Launch Center application using the following command:

    python launch_center.py

Application Overview

    Main Window: A clean and centered window displaying buttons for various media platforms.
    Buttons: Each button corresponds to a different media service. Clicking a button will open the respective service in your default browser or launch the Steam application.

Supported Media Platforms

    Netflix: Opens Netflix in your default browser.
    Yle Areena: Opens Yle Areena in your default browser.
    Disney Plus: Opens Disney Plus in your default browser.
    Apple TV: Opens Apple TV in your default browser.
    Discovery Plus: Opens Discovery Plus in your default browser.
    YouTube: Opens YouTube in your default browser.
    Steam: Launches the Steam application if installed.

Customizing the Browser

By default, the application uses Firefox to open URLs. You can change the browser by modifying the self.browser variable in the MediaLauncher class:

self.browser = "your_preferred_browser_executable"

For example, to use firefox:

self.browser = "firefox"
