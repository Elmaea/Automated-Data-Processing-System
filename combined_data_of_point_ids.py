
import pandas as pd
import os
import glob
import argparse
import sys
from datetime import datetime, timezone
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
def read_static(static_paths, point_ids):
    D={}
    #print("listttt",static_paths,"\n")
    for i in static_paths:
        path=Path(i)
        #print("this",path)
        #print("hereee",point_ids)
        
        try:
            df = pd.read_csv(path, sep="\t", header = None)
            df_selected = df.iloc[:, :3]
            #print("uyfsadugsa",df_selected)
            #finding the rows with required point ids
            for idx, j in df_selected.iterrows():
                if j[2] in point_ids:
                    if j[1] in D.keys():
                        D[j[1]].append(str(j[0]))
                    else:
                        D[j[1]]=[str(j[0])]
                    D[j[1]].append(str(i))
            #print("ajshdvjsahudv",D)
            
        
        except Exception as e:
            print("Error: reading static files in {}:{}".format(path.name,e))
            return {}
    return D
    
global working_directory


def read_dynamic_files(folder,D,point_ids):
    dynamic_files = D.keys()
    #print("tfsujydfauysd",dynamic_files)
    if len(dynamic_files)!=0:
        for i in dynamic_files:
            #print("jhsfdjsayfdjgv")
            k=D[i][1].split('/')
            p=k.pop()
            k.append(i)
            #print("hhahah",k)
            dyn_path=Path("/".join(k))
            #print("thiusis",dyn_path)
            #dyn_path=sorted(glob.glob(str(folder,"/*",i)))
            #dyn_path=os.path.join(folder,"**",i)
            #print("pathhhhh",dyn_path)
            
            #creating a list of names of col_no
            cols=D[i]
            #creating a list of required column headers
            needed_cols = []
            for col_no in cols:
                needed_cols.append("{}value".format(col_no))
                needed_cols.append("{}status".format(col_no))
            
            #reading the dynamic file and taking all the column data
            try:
                df = pd.read_csv(dyn_path, sep='\t', usecols= lambda col: col in ["sequence_counter"] +["timestamp_s"] + ["time_ms"] + ["timestamplocal_s"] + needed_cols)
                df["timestamp_s_utc"]=df["timestamp_s"].apply(fmt_epoch)
                df.rename(columns={"timestamp_s": "timestamp_epoch"})
                
               # print("Df: \n", df)
                
                #creating a csv file with all the data, appending it each time
                if os.path.exists("output.csv"):
                    df.to_csv("output.csv", mode='a', sep='\t', index=False, header=None)
                else:
                    df.to_csv("output.csv", mode='a', sep='\t' , index=False)
         
                
            except Exception as e:
                print("Error: reading dynamic files in {}:{}".format(dyn_path.name,e))
                return {}

            
#changing the epoch time to a human readable form
def fmt_epoch(ts):
    try:
        return datetime.fromtimestamp(int(ts),tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    except(ValueError,OSError):
        return str(ts)
        
#calling all the functions
def process_folder(folder,point_ids):
    p = get_all_static_files(folder)
    index =read_static(p,point_ids)
    read_dynamic_files(folder,index,point_ids)

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Process file with Point ids.")
    # Define arguments with flags
    parser.add_argument("-d", "--directory", type=str, required=True, help="The directory path where data is stored")
    parser.add_argument("-i", "--ids", nargs="+", required=True, help="one or more point ids")
    
    # Parse arguments
    args = parser.parse_args()
    
    #printing the given directory
    #print(f"Directory: {args.directory}")
    
    root_dir = Path(args.directory)
    if root_dir is None or not root_dir:
        print("No directory for data archive")
        sys.exit(1)
        
    point_ids=[p.strip() for p in args.ids]
    #print("erooreeeeeeeee",point_ids)
    if os.path.exists("output.csv"):
        os.remove("output.csv")
        
    folders=find_data_folders(root_dir)
    if not folders:
        print("[ERROR] No matching folders found in:{}".format(root_dir))
        sys.exit(1)
    print("\nFound {} folders(s). Querying point IDS:{}".format(len(folders),point_ids))
    
    for folder in folders:
        process_folder(folder,point_ids)
    
    #df1 = pd.read_csv("output.csv", sep='\t')
    
    #print("Initial reading from output file", df1)
    
    #df1.drop_duplicates(inplace=True, keep = False)
    
    #df1.to_csv("output_final.csv", sep='\t', mode = 'a', index=False)
    
    #os.remove("output.csv")
    
    return 

if __name__ == "__main__":
    main()
    