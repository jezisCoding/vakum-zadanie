from trademark_xml_parser import parse_dir
from dbconnector import DBConnector
from ftplib import FTP_TLS
from os import listdir, remove, rmdir, getcwd, mkdir
from os.path import isdir
from shutil import rmtree
from zipfile import ZipFile
from time import sleep

class DBFiller:
    '''
    This class can download trademark data from the online source and use it to 
    fill the database.
    '''
    def __init__(self):
        self.dbc = DBConnector()
        if not self.dbc.connect():
            raise Exception("Cant connect to database.")

        self.data_folder = getcwd() + "/data/"
        # Make sure there is a / at the end of path
        mkdir(self.data_folder)
        if self.data_folder[-1:] != "/":
            self.data_folder += "/"

    def __del__(self):
        self.dbc.disconnect()

    def start_fdbf(self):
        ''' 
        Start filling db from a given folder.
        Remove the folder afterwards.
        '''
        print("Start filling the database", flush=True)
        self.fill_db_by_folder(self.data_folder)
        print("Done filling the database", flush=True)

        for f in listdir(self.data_folder):
            fpath = "{}/{}".format(self.data_folder, f)
            rmtree(fpath)

    def fill_db_by_folder(self, path):
        ''' 
        Use all the data in the folder to fill the database. 
        Search recursively.
        '''
        for entry in listdir(path):
            entrypath = path+"/"+entry
            # print("fill_db_by_folder("+entrypath+")", flush=True)
            if isdir(entrypath):
                if self.has_subdirs(entrypath):
                    self.fill_db_by_folder(entrypath)
                else:
                    # Only call parse_dir on folders without subdirs
                    # Those are the ones with data
                    # print("parse_dir("+entrypath+")")
                    trademarks = parse_dir(entrypath)
                    # print("insert_many("+str(trademarks)+")")
                    self.dbc.insert_many(trademarks)
            else:
                raise DBFillerError("Unexpected file found in data folder."\
                        "Path:{}".format(entrypath))

    def download_2019_trademarks(self):
        ''' 
        Download the EUTMS files in 2019 folder from the data source via ftp
        '''
        ftp=FTP_TLS()
        ftp.connect("ftp.euipo.europa.eu", 21)
        ftp.sendcmd("USER opendata")
        ftp.sendcmd("PASS kagar1n")

        print("Connected to FTP", flush=True)

        ftp.cwd("/Trademark/Full/2019/")

        files = ("EUTMS_20201118_0001.zip", "EUTMS_20201118_0002.zip", 
                "EUTMS_20201118_0003.zip", "EUTMS_20201118_0004.zip", 
                "EUTMS_20201118_0005.zip", "EUTMS_20201118_0006.zip")

        for f in files:
            fpath = "{}/{}".format(self.data_folder, f)
            with open(fpath, "wb") as fp:
                print("Downloading {}".format(f), flush=True)
                ftp.retrbinary("RETR {}".format(f), fp.write)
                print("Done.", flush=True)
        '''
        # Download only one zip, for debugging
        f = "EUTMS_20201118_0001.zip"
        fpath = "{}/{}".format(self.data_folder, f)
        with open(fpath, "wb") as fp:
            print("Downloading {}".format(f), flush=True)
            ftp.retrbinary("RETR {}".format(f), fp.write)
        '''

        ftp.quit()

    def unzip_data_folder(self):
        ''' Unzip each file and then remove it '''
        for z in listdir(self.data_folder):
            zpath = "{}/{}".format(self.data_folder, z)
            with ZipFile(zpath, 'r') as zip_ref:
                zip_ref.extractall(zpath[0:-4])
                print("Extractiong into " + zpath[0:-4], flush=True)
                remove(zpath)

    def get_2019(self):
        ''' Download 2019 data, unzip it and put it into the database '''
        self.download_2019_trademarks()
        self.unzip_data_folder()
        self.start_fdbf()
    
    def has_subdirs(self, directory):
        ''' Return True if directory has subdiretories, else return False '''
        for entry in listdir(directory):
            if isdir(directory+"/"+entry): 
                return True

        return False

class DBFillerError(Exception):
    pass

if __name__ == "__main__":
    print("Waiting for docker compose to start up the db", flush=True)
    sleep(20)
    dbf = DBFiller()
    dbf.get_2019()
