from library import *
import func
import read
import split
import export
import plot

#Webpage Customization
st.set_page_config(layout="wide")

# Function to process each file in parallel (helper function)
def process_file(zf, file_name):
    """Helper function to process individual file inside the ZIP."""
    try:
        with zf.open(file_name) as file:
            # Read the content of the file as a DataFrame
            df = pd.read_csv(file)
            
            # Get the file size in bytes
            file_size = zf.getinfo(file_name).file_size
            
            # Return the DataFrame and file size
            return file_name, df, file_size
    except Exception as e:
        st.write(f"Error reading {file_name}: {e}")
        return file_name, None, None

# Refactored function to process ZIP files with parallelism
def process_zip(load_file):
    """Process the ZIP file and extract CSV/TXT data as DataFrames in parallel."""
    file_dataframes = {}
    file_sizes = {}

    # Open the ZIP archive
    with zipfile.ZipFile(io.BytesIO(load_file.read())) as zf:
        file_names = zf.namelist()

        # Filter files to only process .txt and .csv
        file_names_to_process = [file_name for file_name in file_names if file_name.endswith('.txt') or file_name.endswith('.csv')]

        # Use ThreadPoolExecutor to process each file in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Map the process_file function to each file and retrieve results
            results = executor.map(lambda file_name: process_file(zf, file_name), file_names_to_process)
        
        # Process results after parallel execution
        for file_name, df, file_size in results:
            if df is not None:
                file_dataframes[file_name] = df
                file_sizes[file_name] = file_size
                # st.write(f"Filename: {file_name}, Size: {file_size}")

    return file_dataframes, file_sizes


# Function to process and split the data (with filter2 applied after splitting)
def run(file_dataframes, file_sizes):
    # Step 1: Apply the first filter to the raw data (filter1)
    data_lib = read.run(file_dataframes, file_sizes, func.filter1)

    # Step 2: Split the telemetry data files after applying filter1
    zip_buffer = split.run(data_lib)  # Split the data after filter1
    # st.download_button(
    #     label="Download All CSVs as ZIP",
    #     data=zip_buffer,
    #     file_name="split_csvs.zip",
    #     mime="application/zip"
    # )
    
    return zip_buffer

@st.cache_data
def cache_final_data(final_data):
    """Caches the final processed data."""
    return final_data

    
# Steamlit Web version
def display_filtered_data(cached_data):
    files = list(cached_data.keys())
    telemetry_file = st.selectbox("Select files to view", files)

    tabs1, tabs2 = st.tabs(['Telemetry', 'Plot'])

    with tabs1:
        #Print out the dataframe of the telemetry they want to view
        st.dataframe(cached_data[telemetry_file])

    with tabs2:
        #User will select the graph they want to plot
        selection = st.selectbox("Select Plot", ['UAV vs Pri Baro', 'UAV vs Sec Baro', 'Pri Baro vs Sec Baro'])

        #After selection (plot the relevant graph selected)
        plot.run(cached_data[telemetry_file],selection,toggle=1)

        with st.spinner('Generating Report...'):
            excel_buffer = export.run(cached_data)
            # Provide the download button for the report
            st.download_button(
                label="Download Report",
                data=excel_buffer,
                file_name="report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.success("Report Generated")

        # # Button to generate altitude report
        # generate = st.button('Generate Report')

        # #Function to generate if the button is pressed
        # if generate:
        #     with st.spinner('Wait for it...'):
        #         #Generate report
        #         excel_buffer = export.run(cached_data)
        #         # Provide the download button for the report
        #         st.download_button(
        #             label="Download Report (Excel)",
        #             data=excel_buffer,
        #             file_name="report.xlsx",
        #             mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        #         )
        #         st.success("Report Generated")

def log_memory_usage(title):
    # Get the current memory usage (in MB)
    memory_info = psutil.virtual_memory()
    
    # Display human-readable memory usage information
    st.write(f"### {title} Memory Usage Information")
    st.write(f"**Total Memory:** {memory_info.total / (1024 * 1024):,.2f} MB")
    st.write(f"**Used Memory:** {memory_info.used / (1024 * 1024):,.2f} MB")
    st.write(f"**Available Memory:** {memory_info.available / (1024 * 1024):,.2f} MB")
    st.write(f"**Memory Usage (Percentage):** {memory_info.percent}%")
    
    # Provide context
    if memory_info.percent > 80:
        st.warning("⚠️ Memory usage is high! This could lead to slower performance or crashes.")
    elif memory_info.percent > 50:
        st.info("💡 Memory usage is moderate. Keep an eye on it.")
    else:
        st.success("✅ Memory usage is at a safe level.")


# Step 1: Upload the ZIP file of unprocessed data
uploaded_file = st.file_uploader("Upload a ZIP file containing text (CSV) files", type="zip")

# If a file is uploaded
if uploaded_file is not None:
    log_memory_usage("First Upload File")
    # Step 2: Process the uploaded ZIP to extract data and file sizes
    file_dataframes, file_sizes = process_zip(uploaded_file)
    # Step 3: Run filtering (filter1) and split the data
    second_uploaded_file = run(file_dataframes, file_sizes)
    # Log memory usage periodically
    log_memory_usage("Second Upload File")
    if second_uploaded_file is not None:
        second_filtered_data, second_file_sizes = process_zip(second_uploaded_file)
        second_filtered_data = {key[:15]: value for key, value in second_filtered_data.items()}
        second_file_sizes = {key[:15]: value for key, value in second_file_sizes.items()}
        # Log memory usage periodically
        st.write(f"Second filter data keys: {second_filtered_data.keys()}")
        # Step 2: Apply the second filter (filter2) to the split data
        final_data = read.run(second_filtered_data, second_file_sizes, func.filter2)

        if final_data is not None:
            # Cache the final data after processing
            cached_data = cache_final_data(final_data)
            # Log memory usage periodically
            log_memory_usage("Final Data")
            display_filtered_data(cached_data)
        else:
            st.write("No Final Data")
    else:
        st.write("No Split File")

else:
    st.write("No File Upload")

