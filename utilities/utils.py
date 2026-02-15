from PyQt5.QtWidgets import (
                            QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, 
                            QComboBox, QListView, QTreeWidget, QMessageBox, QTreeWidgetItem,
                            QStyle, QCalendarWidget
)
from utilities.stylesheets import StylingManager
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from utilities.stylesheets import StylingManager

class StyledInputDialog(QDialog):
    def __init__(self, title, label, caps = "N", default_text = ""):
        super().__init__()
        self.styling_manager = StylingManager()
        self.setWindowTitle(title)
        self.resize(400, 150)
        self.setStyleSheet(self.styling_manager.dialog_style())   
        self.caps = caps

        layout = QVBoxLayout(self)
        self.label = QLabel(label)

        self.input = QLineEdit()
        self.input.setText(default_text)
        self.input.setPlaceholderText("Type here...")
        layout.addWidget(self.label)
        layout.addWidget(self.input)

        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def get_text(self):
        self.result = self.exec_()
        text = self.input.text().strip()
        if self.caps.upper() == "Y":
            text = text.upper()
        return text, self.result == QDialog.Accepted


class CheckableComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setView(QListView())
        self.setModel(QStandardItemModel(self))
        self.checked = []
        self.styling_manager = StylingManager()
        self.setObjectName("export_configs_selector")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(self.styling_manager.selector_box_style("export_configs_selector"))
        self.view().setStyleSheet(self.styling_manager.selector_style())
        self.view().pressed.connect(self.handleItemPressed)

    def addCheckItems(self, all_presets, checked_presets):
        for text in all_presets:
            item = QStandardItem(text)
            item.setFlags((item.flags() | Qt.ItemIsUserCheckable) & ~Qt.ItemIsTristate)            
            item.setData(Qt.Unchecked, Qt.CheckStateRole)
            if text in checked_presets:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.model().appendRow(item)

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        item.setFlags((item.flags() | Qt.ItemIsUserCheckable) & ~Qt.ItemIsTristate)
        if item.checkState():
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
        self.updateText()

    def updateText(self):
        self.checked = []
        for i in range(self.model().rowCount()):
            item = self.model().item(i)
            if item.checkState():
                self.checked.append(item.text())
        self.setEditText(", ".join(self.checked))
        
    def getChecked(self):
        return self.checked


class TreePopUp(QDialog):
    def __init__(self, selected_config, styling_manager, history_manager, log_viewer, selected_sr = None):
        super().__init__()
        self.styling_manager = styling_manager
        self.history_manager = history_manager
        self.setWindowTitle("Service Request Logs")
        self.resize(600, 300)
        self.setStyleSheet(self.styling_manager.dialog_style())
        self.config_name = selected_config
        self.sr_num = selected_sr
        self.log_viewer = log_viewer 
        
        layout = QVBoxLayout()
       
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["SR#", "Date of Export", "Log"])
        self.tree.setColumnWidth(0, 100)
        self.tree.setColumnWidth(1, 150)
        self.tree.setIndentation(0)
        self.tree.setStyleSheet(self.styling_manager.header_style())
        layout.addWidget(self.tree)
        self.setLayout(layout)
        
        self.load_tree()
        
    def load_tree(self):
        
        self.tree.clear()
        self.history = self.history_manager.get_all_history()
        if not self.sr_num:
            config_history  = [h for h in self.history if h["config"] == self.config_name]
        else:
            print(self.sr_num)
            config_history  = [h for h in self.history if h["sr_num"] == self.sr_num]
        
        if config_history:
            for items in config_history:
                config_name = items.get("config", "")
                sr_num = items.get("sr_num", "")
                date_of_export = items.get("date_extracted", "")
                export_log = items.get("extraction_log", "")
                                            
                item = QTreeWidgetItem([sr_num, date_of_export, ''])
                self.tree.addTopLevelItem(item)
                
                log_preview_btn = QPushButton()
                log_preview_btn.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
                log_preview_btn.setFlat(True)
                log_preview_btn.clicked.connect(lambda _, e_log = export_log : self.show_log(e_log))
                
                self.tree.setItemWidget(item, 2, log_preview_btn)
                
            self.exec_()
            
        else:
            QMessageBox.information(self, "Export Logs", "No Service Request registered for this configuration")
               
    def show_log(self, export_log):
        print("Showing")
        self.log_viewer(self.styling_manager, export_log).exec_()    
            
