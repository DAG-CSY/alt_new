from library import *

#  Function to read GitHub token from a secrets.txt file
def get_github_token():
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token is not None:
        return github_token
    else:
        return None  # Return None if no token is found

def upload_zip_buffer_to_github(repo, zip_buffer, commit_message, target_path):
    # Ensure the buffer is in bytes if it's a BytesIO object
    if isinstance(zip_buffer, io.BytesIO):
        zip_buffer = zip_buffer.getvalue()  # Convert buffer to bytes

    try:
        # Try to get the file from the target path to check if it exists
        existing_file = repo.get_contents(target_path)
        # If the file exists, update it
        repo.update_file(existing_file.path, commit_message, zip_buffer, existing_file.sha)
        print(f"Updated the file: {target_path}")
    except:
        # If the file doesn't exist, create a new one
        repo.create_file(target_path, commit_message, zip_buffer)
        print(f"Created new file: {target_path}")


# Function to get the repository from GitHub using a token
def get_github_repo(token, repo_name):
    g = Github(token)
    repo = g.get_repo(repo_name)
    return repo


def extract_zip_content_from_github(zip_data):
    # Create dictionaries to store file names and their corresponding data and sizes
    file_data = {}  
    file_sizes = {}  
    with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_ref:
        file_names = zip_ref.namelist()  # List of files inside the zip
        for file_name in file_names:
            # Get the file size directly from the zip file metadata
            file_info = zip_ref.getinfo(file_name)
            file_size = file_info.file_size  # Get the file size from the metadata
            file_sizes[file_name] = file_size

            with zip_ref.open(file_name) as file:
                # For CSV files, read them into a pandas DataFrame
                if file_name.endswith('.csv'):
                    file_data[file_name] = pd.read_csv(file)  # Load CSV into DataFrame
                elif file_name.endswith('.txt'):
                    file_data[file_name] = file.read().decode('utf-8')  # Read TXT file as string
    return file_data, file_sizes

# Function to fetch the latest file from GitHub
def fetch_latest_file_from_github(repo_name, zip_file, token):
    raw_url = f"https://raw.githubusercontent.com/{repo_name}/main/{zip_file}"

    # Make a request to get the zip file as binary data
    response = requests.get(raw_url, headers={"Authorization": f"token {token}"})
    response.raise_for_status()  # Check for errors in the response

    if response.status_code == 200:
        # Get the file data
        file_data = response.content
        return file_data
    else:
        raise Exception(f"Failed to fetch file: {response.status_code}")
    
    

# # Function to compute the hash of the file content
# def get_file_hash(file_data):
#     return hashlib.md5(file_data).hexdigest()

# # Function to compare the current file's hash with the stored hash
# def check_for_file_update(stored_hash, repo_name, zip_file, token):
#     try:
#         # Fetch the latest file data from GitHub
#         latest_file_data = fetch_latest_file_from_github(repo_name, zip_file, token)

#         # Calculate the hash of the latest file
#         latest_file_hash = get_file_hash(latest_file_data)

#         # If the hash is different from the stored hash, it means the file has changed
#         if latest_file_hash != stored_hash:
#             print("File has been updated.")
#             # Update stored hash to the new file hash
#             stored_hash = latest_file_hash
#             return True, stored_hash
#         else:
#             print("File has not changed.")
#             return False, stored_hash
#     except Exception as e:
#         print(f"Error checking for update: {e}")
#         return False, stored_hash
