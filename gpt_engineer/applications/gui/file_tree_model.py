"""
File tree model for the GPT Engineer GUI.

This module provides a model for displaying and managing project files in a
tree view structure, making it easy for users to navigate their project files.
"""

from PyQt6.QtCore import Qt, QAbstractItemModel, QModelIndex
from PyQt6.QtGui import QIcon
from pathlib import Path

class FileTreeItem:
    def __init__(self, path: Path, parent=None):
        self.path = path
        self.parent_item = parent
        self.child_items = []
        self.loaded = False
        
    def load_children(self):
        """Load child items from the filesystem"""
        if self.loaded:
            return
            
        if self.path.is_dir():
            for child_path in sorted(self.path.iterdir()):
                # Skip hidden files and common ignore patterns
                if not child_path.name.startswith('.') and child_path.name not in {
                    '__pycache__', 'node_modules', 'venv'
                }:
                    self.child_items.append(FileTreeItem(child_path, self))
                    
        self.loaded = True
        
    def child(self, row):
        """Get child item at specified row"""
        if row < 0 or row >= len(self.child_items):
            return None
        return self.child_items[row]
        
    def child_count(self):
        """Get number of child items"""
        self.load_children()
        return len(self.child_items)
        
    def row(self):
        """Get row number of this item"""
        if self.parent_item:
            return self.parent_item.child_items.index(self)
        return 0
        
class FileTreeModel(QAbstractItemModel):
    def __init__(self, root_path: Path):
        super().__init__()
        self.root_item = FileTreeItem(root_path)
        
    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
            
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
            
        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QModelIndex()
        
    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
            
        child_item = index.internalPointer()
        parent_item = child_item.parent_item
        
        if parent_item == self.root_item:
            return QModelIndex()
            
        return self.createIndex(parent_item.row(), 0, parent_item)
        
    def rowCount(self, parent=QModelIndex()):
        if parent.column() > 0:
            return 0
            
        if not parent.isValid():
            parent_item = self.root_item
        else:
            parent_item = parent.internalPointer()
            
        return parent_item.child_count()
        
    def columnCount(self, parent=QModelIndex()):
        return 1
        
    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
            
        item = index.internalPointer()
        
        if role == Qt.ItemDataRole.DisplayRole:
            return item.path.name
            
        return None
