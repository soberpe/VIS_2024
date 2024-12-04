import mbsModel

import os

from vtkmodules.vtkCommonColor import vtkNamedColors

from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkPolyDataMapper,
    vtkActor,
    vtkRenderer
)

from vtkmodules.all import vtkInteractorStyleTrackballCamera

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QMainWindow, QFileDialog, QInputDialog

import QVTKRenderWindowInteractor as QVTK
QVTKRenderWindowInteractor = QVTK.QVTKRenderWindowInteractor
from PySide6.QtCore import Qt
Qt.MidButton = Qt.MiddleButton

class pyFreeDynMainWindow(QMainWindow):
    def __init__(self):
        self.dataModel = mbsModel.mbsModel()

        QMainWindow.__init__(self)
        self.setWindowTitle("pyFreeDyn")
        
        # create the widget
        self.widget = QVTKRenderWindowInteractor(self)
        self.setCentralWidget(self.widget)

        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("file")
        self.settings_menu = self.menu.addMenu("settings")
        settings_action = QAction("scale factor", self)
        self.scaleFactor = 1.
        settings_action.triggered.connect(self.openSettingsDialog)
        self.settings_menu.addAction(settings_action)

        ## Open QAction
        open_action = QAction("open", self)
        open_action.triggered.connect(self.loadModel)
        self.file_menu.addAction(open_action)

        ## Exit QAction
        exit_action = QAction("exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()
        self.status.showMessage("Data loaded and plotted")

        # Window dimensions
        geometry = self.screen().availableGeometry()
        self.setBaseSize(geometry.width() * 0.8, geometry.height() * 0.7)
        
        self.ren = vtkRenderer()
        self.widget.GetRenderWindow().AddRenderer(self.ren)

        # Create a renderwindowinteractor for allowing user to interact with 3D scene
        self.iren = vtkRenderWindowInteractor()
        style = vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(style)
        self.iren.SetRenderWindow(self.widget.GetRenderWindow())

        colors = vtkNamedColors()
        self.ren.SetBackground(colors.GetColor3d('White'))

        QMainWindow.show(self)
        
    def show(self):        
        # Enable user interface interactor
        self.iren.Initialize()

        self.widget.Initialize()
        self.iren.Start()
        self.widget.Start()
    
    def loadModel(self):
        if hasattr(self, 'dataModel'):
            self.dataModel.clear()

        fname = QFileDialog.getOpenFileName(self, 'Select FreeDyn database file', 
         'C:\\VIS_2024\\Aufgabe_3',"FreeDyn database file (*.fdd)")

        os.chdir(os.path.dirname(fname[0]))
        self.dataModel.importFddFile(fname[0])

        self.dataModel.showModel(self.ren)

    def openSettingsDialog(self):
        text, ok = QInputDialog.getText(self, 'scale factor settings', 'type scale factor here')
        if ok:
            self.scaleFactor = float(text)
            if hasattr(self, 'dataModel'):
                for object in self.dataModel:
                    object.setScaleFactor(float(text))