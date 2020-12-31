from trademark_xml_parser import parse_dir
from dbconnector import DBConnector
from ftplib import FTP_TLS
from os import listdir
from os.path import isdir

class DBFiller:
    '''
    This class can download trademark data from the online source and use it to 
    fill the database.
    '''
    def __init__(self, data_folder):
        self.dbc = DBConnector()
        self.dbc.connect()

        # Make sure there is a / at the end of path
        self.data_folder = data_folder
        if self.data_folder[-1:] != "/":
            self.data_folder += "/"

    def __del__(self):
        self.dbc.disconnect()

    def start_fdbf(self):
        ''' Start filling db from a given folder '''
        self.fill_db_by_folder(self.data_folder)

    def fill_db_by_folder(self, path):
        ''' 
        Use all the data in the folder to fill the database. 
        Search recursively.
        '''
        for entry in listdir(path):
            entrypath = path+"/"+entry
            print("fill_db_by_folder("+entrypath+")")
            if isdir(entrypath):
                if self.has_subdirs(entrypath):
                    self.fill_db_by_folder(entrypath)
                else:
                    # Only call parse_dir on folders without subdirs
                    # Those are the ones with data
                    # Tu sa deje vela veci, nejake exceptiony?
                    print("parse_dir("+entrypath+")")
                    trademarks = parse_dir(entrypath)
                    print("insert_many("+str(trademarks)+")")
                    self.dbc.insert_many(trademarks)
            else:
                raise DBFillerError("Unexpected file found in data folder."\
                        "Path:{}".format(entrypath))

    def get_2019_one_zip(self):
        ''' Download the first zip in 2019 folder from the data source '''
        pass

    def get_2019(self):
        ''' Download all the data in 2019 folder from the data source '''
        pass
    
    def get_trademarks_from_dir(self):
        pass
    
    def get_trademark_from_file(self):
        pass
    
    def download_2019_trademarks(self):
        ''' 
        Download the EUTMS files in 2019 folder from the data source via ftp
        '''
        ftp=FTP_TLS()
        ftp.connect("ftp.euipo.europa.eu", 21)
        ftp.sendcmd("USER opendata")
        ftp.sendcmd("PASS kagar1n")

        files = ("EUTMS_20201118_0001.zip", "EUTMS_20201118_0002.zip", 
                "EUTMS_20201118_0003.zip", "EUTMS_20201118_0004.zip", 
                "EUTMS_20201118_0005.zip", "EUTMS_20201118_0006.zip")

        ftp.cwd("/Trademark/Full/2019/")

        for f in files:
            with open("{}/{}".format(self.data_folder, f), "wb") as fp:
                print("Downloading {}".format(f))
                ftp.retrbinary("RETR {}".format(f), fp.write)
                print("Done.")

        ftp.quit()

    def has_subdirs(self, directory):
        ''' Return True if directory has subdiretories, else return False '''
        for entry in listdir(directory):
            if isdir(directory+"/"+entry): 
                return True

        return False

class DBFillerError(Exception):
    pass

if __name__ == "__main__":
    data_folder = "/home/sanko/test/web_apina/data"

    dbf = DBFiller(data_folder)
    #dbf.get_2019_one_zip()
    #dbf.start_fdbf(data_folder)
    dbf.download_2019_trademarks()

#catch ParseErrors
