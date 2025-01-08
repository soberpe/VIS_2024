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
from PySide6.QtWidgets import QMainWindow, QFileDialog, QInputDialog, QApplication

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

        ## Load QAction
        load_action = QAction("Load", self)
        load_action.triggered.connect(self.loadModel)
        self.file_menu.addAction(load_action)

        ## Save QAction
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.saveModel)
        self.file_menu.addAction(save_action)

        ## Load QAction
        import_action = QAction("ImportFdd", self)
        import_action.triggered.connect(self.importModel)
        self.file_menu.addAction(import_action)

        ## Exit QAction
        exit_action = QAction("exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(exit_action)

        # Status Bar
        self.status = self.statusBar()

        # Window dimensions
        geometry = self.screen().availableGeometry()
        self.setBaseSize(geometry.width() * 0.8, geometry.height() * 0.7)
        
        self.ren = vtkRenderer()
        self.widget.GetRenderWindow().AddRenderer(self.ren)

        # Create a renderwindowinteractor for allowing user to interact with 3D scene
        self.iren = self.widget.GetRenderWindow().GetInteractor()
        style = vtkInteractorStyleTrackballCamera()
        self.iren.SetInteractorStyle(style)
        self.iren.SetRenderWindow(self.widget.GetRenderWindow())

        colors = vtkNamedColors()
        self.ren.SetBackground(colors.GetColor3d('White'))
       
        self.show()
        self.iren.Initialize()

    def exit(self):
        QApplication.instance().quit()
        print("Window closed") 
    
    def loadModel(self):
        if hasattr(self, 'dataModel'):
            self.dataModel.hideModel(self.ren)
            self.dataModel.clear()

        fname = QFileDialog.getOpenFileName(self, 'Select pyFreeDyn database file', 
         'C:\\VIS_2024\\Aufgabe_3',"pyFreeDyn database file (*.json)")

        os.chdir(os.path.dirname(fname[0]))
        self.dataModel.loadDatabase(fname[0])

        self.dataModel.showModel(self.ren)
        self.status.showMessage("Model loaded and rendered")

        self.ren.ResetCamera()
    
    def saveModel(self):
        fname = QFileDialog.getSaveFileName(self, 'Select pyFreeDyn database file', 
         'C:\\VIS_2024\\Aufgabe_3',"pyFreeDyn database file (*.json)")

        os.chdir(os.path.dirname(fname[0]))
        self.dataModel.saveDatabase(fname[0])
        self.status.showMessage("Saved database")
    
    def importModel(self):
        if hasattr(self, 'dataModel'):
            self.dataModel.hideModel(self.ren)
            self.dataModel.clear()

        fname = QFileDialog.getOpenFileName(self, 'Select FreeDyn database file', 
         'C:\\VIS_2024\\Aufgabe_3',"FreeDyn database file (*.fdd)")

        os.chdir(os.path.dirname(fname[0]))
        self.dataModel.importFddFile(fname[0])

        self.dataModel.showModel(self.ren)
        self.status.showMessage("Model imported")

        self.ren.ResetCamera()

    def openSettingsDialog(self):
        text, ok = QInputDialog.getText(self, 'scale factor settings', 'type scale factor here')
        if ok:
            self.scaleFactor = float(text)
            if hasattr(self, 'dataModel'):
                for object in self.dataModel:
                    object.setScaleFactor(float(text))