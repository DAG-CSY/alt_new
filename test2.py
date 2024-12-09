from library import *
import func
import read
import split
import export
import plot

# Function to process uploaded ZIP file
def process_zip(uploaded_zip):
    # Initialize dictionaries
    file_data = {}
    file_sizes = {}

    # Read the ZIP file
    with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
        # Loop over each file in the ZIP archive
        for file_name in zip_ref.namelist():
            # Get file size
            file_sizes[file_name] = zip_ref.getinfo(file_name).file_size

            # Read the file content based on its extension
            with zip_ref.open(file_name) as file:
                # For CSV files
                if file_name.endswith('.csv'):
                    df = pd.read_csv(file)
                # For TXT files (assuming they are tabular and can be read as CSV)
                elif file_name.endswith('.txt'):
                    df = pd.read_csv(file, delimiter="\t")  # assuming tab-delimited
                else:
                    continue

                # Add the dataframe to the dictionary
                file_data[file_name] = df

    return file_data, file_sizes

# Function to save the data into HDF5 (in /mnt/data/)
def save_to_hdf5(file_data, file_sizes):
    # Path for saving the HDF5 file
    hdf5_file_path = '/mnt/data/processed_files.h5'
    
    # Create the HDF5 file
    try:
        with h5py.File(hdf5_file_path, 'w') as hdf:
            # Store DataFrames as datasets
            for file_name, df in file_data.items():
                hdf.create_dataset(file_name, data=df.values)
            
            # Store file sizes in a group
            size_group = hdf.create_group('file_sizes')
            for file_name, size in file_sizes.items():
                size_group.create_dataset(file_name, data=size)
    except Exception as e:
        st.error(f"An error occurred while saving the file: {e}")
        return None

    return hdf5_file_path

# Function to read the HDF5 file and convert the datasets into DataFrames
def read_hdf5_to_dataframe(hdf5_file_path):
    # Open the HDF5 file
    with h5py.File(hdf5_file_path, 'r') as hdf:
        # Create a dictionary to hold DataFrames
        file_data = {}
        
        # Iterate through the datasets in the HDF5 file
        for file_name in hdf.keys():
            # Skip the 'file_sizes' group
            if file_name == 'file_sizes':
                continue
            
            # Read the dataset and convert it to a Pandas DataFrame
            df = pd.DataFrame(hdf[file_name][:])
            file_data[file_name] = df
        
        # Optionally, also read file sizes
        file_sizes = {}
        if 'file_sizes' in hdf:
            size_group = hdf['file_sizes']
            for file_name in size_group.keys():
                file_sizes[file_name] = size_group[file_name][()]
        
        return file_data, file_sizes

# Example filter function to process the DataFrames further
def filter_dataframes(file_data):
    filtered_data = {}
    for file_name, df in file_data.items():
        # Apply a filter to each DataFrame (example: remove rows where any column is NaN)
        filtered_data[file_name] = df.dropna()
    
    return filtered_data

# Streamlit UI for file upload
st.title("Process ZIP File")
uploaded_zip = st.file_uploader("Upload a ZIP file", type="zip")

if uploaded_zip is not None:
    # Process the ZIP file
    file_data, file_sizes = process_zip(uploaded_zip)


    # Save to HDF5 in the /mnt/data/ directory and provide download link
    hdf5_file = save_to_hdf5(file_data, file_sizes)
    
    if hdf5_file:
        st.download_button("Download HDF5 File", data=open(hdf5_file, "rb"), file_name="processed_files.h5")

    # Once the file is downloaded, you can read it back and apply filters
    st.write("### Filter Processed Data")

    # Read the HDF5 file back into DataFrames
    file_data_from_hdf5, file_sizes_from_hdf5 = read_hdf5_to_dataframe(hdf5_file)

    # Display processed data (e.g., first 5 rows of each dataframe)
    for file_name, df in file_data_from_hdf5.items():
        st.write(f"### {file_name}")
        st.write(df.head())

    # Display file sizes
    st.write("### File Sizes")
    st.write(file_sizes)
