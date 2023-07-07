import os
import hashlib
import dropbox.files

directory = "../../work/env/"


class DropboxUploader:
    def __init__(self, token_file):
        with open(token_file, "r") as f:
            access_token = f.read()
        self.dbx = dropbox.Dropbox(access_token)

    @staticmethod
    def dropbox_content_hash(file):
        hash_chuck_size = 4 * 1024 * 1024
        with open(file, "rb") as f:
            block_hashes = bytes()
            while True:
                chunk = f.read(hash_chuck_size)
                if not chunk:
                    break
                block_hashes += hashlib.sha256(chunk).digest()
            return hashlib.sha256(block_hashes).hexdigest()

    def upload_changed(self):
        cloud_files = {e.name: e.content_hash for e in self.dbx.files_list_folder("").entries}
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)
                cloud_file_path = f"/{relative_path}"

                if file in cloud_files.keys():
                    local_hash = self.dropbox_content_hash(file_path)
                    if local_hash != cloud_files[file]:
                        print(f"File Changed {file}")
                        with open(file_path, "rb") as f:
                            data = f.read()
                            self.dbx.files_upload(data, cloud_file_path, mode=dropbox.files.WriteMode.overwrite)
                    else:
                        print(f"File Not Changed {file}")
                else:
                    print(f"File Not Found {file}")
                    with open(file_path, "rb") as f:
                        data = f.read()
                        self.dbx.files_upload(data, cloud_file_path, mode=dropbox.files.WriteMode.overwrite)

    def delete_removed(self):
        cloud_files = {e.name: e.content_hash for e in self.dbx.files_list_folder("").entries}
        local_files = os.listdir(directory)  # Get the list of files in the local directory using self.directory

        for file in cloud_files.keys():
            if file not in local_files:
                print(f"File Removed {file}")
                self.dbx.files_delete_v2(f"/{file}")


DropboxUploader("token.txt").delete_removed()
DropboxUploader("token.txt").upload_changed()
