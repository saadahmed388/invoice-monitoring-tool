# ---------------- ui/calendar_view.py ----------------
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QTreeWidget, QTreeWidgetItem, QInputDialog, QComboBox, QListView, QLabel, 
    QMessageBox, QTableWidget, QTableWidgetItem, QFrame, QDialog, QStyle, QHeaderView, QHBoxLayout, QApplication, QCalendarWidget, QSizePolicy
)
from PyQt5.QtCore import Qt, QDate
from utilities.utils import ShowCalendar
from core.file_manager import CalendarManager
from utilities.stylesheets import StylingManager

class CalenderTab(QWidget):
    def __init__(self):
        super().__init__()
        
        #init variables
        self.date_obj = QDate()
        self.size_policy = QSizePolicy()
        
        #init managers
        self.styling_manager = StylingManager()
        self.calendar_manager = CalendarManager()

        #init utils
        self.show_calendar = ShowCalendar(self.styling_manager)
        
        #Layout Boxes
        parent_layout = QVBoxLayout() #Parent layout (Central)
        top_bar_layout = QHBoxLayout() #Top Bar Layout (Housing date or combo selectors)
        cal_box_layout = QHBoxLayout() #Middle Layout (It will house both TOB and D2S calendars side by side
        tob_cal_layout = QVBoxLayout() #For TOB Cal
        d2s_cal_layout = QVBoxLayout() #For D2S Cal
  
        #Item 1
        today = self.date_obj.currentDate()
        label_current_date = QLabel(f"Date Today: {today.toString()}")
        label_current_date.setStyleSheet(self.styling_manager.label_style())
        label_current_year = QLabel(f"Ongoing Year : {str(today.year())}")
        label_current_year.setStyleSheet(self.styling_manager.label_style())
        top_bar_layout.addWidget(label_current_date, alignment=Qt.AlignLeft)
        top_bar_layout.addWidget(label_current_year, alignment=Qt.AlignLeft)

             
        #-------------------TOB Cal Layout---------------------#
        
        #Header Label
        tob_label_window = QWidget()
        tob_label = QLabel("TOB Verification Due Dates")
        tob_label_layout = QVBoxLayout()     
        tob_label.setStyleSheet(self.styling_manager.header_label_style())
        tob_label_layout.addWidget(tob_label, alignment=Qt.AlignCenter)
        tob_label_window.setLayout(tob_label_layout)
        tob_label_window.setStyleSheet(self.styling_manager.header_label_style())

        ##Tree
        self.tree_tob = QTreeWidget()
        self.tree_tob.setIndentation(0)
        self.tree_tob.setHeaderLabels(["Month", "Due Date"])
        self.tree_tob.setStyleSheet(self.styling_manager.header_style())

        ##Bottom Layout HBOX (Button Bar)
        bottom_bar_layout_tob = QHBoxLayout()
        self.edit_due_btn_tob = QPushButton("Edit Due Date")
        self.reset_due_btn_tob = QPushButton("Reset Date")
        self.reset_due_btn_tob.setFixedWidth(100)
        self.edit_due_btn_tob.clicked.connect(lambda _, org = 'tob' : self.show_cal(org))
        self.reset_due_btn_tob.clicked.connect(lambda _, org = 'tob' : self.reset_due(org))
        self.edit_due_btn_tob.setStyleSheet(self.styling_manager.button_style())
        self.reset_due_btn_tob.setStyleSheet(self.styling_manager.button_style())
        bottom_bar_layout_tob.addWidget(self.edit_due_btn_tob)
        bottom_bar_layout_tob.addWidget(self.reset_due_btn_tob)

        ##Add to TOB Cal Layout
        tob_cal_layout.addWidget(tob_label_window)
        tob_cal_layout.addWidget(self.tree_tob)
        tob_cal_layout.addLayout(bottom_bar_layout_tob)
        

        #-------------------D2S Cal Layout---------------------#
        
        #Header Label
        d2s_label_window = QWidget()
        d2s_label = QLabel("D2S Verification Due Dates")
        d2s_label_layout = QVBoxLayout()     
        d2s_label.setStyleSheet(self.styling_manager.header_label_style())
        d2s_label_layout.addWidget(d2s_label, alignment=Qt.AlignCenter)
        d2s_label_window.setLayout(d2s_label_layout)
        d2s_label_window.setStyleSheet(self.styling_manager.header_label_style())

        #Tree
        self.tree_d2s = QTreeWidget()
        self.tree_d2s.setIndentation(0)
        self.tree_d2s.setHeaderLabels(["Month", "Due Date"])
        self.tree_d2s.setStyleSheet(self.styling_manager.header_style())

        #Bottom Layout HBOX (Button Bar)
        bottom_bar_layout_d2s = QHBoxLayout()
        self.edit_due_btn_d2s = QPushButton("Edit Due Date")
        self.reset_due_btn_tob = QPushButton("Reset Date")
        self.reset_due_btn_tob.setFixedWidth(100)
        self.edit_due_btn_d2s.clicked.connect(lambda _, org = 'd2s' : self.show_cal(org))
        self.reset_due_btn_tob.clicked.connect(lambda _, org = 'd2s' : self.reset_due(org))
        self.edit_due_btn_d2s.setStyleSheet(self.styling_manager.button_style())
        self.reset_due_btn_tob.setStyleSheet(self.styling_manager.button_style())
        bottom_bar_layout_d2s.addWidget(self.edit_due_btn_d2s)
        bottom_bar_layout_d2s.addWidget(self.reset_due_btn_tob)

        #Add to D2S Cal Layout
        d2s_cal_layout.addWidget(d2s_label_window)
        d2s_cal_layout.addWidget(self.tree_d2s)
        d2s_cal_layout.addLayout(bottom_bar_layout_d2s)

        #Add to Calender Box Layout
        cal_box_layout.addLayout(tob_cal_layout)
        cal_box_layout.addLayout(d2s_cal_layout)

        #Add to parent
        parent_layout.addLayout(top_bar_layout)
        parent_layout.addLayout(cal_box_layout)

        #Setting Layout
        self.setLayout(parent_layout)

        #Load Calender data
        self.calendar_data = self.calendar_manager.get_all()
        self.current_year = self.calendar_manager.get_cur_year()
 
        #Load tree
        self.load_tree(str(self.current_year), 'tob')
        self.load_tree(str(self.current_year), 'd2s')

        #Connect signals to slots
        self.calendar_manager.calendar_updated.connect(self.load_on_signal)
    
    #ReLoad tree on signal definition
    def load_on_signal(self, org_signal):
        if org_signal == 'tob':
            self.load_tree(str(self.current_year), 'tob')
        if org_signal == 'd2s':
            self.load_tree(str(self.current_year), 'd2s')
        if not org_signal:
            self.load_tree(str(self.current_year), 'tob')
            self.load_tree(str(self.current_year), 'd2s')

    #Load tree definition
    def load_tree(self, year, org):
        if org == 'tob':
            self.tree_tob.clear()
        else:
            self.tree_d2s.clear()

        calendar_year_data = self.calendar_data[str(year)]
        for month, org_item in calendar_year_data.items():
            if org == 'tob':
                due_date = org_item['tob']
                calender_item = QTreeWidgetItem([month, due_date])
                self.tree_tob.addTopLevelItem(calender_item)
            else:
                due_date = org_item['d2s']
                calender_item = QTreeWidgetItem([month, due_date])
                self.tree_d2s.addTopLevelItem(calender_item)

    #Edit due button
    def show_cal(self, org):

        if (not self.tree_tob.currentItem() and org =='tob') or (not self.tree_d2s.currentItem() and org=='d2s'):
            QMessageBox.warning(self, "Warning!!", "Select a month to proceed")
            return
        
        if org == 'tob':
            current_month = self.tree_tob.currentItem().text(0)
        else:
            current_month = self.tree_d2s.currentItem().text(0)
        
        self.show_calendar.access_cal_widget().setCurrentPage(self.current_year, self.get_month_num(current_month))
        
        if self.show_calendar.exec_() == QDialog.Accepted:
            selected_date = self.show_calendar.get_selected_date()
            self.edit_due(org, selected_date)

    def edit_due(self, org, selected_date):
        if org == 'tob':
            month_selected = self.tree_tob.currentItem().text(0)
            self.calendar_data[str(self.current_year)][month_selected]['tob'] = selected_date.toString()
        else:
            month_selected = self.tree_d2s.currentItem().text(0)
            self.calendar_data[str(self.current_year)][month_selected]['d2s'] = selected_date.toString()
        self.calendar_manager.save_calendar(org_signal=org)

     #Rest Due function
    def reset_due(self, org):
        if org == 'tob':
            month_selected = self.tree_tob.currentItem().text(0)
            self.calendar_data[str(self.current_year)][month_selected]['tob'] = "NA"
        else:
            month_selected = self.tree_d2s.currentItem().text(0)
            self.calendar_data[str(self.current_year)][month_selected]['d2s'] = "NA"
        self.calendar_manager.save_calendar(org_signal=org)
        return

    def get_month_num(self, month):
        month_dict = {
            "January" : 1,
            "February" : 2,
            "March" : 3,
            "April" : 4,
            "May" : 5,
            "June" : 6,
            "July" : 7,
            "August" : 8,
            "September" : 9,
            "October" : 10,
            "November" : 11,
            "December" : 12
        }
        return month_dict[month]
        