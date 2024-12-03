from library import *
import func

def run(data,arg,toggle):
    fig = go.Figure()

    # Determine the plot size based on the argument
    width, height = (1500, 750)

    # Adding lines for the selected case
    if arg == "UAV vs Pri Baro":
        fig.add_trace(go.Scatter(x=data['Mission Time'], y=data['UAV Altitude'], mode='lines', name='UAV', line=dict(color="#0436A9")))
        fig.add_trace(go.Scatter(x=data['Mission Time'], y=data['Baro Altitude'], mode='lines', name='Pri Baro', line=dict(color="#04A777")))
        offset = func.calculate_error(data, 'UAV Altitude', 'Baro Altitude', 1)
        fig.add_trace(go.Scatter(x=data['Mission Time'], y=[3.5] * len(data['Mission Time']),
                        mode='lines', line=dict(color="yellow", dash="dash"),
                        name="Warning (m) To monitor"))
        fig.add_trace(go.Scatter(x=data['Mission Time'], y=[6.5] * len(data['Mission Time']),
                        mode='lines', line=dict(color="orange", dash="dash"),
                        name="Warning (m) Bring back for maintenance"))
        fig.add_trace(go.Scatter(x=data['Mission Time'], y=[13] * len(data['Mission Time']),
                        mode='lines', line=dict(color="orange", dash="dash"),
                        name="IMU Baro Failure"))            
    elif arg == "UAV vs Sec Baro":
        fig.add_trace(go.Scatter(x=data['Mission Time'], y=data['UAV Altitude'], mode='lines', name='UAV',line=dict(color="#234BFB")))
        fig.add_trace(go.Scatter(x=data['Mission Time'], y=data['Sec Baro Altitude'], mode='lines', name='Sec Baro',line=dict(color="#FB8B24")))
        offset = func.calculate_error(data, 'UAV Altitude', 'Sec Baro Altitude', 0)
        fig.add_trace(go.Scatter(x=data['Mission Time'], y=[3.5] * len(data['Mission Time']),
                        mode='lines', line=dict(color="yellow", dash="dash"),
                        name="Warning (m) To monitor"))
        fig.add_trace(go.Scatter(x=data['Mission Time'], y=[6.5] * len(data['Mission Time']),
                        mode='lines', line=dict(color="orange", dash="dash"),
                        name="Warning (m) Bring back for maintenance"))
        fig.add_trace(go.Scatter(x=data['Mission Time'], y=[13] * len(data['Mission Time']),
                        mode='lines', line=dict(color="orange", dash="dash"),
                        name="IMU Baro Failure"))    
    elif arg == "Pri Baro vs Sec Baro":
        fig.add_trace(go.Scatter(x=data['Mission Time'], y=data['Baro Altitude'], mode='lines', name='Pri Baro',line=dict(color="#04A777")))
        fig.add_trace(go.Scatter(x=data['Mission Time'], y=data['Sec Baro Altitude'], mode='lines', name='Sec Baro',line=dict(color="#FB8B24")))
        offset = func.calculate_error(data, 'Baro Altitude', 'Sec Baro Altitude', -1)
        fig.add_trace(go.Scatter(x=data['Mission Time'], y=[10] * len(data['Mission Time']),
                            mode='lines', line=dict(color="red", dash="dash"),
                            name="Cross-check Warning (10m)"))
        fig.add_trace(go.Scatter(x=data['Mission Time'], y=[20] * len(data['Mission Time']),
                            mode='lines', line=dict(color="red", dash="dash"),
                            name="Cross-check Fail (20m)"))
    
    threshold = 3.5
    threshold2= 6.5
    threshold3 = 10
    threshold4 = 13
    threshold5 = 20
    threshold6 = 8.5
    
    # Add the offset line
    #fig.add_trace(go.Scatter(x=Converted_data['Mission Time'], y=offset, mode='lines', name='Error',line=dict(color="#D90368")))
    # if (data['UAV ID'].astype(str).str.contains('15', regex=True).all()):
    #     fig.add_trace(go.Scatter(x=data['Mission Time'], y=[5] * len(data['Mission Time']),
    #                         mode='lines', line=dict(color="yellow", dash="dash"),
    #                         name="DrN-L Max Threshold (5m)"))
    #     fig.add_trace(go.Scatter(x=data['Mission Time'], y=[10] * len(data['Mission Time']),
    #                         mode='lines', line=dict(color="orange", dash="dash"),
    #                         name="Cross-check Warning (10m)"))
    #     fig.add_trace(go.Scatter(x=data['Mission Time'], y=[20] * len(data['Mission Time']),
    #                         mode='lines', line=dict(color="red", dash="dash"),
    #                         name="Cross-check Fail (20m)"))
    #     threshold = 5
    #     threshold2= 10
    #     threshold3 = 20
    # else:
    #     fig.add_trace(go.Scatter(x=data['Mission Time'], y=[3.5] * len(data['Mission Time']),
    #                         mode='lines', line=dict(color="yellow", dash="dash"),
    #                         name="DrN-DH/DrN-DL Max Threshold (3.5m)"))
    #     fig.add_trace(go.Scatter(x=data['Mission Time'], y=[6.5] * len(data['Mission Time']),
    #                         mode='lines', line=dict(color="orange", dash="dash"),
    #                         name="Cross-check Warning (6.5m)"))
    #     fig.add_trace(go.Scatter(x=data['Mission Time'], y=[13] * len(data['Mission Time']),
    #                         mode='lines', line=dict(color="red", dash="dash"),
    #                         name="Cross-check Fail (20m)"))
    #     fig.add_trace(go.Scatter(x=data['Mission Time'], y=[10] * len(data['Mission Time']),
    #                         mode='lines', line=dict(color="red", dash="dash"),
    #                         name="Cross-check Warning (10m)"))
    #     fig.add_trace(go.Scatter(x=data['Mission Time'], y=[20] * len(data['Mission Time']),
    #                         mode='lines', line=dict(color="red", dash="dash"),
    #                         name="Cross-check Fail (20m)"))
    #     threshold = 3.5
    #     threshold2= 10
    #     threshold3 = 6.5
    #     threhold4 = 13
    #     threshold3 = 20
        
    # Split the data into segments based on the threshold
    x_below, y_below = [], []
    x_above, y_above = [], []
    x_below2, y_below2 = [], []
    x_above2, y_above2 = [], []
    x_below3, y_below3 = [], []
    x_above3, y_above3 = [], []
    x_below4, y_below4 = [], []
    x_above4, y_above4 = [], []
    x_below5, y_below5 = [], []
    x_above5, y_above5 = [], []
    x_below6, y_below6 = [], []
    x_above6, y_above6 = [], []


    status = 0
    #If above 3.5m
    for i in range(len(data['Mission Time'])):
        if offset[i] <= threshold:
            x_below.append(data['Mission Time'][i])
            y_below.append(offset[i]) 
        else:
            x_above.append(data['Mission Time'][i])
            y_above.append(offset[i])
            status = 10
    #If above 6.5m      
    for i in range(len(data['Mission Time'])):
        if offset[i] <= threshold2:
            x_below2.append(data['Mission Time'][i])
            y_below2.append(offset[i]) 
        else:
            x_above2.append(data['Mission Time'][i])
            y_above2.append(offset[i])
            status = 11
    #If above 10m 
    for i in range(len(data['Mission Time'])):
        if offset[i] <= threshold3:
            x_below3.append(data['Mission Time'][i])
            y_below3.append(offset[i]) 
        else:
            x_above3.append(data['Mission Time'][i])
            y_above3.append(offset[i])
            status = 111

    #If above 13m       
    for i in range(len(data['Mission Time'])):
        if offset[i] <= threshold4:
            x_below4.append(data['Mission Time'][i])
            y_below4.append(offset[i]) 
        else:
            x_above4.append(data['Mission Time'][i])
            y_above4.append(offset[i])
            status = 1111
    
    #If above 20m       
    for i in range(len(data['Mission Time'])):
        if offset[i] <= threshold5:
            x_below5.append(data['Mission Time'][i])
            y_below5.append(offset[i]) 
        else:
            x_above5.append(data['Mission Time'][i])
            y_above5.append(offset[i])
            status = 11111

    #If above 8.5m       
    for i in range(len(data['Mission Time'])):
        if offset[i] <= threshold5:
            x_below6.append(data['Mission Time'][i])
            y_below6.append(offset[i]) 
        else:
            x_above6.append(data['Mission Time'][i])
            y_above6.append(offset[i])
            status = 111111

    # Add below-threshold trace (3.5)
    fig.add_trace(go.Scatter(x=x_below, y=y_below, mode='lines', name='Error Below Threshold (3.5m)', line=dict(color='green')))

    # Add above-threshold trace (above 3.5)
    fig.add_trace(go.Scatter(x=x_above, y=y_above, mode='markers', name='Error Above Threshold (3.5m) (To Monitor)', line=dict(color='yellow')))

    # Add above-threshold trace (6.5)
    fig.add_trace(go.Scatter(x=x_above2, y=y_above2, mode='markers', name='Error Above Threshold (6.5m) (Bring back for maintenance)', line=dict(color='orange')))

    # Add below-threshold trace (13)
    fig.add_trace(go.Scatter(x=x_below3, y=y_below3, mode='lines', name='IMU Baro Fail Threshold (13m)', line=dict(color='red')))

    # Add below-threshold trace (8.5)
    fig.add_trace(go.Scatter(x=x_below6, y=y_below6, mode='lines', name='Error Below Threshold (8.5m)', line=dict(color='green')))

    # Add above-threshold trace (8.5)
    fig.add_trace(go.Scatter(x=x_above6, y=y_above6, mode='lines', name='Error Above Threshold (8.5m) (To Monitor)', line=dict(color='yellow')))

    # Add above-threshold trace (10m)
    fig.add_trace(go.Scatter(x=x_above4, y=y_above4, mode='markers', name='Error above Cross-check Fail Threshold', line=dict(color='orange')))

    # Add above-threshold trace (20m)
    fig.add_trace(go.Scatter(x=x_above5, y=y_above5, mode='markers', name='Cross-check Fail', line=dict(color='red')))



    if toggle == 1:
        # Display the figure in Streamlit
        st.plotly_chart(fig)

    else: 
        return fig,status
   