import os
import hashlib
import dropbox.files

# Set the directory path where the files are located
directory = ""


# Create a class for DropboxUploader
class DropboxUploader:
    def __init__(self, token_file):
        # Read the access token from the token_file
        with open(token_file, "r") as f:
            access_token = f.read()
        # Initialize an instance of Dropbox using the access token
        self.dbx = dropbox.Dropbox(access_token)

    @staticmethod
    def dropbox_content_hash(file):
        # Calculate the content hash of a file
        hash_chuck_size = 4 * 1024 * 1024
        with open(file, "rb") as f:
            block_hashes = bytes()
            # Read the file in chunks and calculate the hash for each chunk
            while True:
                chunk = f.read(hash_chuck_size)
                if not chunk:
                    break
                block_hashes += hashlib.sha256(chunk).digest()
            # Calculate the final hash by hashing all the individual hashes
            return hashlib.sha256(block_hashes).hexdigest()

    def upload_changed(self):
        # Get the list of filenames and their content hashes from the Dropbox folder
        cloud_files = {e.name: e.content_hash for e in self.dbx.files_list_folder("").entries}
        # Traverse through the local directory
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                # Get the relative path of the file
                relative_path = os.path.relpath(file_path, directory)
                # Construct the cloud file path using the relative path
                cloud_file_path = f"/{relative_path}"

                # Check if the file is already present in the Dropbox folder
                if file in cloud_files.keys():
                    local_hash = self.dropbox_content_hash(file_path)
                    # Compare the local hash with the cloud content hash
                    if local_hash != cloud_files[file]:
                        print(f"File Changed {file}")
                        # If the hashes don't match, upload the file to Dropbox
                        with open(file_path, "rb") as f:
                            data = f.read()
                            self.dbx.files_upload(data, cloud_file_path, mode=dropbox.files.WriteMode.overwrite)
                    else:
                        print(f"File Not Changed {file}")
                else:
                    print(f"File Not Found {file}")
                    # If the file is not found in the Dropbox folder, upload it to Dropbox
                    with open(file_path, "rb") as f:
                        data = f.read()
                        self.dbx.files_upload(data, cloud_file_path, mode=dropbox.files.WriteMode.overwrite)

    def delete_removed(self):
        # Get the list of filenames and their content hashes from the Dropbox folder
        cloud_files = {e.name: e.content_hash for e in self.dbx.files_list_folder("").entries}
        # Get the list of files in the local directory using self.directory
        local_files = os.listdir(directory)

        # Traverse through the cloud files
        for file in cloud_files.keys():
            # Check if the file exists in the local directory
            if file not in local_files:
                print(f"File Removed {file}")
                # If the file does not exist locally, delete it from Dropbox
                self.dbx.files_delete_v2(f"/{file}")


# Create an instance of DropboxUploader and call the delete_removed method
DropboxUploader("token.txt").delete_removed()
# Create another instance of DropboxUploader and call the upload_changed method
DropboxUploader("token.txt").upload_changed()
