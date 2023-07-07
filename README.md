# Dropbox Uploader

This Python script allows you to upload changed files from a local directory to your Dropbox account and delete any removed files from Dropbox. It utilizes the Dropbox API for file operations.

## Prerequisites

Before running the script, make sure you have the following:

- Python 3 installed on your machine
- A Dropbox account
- An access token for your Dropbox account. You can obtain this token by creating an app in the [Dropbox developer console](https://www.dropbox.com/developers/apps).

## Installation

1. Clone or download this repository to your local machine.
2. Install the required dependencies by running the following command:
```
pip install dropbox
```

## Usage

1. Set the `directory` variable in the script to the path of the local directory containing the files you want to sync with Dropbox.

2. Create a text file called `token.txt` and paste your Dropbox access token into it. Save the file in the same directory as the script.

3. Run the script using the following command:
```
python main.py
```

The script will compare the files in the local directory with the files in your Dropbox account. It will upload any changed files and delete any files that have been removed locally from Dropbox.

## Explanation

The script consists of the following main components:

- **DropboxUploader class**: This class encapsulates the functionality for interacting with Dropbox. It initializes the Dropbox client using the access token from the `token.txt` file. It also provides methods for calculating the content hash of a file and uploading changed files to Dropbox.

- **dropbox_content_hash function**: This function calculates the content hash of a file by reading it in chunks and hashing each chunk using SHA256. The individual hashes are then hashed again to get the final content hash.

- **upload_changed method**: This method compares the files in the local directory with the files in Dropbox. It uploads any files that have changed (by comparing their content hashes) and logs the changes.

- **download_changed method**: This method compares the files in Dropbox with files in the local directory. It uploads any files that have changed (by comparing their content hashes) and logs the changes.

- **delete_removed method**: This method compares the files in Dropbox with the files in the local directory. It deletes any files that were removed locally from Dropbox and logs the deletions.

- **Main code**: The main code at the bottom of the script creates an instance of the DropboxUploader class and calls the `delete_removed` and `upload_changed` methods to synchronize the files.

## Notes

- Make sure to keep your access token secure and avoid sharing it with others.

- Ensure that you have proper read and write permissions for both the local directory and your Dropbox account.

- You can modify the script according to your specific requirements, such as changing the directory path or adding additional file synchronization logic.

- This script can be scheduled to run periodically using task scheduling tools like cron on Linux or Task Scheduler on Windows to automate the file synchronization process.

For more information on the Dropbox API and Python SDK, refer to the official Dropbox documentation: [https://www.dropbox.com/developers/documentation/python](https://www.dropbox.com/developers/documentation/python)