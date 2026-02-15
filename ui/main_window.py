from PyQt5.QtWidgets import QMainWindow, QTabWidget, QMessageBox
from PyQt5.QtGui import QIcon
from core.db_client import DBClient

#-----Importing managers------"
from core.db_config_manager import DBConfigManager
from core.query_manager import QueryManager
from core.file_manager import TOBReportManager
from core.file_manager import CalendarManager
from utilities.stylesheets import StylingManager

#-----Importing Tab Views------"
from ui.connections_view import ConnectionsTab
from ui.queries_view import QueriesTab
from ui.invoice_report_view import InvoiceReportsTab
from ui.calendar_view import CalenderTab

class MainWindow(QMainWindow):
    def __init__(self):
        #-------Parent Initialization--------#
        super().__init__()
        
        #-------Window Initialization--------#
        self.setWindowTitle("Invoice Verification")
        self.setWindowIcon(QIcon("Assets/invoice.png"))
        self.resize(1600, 800)
        
        #-------Empty Variable Initialization--------#
        self.db_clients = {}
        
        #-------Managers--------#
        self.tob_report_manager = TOBReportManager()
        self.db_config_manager = DBConfigManager()
        self.styling_manager = StylingManager()
        self.query_manager = QueryManager()
        self.calendar_manager = CalendarManager()
        
        #-------Tabs--------#
        self.connections_tab = ConnectionsTab(self.db_clients)
        self.queries_tab = QueriesTab()
        self.invoice_reports_tab = InvoiceReportsTab()
        self.calendar_tab = CalenderTab()
       
        #-------Tab Widget Initialization--------#
        tabs = QTabWidget()
        
        #-------Adding tabs to the widget--------#
        tabs.addTab(self.connections_tab, "Connections")
        tabs.addTab(self.queries_tab, "Queries")
        tabs.addTab(self.invoice_reports_tab, "Invoice Reports")
        tabs.addTab(self.calendar_tab, "Calendar")
        
        #-------Setting Tab stylsheet--------#
        tabs.setStyleSheet(self.styling_manager.tab_style())
        
        #-------Setting Tab as Central Widget (One Central Widget per window)--------#
        self.setCentralWidget(tabs)
        
        
        
        