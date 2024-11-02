"""
Main window implementation for the GPT Engineer GUI.

This module contains the MainWindow class which serves as the primary interface
for the GPT Engineer application. It provides a modern, intuitive interface for
users to interact with the AI code generation and improvement capabilities.
"""

import os
import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QLabel,
    QStatusBar,
    QTabWidget,
    QTreeView,
    QSplitter,
)

from gpt_engineer.applications.cli.main import load_env_if_needed
from gpt_engineer.core.default.disk_memory import DiskMemory
from gpt_engineer.core.default.paths import memory_path
from gpt_engineer.applications.gui.theme_manager import ThemeManager
from gpt_engineer.applications.gui.file_tree_model import FileTreeModel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GPT Engineer")
        self.setMinimumSize(1200, 800)
        
        # Initialize environment
        load_env_if_needed()
        
        self.theme_manager = ThemeManager(self)
        self.file_tree_model = None
        
        self.setup_ui()
        self.setup_menubar()
        self.setup_statusbar()
        self.setup_theme()
        
    def setup_ui(self):
        """Set up the main user interface components"""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Project Navigation
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Project tree
        self.project_tree = QTreeView()
        self.file_tree_model = FileTreeModel(Path.home())
        self.project_tree.setModel(self.file_tree_model)
        left_layout.addWidget(QLabel("Project Files"))
        left_layout.addWidget(self.project_tree)
        
        # Right panel - Main content area
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Tab widget for different views
        self.tab_widget = QTabWidget()
        
        # Prompt tab
        prompt_tab = QWidget()
        prompt_layout = QVBoxLayout(prompt_tab)
        self.prompt_edit = QTextEdit()
        self.prompt_edit.setPlaceholderText("Enter your prompt here...")
        prompt_layout.addWidget(self.prompt_edit)
        
        # Generate button
        generate_btn = QPushButton("Generate Code")
        generate_btn.clicked.connect(self.generate_code)
        prompt_layout.addWidget(generate_btn)
        
        # Output tab
        output_tab = QWidget()
        output_layout = QVBoxLayout(output_tab)
        self.output_edit = QTextEdit()
        self.output_edit.setReadOnly(True)
        output_layout.addWidget(self.output_edit)
        
        # Add tabs
        self.tab_widget.addTab(prompt_tab, "Prompt")
        self.tab_widget.addTab(output_tab, "Output")
        
        right_layout.addWidget(self.tab_widget)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        
        # Set initial sizes
        splitter.setSizes([300, 900])
        
        main_layout.addWidget(splitter)
        
    def setup_menubar(self):
        """Set up the application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_project = QAction("New Project", self)
        new_project.triggered.connect(self.new_project)
        file_menu.addAction(new_project)
        
        open_project = QAction("Open Project", self)
        open_project.triggered.connect(self.open_project)
        file_menu.addAction(open_project)
        
        # Settings menu
        settings_menu = menubar.addMenu("Settings")
        
        theme_menu = settings_menu.addMenu("Theme")
        light_theme = QAction("Light", self)
        light_theme.triggered.connect(self.theme_manager.set_light_theme)
        dark_theme = QAction("Dark", self)
        dark_theme.triggered.connect(self.theme_manager.set_dark_theme)
        theme_menu.addAction(light_theme)
        theme_menu.addAction(dark_theme)
        
    def setup_statusbar(self):
        """Set up the status bar"""
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
        
        # Add token usage display
        self.token_label = QLabel("Tokens: 0")
        self.statusBar.addPermanentWidget(self.token_label)
        
    def setup_theme(self):
        """Set up the initial theme"""
        self.theme_manager.set_light_theme()
        
    def new_project(self):
        """Create a new project"""
        directory = QFileDialog.getExistingDirectory(self, "Select Project Directory")
        if directory:
            # Initialize project
            self.current_project_path = Path(directory)
            self.file_tree_model = FileTreeModel(self.current_project_path)
            self.project_tree.setModel(self.file_tree_model)
            self.statusBar.showMessage(f"Created new project in {directory}")
            
    def open_project(self):
        """Open an existing project"""
        directory = QFileDialog.getExistingDirectory(self, "Open Project Directory")
        if directory:
            # Load project
            self.current_project_path = Path(directory)
            self.file_tree_model = FileTreeModel(self.current_project_path)
            self.project_tree.setModel(self.file_tree_model)
            self.statusBar.showMessage(f"Opened project: {directory}")
            
    def generate_code(self):
        """Handle code generation"""
        if not hasattr(self, 'current_project_path'):
            QMessageBox.warning(self, "Warning", "Please create or open a project first.")
            return
            
        prompt = self.prompt_edit.toPlainText()
        if not prompt:
            QMessageBox.warning(self, "Warning", "Please enter a prompt first.")
            return
            
        # Here we'll add the actual code generation logic
        self.statusBar.showMessage("Generating code...")
        
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
