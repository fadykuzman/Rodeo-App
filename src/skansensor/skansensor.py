import pandas as pd
from xml.dom import minidom
import numpy as np

def read_rodeo(path):
    """
        Reads data produced from iorodeo as text file.
        Produces a 2 Column (time, data) DataFrame as well as exporting
        it as Excel sheet

        Parameters:
        -------------
        path: the path to the .TXT file produced by rodeo

        returns:
        -------------
        df: pandas DataFrame with time and data in two columns
        Excel file with the time and data in two columns

        Example:
        ------------
        data = skansensor.read_rodeo(
                                 './data_20180701/AD-020718_01-SP.TXT'
                                    )
    """
    names = ['time', 'P' ,'data']                           # Specify the headers to the 3 columns in
                                                            # .TXT file
    df = pd.read_csv(path, names=names)                     # read data from .TXT file into a pandas
                                                            # DataFrame and assign the column names
                                                            # To each column
    df = df.drop('P', axis = 1)                             # Drop the P column
    
    filename, fileext = os.path.splitext(path)              # Clean the file name
    df.to_excel('{}.xlsx'.format(filename), index =False)   # Export the Excel file into the same path
    return df

def read_dropsense(path):
    """
        Reads data from .MTA file and organizes it into a dataframe
        with only the time and ampere values
        
        Parameters:
        --------------
        path: the path to the .MTA file
        
        returns:
        --------------
        df: pandas DataFrame with time and ampere values in two columns

        Example:
        --------------
        data = skansensor.read_dropsense('./data_20180628/dritte_Messung.mta')    
    """
    
    xmldoc = minidom.parse(path)                         # Parse the MTA (as XML) file
    itemlist = xmldoc.getElementsByTagName('points')     # Get the Elements in 'points' Tag
    last_item = len(itemlist)-1
    timetag = itemlist[last_item].getElementsByTagName('time')   # Get the elements in 'time' Tag
    timepoints = timetag[0].childNodes[0].data           # Get the time data as a string and 
                                                         # assign them to timepoints variable
    time = timepoints.split(',')                         # Split the string on the comma
    time = list(map(float, time))                        # Convert values to float
    
    datatag = itemlist[last_item].getElementsByTagName('i1')     # Get the elements from 'i1' Tag 
                                                         # since that's where the data point reside
    datapoints = datatag[0].childNodes[0].data           # Get the ampere values as a string and 
                                                         # assign them to datapoints variable
    data = datapoints.split(',')                         # Split the string on the comma
    data = list(map(float, data))                        # Convert values to float
    data = list(map(abs, data))                          # Get the absolute values, since this is the correct 
                                                         # representation
    
    df_dict = {
        'time': time,
        'data_mamp': data
    }
    
    df = pd.DataFrame(df_dict)
    return df


def read_picarro(path):
    """ 
        Reads data from .dat file and organizes it into a dataframe
        with all values in the file but returns only time and H2O2 values
        
        Parameters:
        --------------
        path: the path to the .dat file
        
        returns:
        --------------
        d_time_ho: pandas DataFrame with time and ampere values in two columns

        Example:
        -------------
        data = skansensor.read_picarro('./data_20180608/erstemessung.dat')
    """
    df = pd.read_fwf(path)
    time1 = df['TIME']
    time1 = pd.to_datetime(time1)
    td = []

    for i in range(time1.shape[0]):
        td.append(time1.iloc[i]-time1.iloc[0])
    td_s = list(map(lambda x: x.seconds, td))
    df['time'] = td_s
    df = df[['time','H2O2']]
    return df


def fit(base_df, df_to_filter, t0 = 500, t1 = 2000):
    """
	fits two pandas DataFrames to have the same length and time
        intervals.

	Parameters:
	---------------
	base_df: pandas DataFrame on which to be filtered upon
		 The dataframe has the length and the needed time
                 interval
	
        df_to_filter: pandas DataFrame to be filtered.
        
        t0: the start time to truncate the values. Default = 500s

        t1: the snd time to truncate the values. Default = 2000s

	returns:
	---------------
	df: a pandas DataFrame compromises of the two DataFrames;
            base and To-be-filtered

        Example:
        ---------------
        deta_fitted = skansensor.fit(data_picarro, data_dropsense)
    """
    dropsense_filtered = []

    # Calculate the max and min time in the data set
    time_piccaro = list(base_df['time'])
    time_min_ds = df_to_filter['time'].min()
    time_max_ds = df_to_filter['time'].max()

    # loop through the dataset and assign only the data that have corresponding
    # time values to a new dataset
    for t in  np.arange(time_min_ds, time_max_ds):
        if t in time_piccaro:
            dropsense_filtered.append(
                float(df_to_filter['data_mamp'][df_to_filter['time'] == t])
                                     )

    # make a new dictionary out of the new data
    df_dict = {
        'time': time_piccaro,
        'data_dropsense': dropsense_filtered,
        'data_picarro': base_df['H2O2']
    }

    df = pd.DataFrame(df_dict)

    # truncate graph to get the proper maximas
    df = df[(df['time'] >= t0) & (df['time'] <= t1)]
    
    df = df.reset_index()
   
    # get the times where the values of each graph is maximum and calculate the distance
    # between the values 
    tmax_ds = df['time'][df['data_dropsense'] == df['data_dropsense'].max()]
    tmax_p = df['time'][df['data_picarro'] == df['data_picarro'].max()]
    t_diff = int(tmax_ds) - int(tmax_p)
    df_len = len(df[df['time'] <= df.loc[0, 'time']-t_diff])
    
    #shift the dropsense values the calculated length -2 to fit to the first point of
    # picarro graph. tested on data 1811
    df['data_dropsense'] = df.data_dropsense.shift(df_len-2)

    return df
