#Function to color code the dataframe cells
def highlight(s, column_name):
    if column_name == 'Recommendation':
        return ['background-color: #FFB6B3' if x == 'Service Maintenance' else 'background-color: #BDE78D' for x in s]
    
    elif column_name in ['Sorties To Replacement', 'Add Sorties To Replacement']:
        return [
            'background-color: #FBCA62' if isinstance(x, int) and x < 10 else #If the sorties is getting close to 0 
            '' if isinstance(x, str) else
            '' for x in s
        ]