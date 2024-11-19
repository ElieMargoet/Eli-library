import nuke
import os
import sys
import math
import re
from PySide2 import QtCore, QtUiTools, QtWidgets, QtGui


class mytool(QtWidgets.QWidget):
    def __init__(self):
        #define and load UI
        super(mytool,self).__init__()
        scriptpath = "C:/Users/Elie/.nuke/ElieStockshot.ui"
        self.ui = QtUiTools.QUiLoader().load(scriptpath, parentWidget=self)

        #fit UI in QBoxLayout
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.ui)
        self.setLayout(mainLayout)

        #Set window to stay on top of nuke and set its title
        label = self.setWindowTitle('Eli-brary')

        self.ui.btn_explore.clicked.connect(self.btnexplore)
        self.ui.btn_import.clicked.connect(self.btnimport)

        global slider
        global percent
        global sbox 

        slider = self.ui.slider
        percent = self.ui.percent
        sbox = self.ui.sbox_amount

        sbox.valueChanged.connect(self.ui_update)
        slider.valueChanged.connect(self.ui_update)

        self.ui_update()

    def btnexplore(self):
        path = self.ui.lineE_path.text()
        mysel = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder", path, QtWidgets.QFileDialog.ShowDirsOnly)
        self.ui.lineE_path.setText(mysel)

        self.ui_update()

    def ui_update(self):

        mult = slider.value()*0.01
        maxColumn = sbox.value()

        path = self.ui.lineE_path.text()
        jpg =[]
        for f in os.listdir(path):
            full_path = os.path.join(path, f)
            if os.path.isdir(full_path):
                jpg.append(f)

        amount = len(jpg)
        column = maxColumn
        row = math.ceil(amount/column)

        self.ui.tbl_stockshot.setRowCount(row)
        self.ui.tbl_stockshot.setColumnCount(column)

        count = 0
        for x in jpg:
            row = int(count / column)
            col = count % column
            item = QtWidgets.QTableWidgetItem()

            # Set icon for the item
            folder_path = os.path.join(path, x)
            image_files = [f for f in os.listdir(folder_path) if re.match(rf"{x}_\d+\.jpg", f)]
            if image_files:
                image_files.sort()
                last_frame = int(re.search(rf"{x}_(\d+)\.jpg", image_files[-1]).group(1))
                last_frame_offset = last_frame - 40
                icon_path = os.path.join(folder_path, f"{x}_{last_frame_offset}.jpg")
                if os.path.exists(icon_path):
                    icon = QtGui.QIcon(icon_path)
                    item.setIcon(icon)
                    # set icon size
                    sizex,sizey = 1080*mult, 512*mult
                    size = QtCore.QSize(sizex, sizey)
                    self.ui.tbl_stockshot.setIconSize(size)
                else:
                    item.setText(x)

            item.setData(QtCore.Qt.UserRole, x)

            header = self.ui.tbl_stockshot.horizontalHeader()
            header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
            header = self.ui.tbl_stockshot.verticalHeader()
            header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

            self.ui.tbl_stockshot.setItem(row, col, item)
            count +=1
           

    def btnimport(self):
        items = self.ui.tbl_stockshot.selectedItems()
        path = self.ui.lineE_path.text()


        for i in items:
            folder_name= i.data(QtCore.Qt.UserRole)
            folder_path = os.path.join(path, folder_name)

            sequence_path = os.path.join(f"{path}/{folder_name}/{folder_name}_####.jpg")
            image_files = [f for f in os.listdir(folder_path) if re.match(rf"{folder_name}_\d+\.jpg", f)]


            if os.path.exists(os.path.join(path, folder_name)):

                # Trier les fichiers pour obtenir le premier et le dernier
                image_files.sort()
                first_frame = int(re.search(rf"{folder_name}_(\d+)\.jpg", image_files[0]).group(1))
                last_frame = int(re.search(rf"{folder_name}_(\d+)\.jpg", image_files[-1]).group(1))

                read = nuke.nodes.Read(file=sequence_path)
                read['first'].setValue(first_frame)
                read['last'].setValue(last_frame)

            else: 
                QtWidgets.QMessageBox.warning(self, "Erreur", f"Le dossier '{folder_name}' ne contient pas de séquence d'images valide.")

        
        
#define global window, try to close it if already open. Then show  window
def open_mytool():
    global win
    try:
        win.close()
    except:
        pass
    win = mytool()
    win.show()

