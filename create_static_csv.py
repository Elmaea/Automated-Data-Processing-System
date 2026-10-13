import pandas as pd
import os
import glob
import argparse
import sys
#from datetime import datetime, timezone
from pathlib import Path

#getting all folders from the directory
def find_data_folders(root_dir):
    matching=[f for f in root_dir.iterdir()
              if f.is_dir()]
    return matching

#gives all files that are staic csv files in that folder
def get_all_static_files(folder):
    static_paths=sorted(glob.glob(str(folder/"*/*_static_DB_File.csv")))
    return static_paths

#reading the static csv files, and creating a dict of col_name, filename according to the required point id
def read_static(static_paths):
    for i in static_paths:
        path=Path(i)
        try:
            df = pd.read_csv(path, sep="\t")
            #df = pd.read_csv(path, sep='\t', usecols= lambda col: col.strip() in ["CSV_File_Name"] +["Point_Id"] +["Var_Name"] + ["Description"])
            df_selected = df.iloc[:,2:5]
            #finding the rows with required point ids
            #print(df)
            if os.path.exists("first.csv"):
                df_selected.to_csv("first.csv", mode='a',sep='\t', index=False, header=None)
            else:
                df_selected.to_csv("first.csv", mode='a',sep='\t', index=False)
                
        
        except Exception as e:
            print("Error: reading static files in {}:{}".format(path.name,e))
            return {}
        
def process_folder(folder):
    p = get_all_static_files(folder)
    read_static(p)
def main():
    parser = argparse.ArgumentParser(description="Process file with Point ids.")
    # Define arguments with flags
    parser.add_argument("-d", "--directory", type=str, required=True, help="The directory path where data is stored")
    
    args = parser.parse_args()
    
    print(f"Directory: {args.directory}")
    
    root_dir = Path(args.directory)
    if root_dir is None or not root_dir:
        print("No directory for data archive")
        sys.exit(1)
        
    if os.path.exists("first.csv"):
        os.remove("first.csv")
    if os.path.exists("first_final.csv"):
        os.remove("first_final.csv")
    folders=find_data_folders(root_dir)
    if not folders:
        print("[ERROR] No matching folders found in:{}".format(root_dir))
        sys.exit(1)
    print("Found {} folders(s).\n".format(len(folders)))
    
    for folder in folders:
        process_folder(folder)
        
    df1 = pd.read_csv("first.csv", sep='\t')
    
    #print("Initial reading from output file", df1)
    
    df1.drop_duplicates(inplace=True)
    df1.to_csv("first_final.csv", sep='\t', mode = 'a', index=False)
    os.remove("first.csv")
        
if __name__ == "__main__":
    main()