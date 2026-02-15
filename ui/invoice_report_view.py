# ---------------- ui/invoice_report_view.py ----------------
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem, QInputDialog, QComboBox, QListView, QLabel, 
    QMessageBox, QTableWidget, QTableWidgetItem, QFrame, QDialog, QStyle, QHeaderView, QHBoxLayout, QApplication
)
from PyQt5.QtCore import Qt, QDate
from core.file_manager import TOBReportManager, D2SReportManager, CalendarManager
from utilities.stylesheets import StylingManager
from utilities.helpers import VerificationHelper
from utilities.utils import TobReportViewer
from utilities.utils import TobChecksViewer

class InvoiceReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        
        #Init Managers and Helpers
        self.styling_manager = StylingManager()
        self.tob_report_manager = TOBReportManager()
        self.d2s_report_manager = D2SReportManager()
        self.calender_manager = CalendarManager()
        self.verification_helper = VerificationHelper()

        #Init variables or data containers
        self.calender_data = self.calender_manager.get_all()
        self.tob_reports_data = self.tob_report_manager.get_all()
        self.d2s_reports_data = self.d2s_report_manager.get_all()
        
        #Central Layout VBOX (Central)
        central_layout = QVBoxLayout()
        
        #Parent TOB/D2S Layouts
        parent_layout = QHBoxLayout()

        #Child TOB/D2S Layouts
        child_tob_layout = QVBoxLayout()
        child_d2s_layout = QVBoxLayout()

        
        #Top Layout HBOX
        top_bar_layout = QHBoxLayout()
        
        #Item 1
        label = QLabel("Select Year : ")
        label.setFixedWidth(150)
        label.setStyleSheet(self.styling_manager.label_style())
        top_bar_layout.addWidget(label, alignment=Qt.AlignLeft)
        
        #Item 2
        self.year_selector = QComboBox() 
        self.year_selector.setFixedWidth(150)
        self.year_selector.setView(QListView())                
        self.year_selector.setObjectName("year_selector")
        self.year_selector.setAttribute(Qt.WA_StyledBackground, True)
        self.year_selector.setStyleSheet(self.styling_manager.selector_box_style("year_selector"))
        self.year_selector.view().setStyleSheet(self.styling_manager.selector_style())
        years = [str(y) for y in range(2026, 2031)]
        self.year_selector.addItems(years)
        currentYear = QDate().currentDate().year()
        self.year_selector.setCurrentText(str(currentYear))
        top_bar_layout.addWidget(self.year_selector)
        top_bar_layout.addStretch()
        
        #------------------TOB Report Section-----------------------#

        #TOB eader Label
        tob_label_window = QWidget()
        tob_label = QLabel("TOB Invoicing Reports")
        tob_label_layout = QVBoxLayout()     
        tob_label.setStyleSheet(self.styling_manager.header_label_style())
        tob_label_layout.addWidget(tob_label, alignment=Qt.AlignCenter)
        tob_label_window.setLayout(tob_label_layout)
        tob_label_window.setStyleSheet(self.styling_manager.header_label_style())

        #TOB Tree Widget
        self.tree_tob = QTreeWidget()
        self.tree_tob.setIndentation(0)
        self.tree_tob.setHeaderLabels(["Month", "Due Date", "Status", "Reports", "Checks"])
        self.tree_tob.setStyleSheet(self.styling_manager.header_style())
        
        #Bottom Layout HBOX (Button Bar)
        bottom_bar_layout_tob = QHBoxLayout()
        self.verify_btn_tob = QPushButton("Verify")
        self.generate_reports_btn_tob = QPushButton("Generate Report")
        self.verify_btn_tob.setStyleSheet(self.styling_manager.button_style())
        self.generate_reports_btn_tob.setStyleSheet(self.styling_manager.button_style())
        bottom_bar_layout_tob.addWidget(self.verify_btn_tob)
        bottom_bar_layout_tob.addWidget(self.generate_reports_btn_tob)
        
        #Add Widgets & Layout to TOB HBOX Layout
        child_tob_layout.addWidget(tob_label_window)
        child_tob_layout.addWidget(self.tree_tob)
        child_tob_layout.addLayout(bottom_bar_layout_tob)

        #------------------D2S Report Section-----------------------#

        #D2S Header Label
        d2s_label_window = QWidget()
        d2s_label = QLabel("D2S Invoicing Reports")
        d2s_label_layout = QVBoxLayout()     
        d2s_label.setStyleSheet(self.styling_manager.header_label_style())
        d2s_label_layout.addWidget(d2s_label, alignment=Qt.AlignCenter)
        d2s_label_window.setLayout(d2s_label_layout)
        d2s_label_window.setStyleSheet(self.styling_manager.header_label_style())

        #TOB Tree Widget
        self.tree_d2s = QTreeWidget()
        self.tree_d2s.setIndentation(0)
        self.tree_d2s.setHeaderLabels(["Month", "Due Date", "Status", "Reports", "Checks"])
        self.tree_d2s.setStyleSheet(self.styling_manager.header_style())
        
        #Bottom Layout HBOX (Button Bar)
        bottom_bar_layout_d2s = QHBoxLayout()
        self.verify_btn_d2s = QPushButton("Verify")
        self.generate_reports_btn_d2s = QPushButton("Generate Report")
        self.verify_btn_d2s.setStyleSheet(self.styling_manager.button_style())
        self.generate_reports_btn_d2s.setStyleSheet(self.styling_manager.button_style())
        bottom_bar_layout_d2s.addWidget(self.verify_btn_d2s)
        bottom_bar_layout_d2s.addWidget(self.generate_reports_btn_d2s)
        
        #Add Widgets & Layout to D2S HBOX Layout
        child_d2s_layout.addWidget(d2s_label_window)
        child_d2s_layout.addWidget(self.tree_d2s)
        child_d2s_layout.addLayout(bottom_bar_layout_d2s)
        
        #Add child layouts to parent D2S/TOB
        parent_layout.addLayout(child_tob_layout)
        parent_layout.addLayout(child_d2s_layout)

        #Add parent layout to central layout
        central_layout.addLayout(top_bar_layout)
        central_layout.addLayout(parent_layout)

        #Setting Layout
        self.setLayout(central_layout)
        
        #Load tree
        self.load_tree(org = 'tob')
        self.load_tree(org = 'd2s')

        #Connecting signals to slot
        self.verify_btn_tob.clicked.connect(lambda _, org = 'tob' : self.perform_verification(org))
        self.verify_btn_d2s.clicked.connect(lambda _, org = 'd2s' : self.perform_verification(org))
        self.tob_report_manager.tob_report_updated.connect(lambda *_, org = 'tob' : self.load_tree(org))
        
    def load_tree(self, org):
        selected_year = self.year_selector.currentText()
        
        if(org == 'tob'):    
            self.tree_tob.clear()
            self.tob_reports_data = self.tob_report_manager.get_all(year = selected_year)
            selected_year_data = self.tob_reports_data[selected_year]
            for month, month_details in selected_year_data.items():
                due_date = self.calender_data[selected_year][month][org]
                status = month_details['status']
                tree_item = QTreeWidgetItem([month, due_date, status, '', ''])

                self.tree_tob.addTopLevelItem(tree_item)

                # 🔍 Report Preview button
                preview_btn_tob = QPushButton()
                preview_btn_tob.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
                preview_btn_tob.setFlat(True)
                preview_btn_tob.clicked.connect(lambda _, year = selected_year, org = 'tob' : self.show_report(year, org))
                self.tree_tob.setItemWidget(tree_item, 3, preview_btn_tob)

                # 🔍 Checks Preview button
                checks_preview_btn_tob = QPushButton()
                checks_preview_btn_tob.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
                checks_preview_btn_tob.setFlat(True)
                checks_preview_btn_tob.clicked.connect(lambda _, year = selected_year, org = 'tob' : self.show_checks_report(year, org))
                self.tree_tob.setItemWidget(tree_item, 4, checks_preview_btn_tob)
        
        if(org == 'd2s'):
            self.tree_d2s.clear()
            self.d2s_reports_data = self.d2s_report_manager.get_all(year = selected_year)
            selected_year_data = self.d2s_reports_data[selected_year]
            for month, month_details in selected_year_data.items():
                due_date = self.calender_data[selected_year][month][org]
                status = month_details['status']
                tree_item = QTreeWidgetItem([month, due_date, status, ''])
                self.tree_d2s.addTopLevelItem(tree_item)

                # 🔍 Preview button
                preview_btn_d2s = QPushButton()
                preview_btn_d2s.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))
                preview_btn_d2s.setFlat(True)
                preview_btn_d2s.clicked.connect(lambda _, year = selected_year, org = 'd2s' : self.show_report(year, org))
                self.tree_d2s.setItemWidget(tree_item, 3, preview_btn_d2s)
        
    def perform_verification(self, org):
        if org == 'tob':
            selected_month = self.tree_tob.currentItem().text(0)
            selected_year = self.year_selector.currentText()
            final_status, checks_dict, report_dict = self.verification_helper.verify_tob_invoice(selected_month, selected_year)
            if not final_status:
                QMessageBox.information(self, "Aborting", "Folder structure in error\nPlease conform to the standard structure")
                return
            self.save_details(final_status, checks_dict, report_dict)
            checks_and_report_dict = self.verification_helper.merge_outputs(report_dict, checks_dict)            
            print(checks_and_report_dict)
            print(final_status)

            
    def save_details(self, status, checks_dict: dict, report_dict: dict):
        selected_year = self.year_selector.currentText()
        selected_month = self.tree_tob.currentItem().text(0)
        due_for_month_year = QDate.currentDate().addMonths(-1).toString("MMMM yyyy")
        self.tob_reports_data[selected_year][selected_month]["duefor"] = due_for_month_year
        if status == 'pass':
            self.tob_reports_data[selected_year][selected_month]["status"] = 'Successful'
        else:
            self.tob_reports_data[selected_year][selected_month]["status"] = 'Unsuccessful'
        
        for env, checks in checks_dict.items():
            self.tob_reports_data[selected_year][selected_month]["reports"][env]["checks"] = checks
        
        for env, report in report_dict.items():
            self.tob_reports_data[selected_year][selected_month]["reports"][env]["report"]["DT01"] = report["DT01"]
            self.tob_reports_data[selected_year][selected_month]["reports"][env]["report"]["DT27"] = report["DT27"]
            self.tob_reports_data[selected_year][selected_month]["reports"][env]["report"]["ChassisInvs"] = report["Principal Chassis Invoices"]
            self.tob_reports_data[selected_year][selected_month]["reports"][env]["report"]["RecycleInvs"] = report["Principal Recycle Invoices"]
            self.tob_reports_data[selected_year][selected_month]["reports"][env]["report"]["ChassisTaxInvs"] = report["Tax Invoices for Chassis Orders (Non Zero Amount)"]
            self.tob_reports_data[selected_year][selected_month]["reports"][env]["report"]["ChassisZeroInvs"] = report["Principal Chassis Invoices with Zero Amount"]
            self.tob_reports_data[selected_year][selected_month]["reports"][env]["report"]["EligibleChassisInvsForJV"] = report["Invoices Eligible for JV creation"]
            self.tob_reports_data[selected_year][selected_month]["reports"][env]["report"]["ChassisJVs"] = report["Count of Chassis JVs created"]
            self.tob_reports_data[selected_year][selected_month]["reports"][env]["report"]["RecycleJVs"] = report["Count of Recycle JVs created"]

        self.tob_report_manager.save_report_data()



    def show_report(self, selected_year, org):
        if org == 'tob':
            selected_month = self.tree_tob.currentItem().text(0)
            if(self.tob_reports_data[selected_year][selected_month]["status"] == "Verification Due"):
                QMessageBox.warning(self, "Verificaton Report", "No Reports to show!!\nVerification is still due....")
            else:
                self.load_tob_report_tree(selected_year, selected_month)
        
        if org == 'd2s':
            selected_month = self.tree_d2s.currentItem().text(0)
            if(self.d2s_reports_data[selected_year][selected_month]["status"] == "Verification Due"):
                QMessageBox.warning(self, "Verificaton Report", "No Reports to show!!\nVerification is still due....")
            else:
                self.load_d2s_report_tree(selected_year, selected_month)

    def load_tob_report_tree(self, selected_year, selected_month):
        monthly_report = self.tob_reports_data[selected_year][selected_month]['reports']
        tob_report_viewer = TobReportViewer(report = monthly_report)
        tob_report_viewer.exec_()

    def load_d2s_report_tree(self, selected_month):
        return

    def show_checks_report(self, selected_year, org):
        if org == 'tob':
            selected_month = self.tree_tob.currentItem().text(0)
            if(self.tob_reports_data[selected_year][selected_month]["status"] == "Verification Due"):
                QMessageBox.warning(self, "Validation Report", "No Reports to show!!\nVerification is still due....")
            else:
                self.load_tob_checks_tree(selected_year, selected_month)
        
        if org == 'd2s':
            selected_month = self.tree_d2s.currentItem().text(0)
            if(self.d2s_reports_data[selected_year][selected_month]["status"] == "Verification Due"):
                QMessageBox.warning(self, "Validation Report", "No Reports to show!!\nVerification is still due....")
            else:
                self.load_d2s_checks_report(selected_year, selected_month)

    def load_tob_checks_tree(self, selected_year, selected_month):
        #print(self.tob_reports_data[selected_year][selected_month])
        monthly_checks_report = self.tob_reports_data[selected_year][selected_month]['reports']
        tob_checks_viewer = TobChecksViewer(report = monthly_checks_report)
        tob_checks_viewer.exec_()