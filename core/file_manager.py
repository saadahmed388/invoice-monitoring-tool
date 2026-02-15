from pathlib import Path
from PyQt5.QtCore import QObject, pyqtSignal, QDate
import json, os



class TOBReportManager(QObject):
    tob_report_updated = pyqtSignal() 
    def __init__(self):
        super().__init__()
        self.BASE_DIR = "data_and_config_files"
        self.base_path = Path(self.BASE_DIR)
        self.filepath = self.base_path/"tob_reports.json"
        self.base_path.mkdir(parents = True, exist_ok = True)
        self.report_data = self.load()

    def get_all(self, year = None):
        if year is not None and year not in self.report_data:
            self.report_data[year] = self.issue_template()
            self.save_report_data()
        return self.report_data

    def load(self):    
        if not Path(self.filepath).is_file():
            with open(self.filepath, "w"): 
                pass
        with open(self.filepath, "r") as f:
            if os.path.getsize(self.filepath) > 0:
                return json.load(f)
            else:
                return {}
        
    
    def issue_template(self):

        checks_template = {
            "c1" : "NA",
            "c2" : "NA",
            "c3" : "NA",
            "c4" : "NA"
        }

        report_template = {
            "DT01" : "NA",
            "DT27" : "NA",
            "ChassisInvs" : "NA",
            "ChassisTaxInvs" : "NA",
            "ChassisZeroInvs" : "NA",
            "ChassisJVs" : "NA",
            "RecycleInvs" : "NA",
            "RecycleJVs" : "NA"
        }
        
        checks_and_report = {
            "checks" : checks_template,
            "report" : report_template
        }

        env_list = {
            "Okayama" : checks_and_report,
            "Aomori" : checks_and_report,
            "Hakodate" : checks_and_report,
            "Iwate" : checks_and_report,
            "Shikoku" : checks_and_report,
            "Okinawa" : checks_and_report,
            "Wakayama" : checks_and_report,
            "Chugoku" : checks_and_report
        }
        
        month_details = {
            "duefor" : "",
            "status" : "Verification Due", 
            "timestamp" : "NA",                           
            "reports" : env_list
        }
        
        months = {
            "January" : month_details,
            "February" : month_details,
            "March" : month_details,
            "April" : month_details,
            "May" : month_details,
            "June" : month_details,
            "July" : month_details,
            "August" : month_details,
            "September" : month_details,
            "October" : month_details,
            "November" : month_details,
            "December" : month_details
        }

        return months

    def get_cur_year(self):
        return QDate().currentDate().year()
        
    def save_report_data(self):
        with open(self.filepath, "w") as f:
            json.dump(self.report_data, f, indent=4)
        self.tob_report_updated.emit()
                    
class D2SReportManager(QObject): 
    d2s_report_updated = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.BASE_DIR = "data_and_config_files"
        self.base_path = Path(self.BASE_DIR)
        self.base_path.mkdir(parents = True, exist_ok = True)
        self.filepath = (self.base_path/"d2s_reports.json")
        self.report_data = self.load()

    def get_all(self, year = None):
        if year is not None and year not in self.report_data:
            self.report_data[year] = self.issue_template()
            self.save_report_data()
        return self.report_data

    def load(self):    
        if not Path(self.filepath).is_file():
            with open(self.filepath, "w"): 
                pass
        with open(self.filepath, "r") as f:
            if os.path.getsize(self.filepath) > 0: 
                return json.load(f)
            else:
                return {}
        
    def issue_template(self):

        report_template = {
                            "DT01" : "NA",
                            "DT27" : "NA",
                            "ChassisInvs" : "NA",
                            "ChassisTaxInvs" : "NA",
                            "ChassisZeroInvs" : "NA",
                            "ChassisJVs" : "NA",
                            "RecycleInvs" : "NA",
                            "RecycleJVs" : "NA"
                          }

        env_list = {
                        "Okayama" : report_template,
                        "Aomori" : report_template,
                        "Hakodate" : report_template,
                        "Iwate" : report_template,
                        "Shikoku" : report_template,
                        "Okinawa" : report_template,
                        "Wakayama" : report_template,
                        "Chugoku" : report_template
                   }
        
        month_details = {
                            "duefor" : "",
                            "status" : "Verification Due", 
                            "timestamp" : "NA",                           
                            "report" : env_list
                        }
        
        months = {
                    "January" : month_details,
                    "February" : month_details,
                    "March" : month_details,
                    "April" : month_details,
                    "May" : month_details,
                    "June" : month_details,
                    "July" : month_details,
                    "August" : month_details,
                    "September" : month_details,
                    "October" : month_details,
                    "November" : month_details,
                    "December" : month_details
                }
        
        return months

    def get_cur_year(self):
        return QDate().currentDate().year()    
        
    def save_report_data(self):
        with open(self.filepath, "w") as f:
            json.dump(self.report_data, f, indent=4)
        self.d2s_report_updated.emit()            
        
class CalendarManager(QObject):
    calendar_updated = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.BASE_DIR = "data_and_config_files"
        self.base_path = Path(self.BASE_DIR)        
        self.filepath = Path(self.BASE_DIR)/"calendar.json"
        self.calendar_data = self.load()
    
    def get_all(self):
        return self.calendar_data

    def get_year(self, year):
        if year not in self.calendar_data:
            self.calendar_data[year] = self.issue_template()
            self.save_calendar()
        return self.calendar_data[year]

    def load(self):    
        if not Path(self.filepath).is_file():
            with open(self.filepath, "w"): 
                pass
        with open(self.filepath, "r") as f:
            if os.path.getsize(self.filepath) > 0:
                return json.load(f)
            else:
                return {}
    
    def issue_template(self):
        tob_d2s_due = {
                "tob" : "NA",
                "d2s" : "NA"
        }
        calendar_template = {
            "January" : tob_d2s_due,
            "February" : tob_d2s_due,
            "March": tob_d2s_due,
            "April": tob_d2s_due,
            "May" : tob_d2s_due,
            "June"  : tob_d2s_due,
            "July" : tob_d2s_due,
            "August" : tob_d2s_due,
            "September" : tob_d2s_due,
            "October" : tob_d2s_due,
            "November" : tob_d2s_due,
            "December" : tob_d2s_due
        }
        return calendar_template
    
    def get_cur_year(self):
        return QDate().currentDate().year()

    def save_calendar(self, org_signal = None):
        with open(self.filepath, "w") as write_calendar_file:
            json.dump(self.calendar_data, write_calendar_file, indent=4)
        self.calendar_updated.emit(org_signal)
        