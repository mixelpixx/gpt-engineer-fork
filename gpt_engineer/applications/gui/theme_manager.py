"""
Theme manager for the GPT Engineer GUI.

This module provides functionality to manage and switch between different themes
in the application, including light and dark modes.
"""

from PyQt6.QtCore import QObject
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication

class ThemeManager(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_theme = "light"
        
    def set_light_theme(self):
        """Apply light theme to the application"""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(245, 245, 245))
        palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.ColorRole.Link, QColor(0, 100, 200))
        
        QApplication.instance().setPalette(palette)
        self.current_theme = "light"
        
    def set_dark_theme(self):
        """Apply dark theme to the application"""
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        
        QApplication.instance().setPalette(palette)
        self.current_theme = "dark"
        
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.current_theme == "light":
            self.set_dark_theme()
        else:
            self.set_light_theme()
