from library import *

def run(data):
    # Create a ZIP file in memory to store all CSV files
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Define the allowed range for the difference
        for files in data:
            allowed_range = 100

            # List to store the split dataframes
            split_dfs = []
            start_idx = 0

            # Loop through the dataframe, checking the difference between consecutive rows
            for i in range(len(data[files]) - 1):
                current_value = data[files]['Mission Time'].iloc[i]
                next_value = data[files]['Mission Time'].iloc[i + 1]

                if abs(current_value - next_value) > allowed_range:
                    # If the difference is larger than allowed, split the dataframe
                    split_dfs.append(data[files].iloc[start_idx:i + 1])
                    start_idx = i + 1

            # Append the last segment
            split_dfs.append(data[files].iloc[start_idx:])

            # Process each split dataframe and save as CSV in the ZIP file
            for index, split_df in enumerate(split_dfs):
                # Extract the base filename (without folder path) to avoid folder structure in the zip
                base_filename = os.path.basename(files)  # Strip off the folder part
                output_filename = f"{base_filename[0:15]}_split_{index}.csv"
                with zip_file.open(output_filename, 'w') as file:
                    split_df.to_csv(file, index=False)

    # Allow the user to download the entire ZIP file
    zip_buffer.seek(0)  # Rewind the buffer to the beginning of the file

    return zip_buffer
