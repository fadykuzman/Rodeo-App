"""
    This class searches for data in a hierarchy of folders and sorts
    them in a list.
    Attributes to the data are:
        path: path to the raw data file           
        type: whether from Picarro, DropSense sensors.
        data: the data set after reading with the modules:
            read_dropsense
            read_picarro
                Please refer to the documentation of the above data 
                reading modules to know the data structure of the
                resultant datasets
"""
import os
from collections import namedtuple
import skansensor.skansensor as ss
class DataCollector:
    dir_list = []
    
    def __init__(self):
        pass
        
        
    def get_files(self, path = '.'):
        """
           Loops through a folder hierarchy from a given path.
           If no path is given, it searches through the current
           directory.
           The method returns a namedtuple of:
               path, kind of file/folder, and if a file, the extension
           
           Parameters:
           -------------
           path: path to the parent directory to loop through. 
                 Default is current directory
           
           returns:
           -------------
           dir_list: a list of all files or folders as a namedtuple.
                     Attributes of the namedtuple are:
                     path: path to file or folder
                     whatis: dir or data
                     whatext: what extension the data file has.
                              (only dropsense and picarro)
        """  
        # Opens an instance of a directory
        with os.scandir(path) as it:
        # loop through all items in a directory
            for entry in it:
                cat = namedtuple('cat', ['path', 'whatis', 'whatext'])
            
                if entry.is_dir():
                    cat.path = entry.path
                    cat.whatis = 'dir'
                    self.dir_list.append(cat)
                    self.get_files(cat.path)
                
                else:
                    filename, fileext = os.path.splitext(entry.path)
                    if (
                        (fileext == '.mta') 
                        or (fileext == '.mtc') 
                        or (fileext == '.mtzc')
                        ):
                        cat.path = entry.path
                        cat.whatis = 'data'
                        cat.whatext = fileext
                        self.dir_list.append(cat)
                        
                    elif fileext == '.dat':
                        cat.path = entry.path
                        cat.whatis = 'data'
                        cat.whatext = fileext
                        self.dir_list.append(cat)
                    else:
                        pass
                
        return self.dir_list
    
    def collect(self, dir_list):
        """
        Parameters:
        ------------
        dir_list: the list of files and folders.
                  Expected the result of the method get_files()

        returns:
        ------------
        data_list: a list of dictionaries that contain data read
                   from data files.
                   Refer to 'skansensor' module for the data structure.
        """
        datalist = []
        for a in dir_list:
            if a.whatis == 'data':
                if (a.whatext == '.mta') or (a.whatext == '.mtc') or (a.whatext == '.mtzc'):
                    d = {
                        'path' : a.path,
                        'type' : 'dropsense',
                        'data' : ss.read_dropsense(a.path)
                        }
                elif a.whatext == '.dat':
                    d = {
                        'path' : a.path,
                        'type' : 'picarro',
                        'data' : ss.read_picarro(a.path)
                        }
                if d not in datalist:
                    datalist.append(d)
        return datalist
