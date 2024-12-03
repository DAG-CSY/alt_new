from library import *
import func

def run(data_lib, sizes, _filter_func):
    # Create an empty library to store the filtered data and file size
    filtered_data_lib = {}

    # Size limits
    min_size = 321410  # Minimum file size in bytes
    max_size = 400845463  # Maximum file size in bytes

    # Iterate over the data (already loaded from process_zip)
    for file_name, data in data_lib.items():
        file_size = sizes.get(file_name)

        # Skip files that are above or below the specified size limits
        if file_size is None or file_size >= max_size or file_size <= min_size:
            continue  # Skip this file if it's outside the size range

        try:
            # Apply the filter function to the DataFrame
            filtered_data = _filter_func(data)
            if isinstance(filtered_data, pd.DataFrame):
                filtered_data_lib[file_name] = filtered_data
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
            continue

    # Remove smaller files with similar names (if required)
    keys = list(filtered_data_lib.keys())
    keys_to_remove = []

    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            filename1, filename2 = keys[i], keys[j]
            if func.compare(filename1, filename2):
                # Compare file sizes and add the smaller one to the removal list
                keys_to_remove.append(filename1 if sizes[filename1] < sizes[filename2] else filename2)
                break

    # Remove the files marked for deletion
    for key in keys_to_remove:
        filtered_data_lib.pop(key, None)

    return filtered_data_lib
