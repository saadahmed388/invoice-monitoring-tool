from PyQt5.QtWidgets import QMessageBox
from core.db_client import DBClient
from core.db_config_manager import DBConfigManager
from core.query_manager import QueryManager
from pathlib import Path
import regex as re
from collections import defaultdict
from PyQt5.QtCore import QDate

class VerificationHelper():
    def __init__(self, raw_folder_path = 'reports/TOB/Raw Invoice Data', reports_folder_path = 'reports/TOB/Reports'):
        self.raw_folder_path = Path(raw_folder_path)
        self.reports_folder_path = Path(reports_folder_path)
        self.raw_folder_path.mkdir(parents=True, exist_ok=True)
        self.reports_folder_path.mkdir(parents=True, exist_ok=True)
        self.connection_helper = ConnectionHelper()
        self.db_clients = self.connection_helper.get_db_clients()
        self.query_manager = QueryManager()
    
    def get_outputs(self, org: str, file: Path):
        if org == 'tob':
            db_outputs = self.get_db_counts('tob')
        else:
            db_outputs = self.get_db_counts('d2s')
        file_outputs = self.get_file_outputs(file)
        merged_outputs = self.merge_outputs(db_outputs, file_outputs)
        return merged_outputs
   
    def get_all_queries(self):
        return self.query_manager.get_all_queries()

    def verify_tob_invoice(self, month, year):  
        found_flag = False 
        try:
            prev_month = self.get_prev_month(month, year)
            for f in self.raw_folder_path.iterdir():
                print(f.stem)
                if f.stem.lower() == str(prev_month).lower():
                    found_flag = True
                    self.tob_folder_structure_check(f)
                    outputs = self.get_outputs('tob', f)
                    counts_check_dict = self.invoice_jv_counts_check(outputs)
                    over_all_ver_stat = self.over_all_verification_check(counts_check_dict)
            if not found_flag:    
                raise FolderStructureError((f"Data for month : {prev_month} not found!!!"))
            print(f"Verification Status : {over_all_ver_stat}")
            return over_all_ver_stat, counts_check_dict, outputs
        except FolderStructureError as e:
            print(str(e))
            print("Aborting execution")
            return  "", {}, {}
        

    def get_file_outputs(self, folder_path: Path):
        file_outputs_all = {}
        for f in folder_path.iterdir():
            file_outputs_env = {}
            for c in f.iterdir():
                if c.stem.startswith('DT01'):
                    with open(c, "r") as dt01_file:
                        file_outputs_env['DT01'] = len(dt01_file.readlines())
                if c.stem.startswith('DT27'):
                    with open(c, "r") as dt27_file:
                        file_outputs_env['DT27'] = len(dt27_file.readlines())
            file_outputs_all[f.stem] = file_outputs_env
        return file_outputs_all

    def get_db_counts(self, org):
        queries = self.get_all_queries()
        db_outputs_all = {}
        if org == 'tob':             
            tob_queries = [q for q in queries if q['class'] == str(org).upper()]            
            for d in self.db_clients:
                db_outputs_env = {}
                for q in tob_queries:
                    db_outputs_env[q['name']] = self.db_clients[d].execute_select(q['sql'])[0][0][0]
                db_outputs_all[d] = db_outputs_env
        return db_outputs_all

    def merge_outputs(self, a : dict, b : dict):
        c = {}
        for k, v in a.items():
            c[k] = v | b[k]
        return c

    def compare_counts(self, a: str, b: str, c: dict, f1 = 1, f2 = 1):
        if f1*c[a] == f2*c[b]:
            return "pass"
        else: 
            return "fail"
    
    def get_prev_month(self, mon, year):
        months_dict = self.get_months_dict()
        date_set = QDate(int(year), months_dict[mon], 1)
        prev_month = date_set.addMonths(-1).toString("MMMM")
        return prev_month
    
    def get_months_dict(self):
        return  {
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
            "Decemebr" : 12    
        }

    def invoice_jv_counts_check(self, data: dict):
        checks_dict_all = {}
        for env, details in data.items():
            checks_dict_env = {}
            #Check1 : Number of Pricinpal Chassis Invoices created is same as count in DT01 file
            checks_dict_env["c1"] = self.compare_counts("Principal Chassis Invoices", "DT01", details)
            #Check2 : Number of Principal Recycle Invoice created is same as count in DT27 file
            checks_dict_env["c2"] = self.compare_counts("Principal Recycle Invoices", "DT27", details)
            #Check3 : Invoices Eligible for JV Created is same as count of JVs created in the environment
            checks_dict_env["c3"] = self.compare_counts("Invoices Eligible for JV creation", "Count of Chassis JVs created", details)
            #Check4 : Number of Recycle JVs created is exactly 3 times the number of records in DT27 file
            checks_dict_env["c4"] = self.compare_counts("DT27", "Count of Recycle JVs created", details, f1=3)
            checks_dict_all[env] = checks_dict_env
        return checks_dict_all

    def over_all_verification_check(self, data: dict[str, dict]):
        for k, v in data.items():
            for k_a, v_a in v.items():
                if v_a == 'fail':
                    return 'fail'
        return 'pass'

    
    def tob_folder_structure_check(self, folder_path: Path):
        try:
            self.parent_folders_check(folder_path)
            self.tob_missing_files_check(folder_path)
        except FolderStructureError as e:
            print(str(e))
            print("Aborting execution")
            return
    
    def parent_folders_check(self, folder_path: Path):
        env_set = {"Okayama", "Aomori", "Hakodate", "Iwate", "Shikoku", "Okinawa", "Wakayama", "Chugoku"}
        for f in folder_path.iterdir():
            env_set.discard(f.stem)
        if len(env_set)>0:
            missing_env = ", ".join(env for env in env_set)
            raise FolderStructureError(
                (f"Missing data for environments : {missing_env}")
            )

    def tob_missing_files_check(self, folder_path: Path):
        
        missing_files_dir = defaultdict(list)
        
        for f in folder_path.iterdir():
            files_set = {'DT01', 'DT27'}
            for c in f.iterdir():
                if c.stem.startswith('DT01'):
                    files_set.discard('DT01')
                if c.stem.startswith('DT27'):
                    files_set.discard('DT27')
            if files_set:
                for file in files_set:
                    missing_files_dir[f.stem].append(file)

        if not missing_files_dir:
            print("Folder structure verified.......Proceeding with Invoice Verification\n")
        else:
            msg = ["Listed files are missing for the mentioned environments:-"]
            for k, v in missing_files_dir.items():
                msg.append(f"Env: {k} | Files: {" ".join(v)}")
            raise FolderStructureError(
                '\n'.join(msg)
            )  
                    
class ConnectionHelper():
    def __init__(self):
        self.db_config_manager = DBConfigManager()
        self.connections = self.db_config_manager.get_all_connections()
        self.db_clients = {}
        self.connect_all()
    
    def connect_all(self):

        for c in self.connections:
            con_name = c["name"]
            connection = DBClient(
                user=c["user"],
                password=c["password"],
                dsn=c["dsn"]
            )
            try:
                connection.connect()
                
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Connection Failed",
                    f"{con_name} connection failed:\n{str(e)}"
                )
            self.db_clients[con_name] = connection
        
    def get_db_clients(self):
        return self.db_clients
    
class FolderStructureError(Exception):
    pass

class CountMismatchError(Exception):
    pass