from library import *

#Function to convert int to 8bit for Status 1
def bit_converter(data):
    # Ensure the number is within the 8-bit range (0 to 255 for unsigned 8-bit)
    for n in range(len(data)):
        data['Status 1'].iloc[n] = format(data['Status 1'].iloc[n], '08b')[5]
    return data

#Function to compare the filename 
def compare(filename1, filename2):
    def get_prefix_from_filename(filename):
        parts = filename.split('_')
        return f"{parts[0]}_{parts[1][:3]}" if len(parts) >= 2 else None
    return get_prefix_from_filename(filename1) == get_prefix_from_filename(filename2)

# Function to calculate the error between two altitude columns
def calculate_error(data, column1, column2,Option):
    if Option == 1:
        error = data['UAV_baro error'].iloc[0]
        return abs((abs(np.subtract(data[column1],data[column2]))) - error)
    elif Option == 0:
        error = data['UAV_secbaro error'].iloc[0]
        return abs((abs(np.subtract(data[column1],data[column2]))) - error)
    else:
        error = data['Baro error'].iloc[0]
        return abs((abs(np.subtract(data[column1],data[column2]))) - error)
    

    
# Function to filter the data based on unique UAV Altitude values
def filter1(data):
    return data if data['UAV Altitude'].nunique() > 1 else None

def filter2(data):
    #Convert the status1 into bit and extract the 5th bit
    data = bit_converter(data)

    #Check if the first value of the data is '1' or '0': if 1 -> remove
    #Remove all the data that only has 1 value in status 1
    if ((data['Status 1'].iloc[0] == '1') | (data['Status 1'].nunique() == 1)):
        pass 
    else:
        data = data.loc[data['Status 1'] == '1']
        temp_time = data['Mission Time'].iloc[0]
        data['Baro error'] = abs(abs((data.loc[data['Mission Time'] == temp_time][['Sec Baro Altitude','Baro Altitude']].iloc[0])[0]) - abs((data.loc[data['Mission Time'] == temp_time][['Sec Baro Altitude','Baro Altitude']].iloc[0])[1])) #baro offset
        data['UAV_baro error'] = abs(abs((data.loc[data['Mission Time'] == temp_time][['UAV Altitude','Baro Altitude']].iloc[0])[0]) - abs((data.loc[data['Mission Time'] == temp_time][['UAV Altitude','Baro Altitude']].iloc[0])[1])) #uav baro offset
        data['UAV_secbaro error'] = abs(abs((data.loc[data['Mission Time'] == temp_time][['UAV Altitude','Sec Baro Altitude']].iloc[0])[0]) - abs((data.loc[data['Mission Time'] == temp_time][['UAV Altitude','Sec Baro Altitude']].iloc[0])[1])) # uav sec baro offset
        data = data.loc[data['Flight Mode'] == 3]
        data = data.reset_index(drop=True)
        data = data[500:len(data)-100]
        data = data.reset_index(drop=True)
        return data
    

