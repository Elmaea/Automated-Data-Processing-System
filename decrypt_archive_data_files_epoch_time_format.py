import sys
'''import pandas as pd '''
import glob
import os
import datetime
import subprocess
import tarfile
import argparse


def transform_filename(file_path):
    # Extract the filename without extension
    filename_without_ext = os.path.splitext(os.path.basename(file_path))[0]
    # Truncate or pad the filename to 15 characters
    truncated_or_padded = filename_without_ext[:15].ljust(20, 'X')
    # Prepend 'CIPHER_' to the string
    cipher_string = 'CIPHER_' + truncated_or_padded
    # Select even-indexed characters from the end
    even_chars = cipher_string[-2::-2]
    # Select odd-indexed characters from the end
    odd_chars = cipher_string[::-2]
    # Concatenate even and odd indexed characters
    transformed_string = even_chars + odd_chars
    mykeydata = cipher_string + transformed_string
    return mykeydata

def get_enc_file_in_directory(encrypted_directory_path):
    #print(encrypted_directory_path)
    files = glob.glob(encrypted_directory_path+"/*.tar.gz.enc")
    #print(files)
    return files

def decript_file(file_path):
    data_file_path = file_path
    decrypted_tar_file = file_path.rsplit(".", 1)[0]
    #print(data_file_path)
    finalkey = transform_filename(data_file_path)
    #print("final", finalkey)
    #cmd = [ "openssl", "enc", "aes-256-cbc", "-d", "-a", "-md", "md5" , "-in", data_file_path , "-out", decrypted_tar_file, "-pass" , f"pass:{finalkey}" ]
    cmd = [ "openssl", "aes-256-cbc", "-d", "-a", "-pbkdf2" , "-in", data_file_path , "-out", decrypted_tar_file, "-pass" , f"pass:{finalkey}" ]
    result = subprocess.run(cmd, capture_output=True, text=True) 
    #print("result", result)
    if result.returncode == 0:
        print("Decryption successful!\n\n")
        return 0
    else:
        print("Error:", result.stderr)
        return 1

def untar_file(encrypted_directory_path, tar_file):
    try:
        with tarfile.TarFile.gzopen(tar_file, 'r') as tar :
            tar.extractall(encrypted_directory_path)
        print(f"Extracted {tar_file} work directory")
    except Exception as e:
       	print(f"Error processing {tar_file}: {e}")
 
def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Enrypted file directory")
    # Define arguments with flags
    parser.add_argument("-d", "--directory", type=str, required=True, help="The directory path where encrypted data is stored")
    # Parse arguments
    args = parser.parse_args()
    # Print values
    if len(sys.argv) != 3:
        print("Usage: python script.py <absolute path of file>")
        sys.exit(1)
    print(f"Directory: {args.directory}")
    current_time = datetime.datetime.now().strftime('Execution started at : %d-%m-%Y %H:%M:%S')
    print(current_time)
    encrypted_directory_path = args.directory
    #print(encrypted_directory_path)
    all_enc_files = get_enc_file_in_directory(encrypted_directory_path)
    #print(all_enc_files)
    if not all_enc_files:
        print(f"No encrypted archive files found in the Directory: {args.directory} \n\nPlease select the correct directory where encrypted files are stored.")
        sys.exit(1)
    else:
        print(f"Total {len(all_enc_files)} encripted file/files found")
        for file in all_enc_files:
            print(file)
    for enc_data_file in all_enc_files:
        decript_file(enc_data_file)
        decrypted_tar_file = enc_data_file.rsplit(".", 1)[0]
        print(decrypted_tar_file)
        untar_file(encrypted_directory_path, decrypted_tar_file)
        os.remove(decrypted_tar_file)
    current_time = datetime.datetime.now().strftime('Execution completed at : %d-%m-%Y %H:%M:%S')
    print(current_time)
    print(f"Extracted data csv files are stored in : {encrypted_directory_path} directory")
    
if __name__ == "__main__":
    main()