class TobReportViewer(QDialog):
    def __init__(self, list_col :list = ["Environment", "DT01", "Chassis Invs Created", "Chassis Invs (Taxes)", "Chassis Invs (Zero Amt)", "Chassis JVs Created", "DT27" ,"Recycle Invs Created", "Recycle JVs Created"], report: dict = None):
        super().__init__()
        self.setWindowTitle("TOB Invoicing Report")
        self.resize(1400,500)
        self.styling_manager = StylingManager()
        
        layout = QVBoxLayout()
        
        self.tree = QTreeWidget()
        self.tree.setIndentation(0)
        self.tree.setHeaderLabels(list_col)
        self.tree.setStyleSheet(self.styling_manager.header_style())
        
        if report:
            for env, dets in report.items():
                #print(env, dets)
                item = QTreeWidgetItem([str(env), str(dets['report']['DT01']), str(dets['report']['ChassisInvs']), str(dets['report']['ChassisTaxInvs']), str(dets['report']['ChassisZeroInvs']), str(dets['report']['ChassisJVs']), str(dets['report']['RecycleInvs']), str(dets['report']['RecycleInvs']), str(dets['report']['RecycleJVs'])])
                self.tree.addTopLevelItem(item)
                
        self.tree.expandAll()
        layout.addWidget(self.tree)
        self.setLayout(layout)

class TobChecksViewer(QDialog):
    def __init__(self, list_col :list = ["Checks", "Okayama", "Aomori", "Hakodate", "Iwate", "Shikoku", "Okinawa" ,"Wakayama", "Chugoku"], report: dict = None):
        super().__init__()
        self.setWindowTitle("TOB Invoicing Validations Report")
        self.resize(1600,300)
        self.styling_manager = StylingManager()
        
        layout = QVBoxLayout()
        
        self.tree = QTreeWidget()
        self.tree.setIndentation(0)
        self.tree.setHeaderLabels(list_col)
        self.tree.setStyleSheet(self.styling_manager.header_style())
        self.tick_mark_path = ''
        if report:
            for i in range(4):
                if i == 0:
                    item_list = ["Chassis Invoices created = Records in DT01"]
                    for env, dets in report.items():
                        item_list.append(dets['checks']['c1'])
                    self.tree.addTopLevelItem(QTreeWidgetItem(item_list))
                if i == 1:
                    item_list = ["Recycle Invoices created = Records in DT27"]
                    for env, dets in report.items():
                        item_list.append(dets['checks']['c2'])
                    self.tree.addTopLevelItem(QTreeWidgetItem(item_list))
                if i == 2:
                    item_list = ["Chassis JVs created = Invs + Tax - 0"]
                    for env, dets in report.items():
                        item_list.append(dets['checks']['c3'])
                    self.tree.addTopLevelItem(QTreeWidgetItem(item_list))
                if i == 3:
                    item_list = ["Recycle JVs created = 3 * Recycle Invs"]
                    for env, dets in report.items():
                        item_list.append(dets['checks']['c4'])
                    self.tree.addTopLevelItem(QTreeWidgetItem(item_list))
        
        self.tree.resizeColumnToContents(0)        
        self.tree.expandAll()
        layout.addWidget(self.tree)
        self.setLayout(layout)

class ShowCalendar(QDialog):
    def __init__(self, styling_manager):
        super().__init__()
        self.resize(400,400)
        self.setWindowTitle("Calendar")
        self.styling_manager = styling_manager

        #Layout
        central_layout = QVBoxLayout()
        button_bar_layout = QHBoxLayout()

        #Buttons & Widgets
        self.cal_widget = QCalendarWidget()
        self.cal_widget.setGridVisible(True)
        self.ok_btn = QPushButton('OK')
        self.ok_btn.setStyleSheet(self.styling_manager.button_style())
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setStyleSheet(self.styling_manager.button_style())
        self.cancel_btn.clicked.connect(self.reject)

        button_bar_layout.addWidget(self.ok_btn)
        button_bar_layout.addWidget(self.cancel_btn)

        #Add to layout
        central_layout.addWidget(self.cal_widget)
        central_layout.addLayout(button_bar_layout)
        self.setLayout(central_layout)

    def access_cal_widget(self):
        return self.cal_widget

    def get_selected_date(self):
        return self.cal_widget.selectedDate()



        
    