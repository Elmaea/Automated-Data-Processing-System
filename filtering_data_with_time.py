import pandas as pd
import argparse
import sys
import os
from datetime import datetime, timezone
from pathlib import Path
import subprocess
from tkinter import messagebox



def fmt_epoch(ts):
    try:
        return datetime.fromtimestamp(int(ts),tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    except(ValueError,OSError):
        messagebox.showerror("ERROR!", ValueError)

def convert_time_to_epoch(ist_datetime_str):
    # Convert to datetime object
    ist_datetime = pd.to_datetime(ist_datetime_str)
    # Convert to epoch timestamp
    
    epoch_time = int(ist_datetime.timestamp())
    return epoch_time

def filtering_data_with_time(df2,present_epoch,point_id):
    
    #df2["timestamp_s"] = df2["timestamp_s"].astype(str).str.strip().astype(int)
    #print("HERERERER", df2.dtypes)
    #print("columns", df2.columns)
    if "timestamp_s" in df2.columns:
        #print("timestamp_s found")
        
        start_epoch=present_epoch - 1800
        end_epoch=present_epoch + 1800
        for idx, j in df2.iterrows():
            #print("HEREE!!!", j[1], type(j[1]))
            k = int(j[1])
            #print("HEREE!!!", k, type(k))
            if (k>=start_epoch and k<=end_epoch):
                #print("J THIS",j)
                df4=pd.DataFrame(j).T
                time_req = str(fmt_epoch(present_epoch))
                req=time_req.split()
                tr="_".join(req)
                #print("THISS",df4)
                if os.path.exists(f"{output_directory}/Output_File_{point_id}_{tr}.csv"):
                    df4.to_csv(f"{output_directory}/Output_File_{point_id}_{tr}.csv", mode='a',sep='\t', index=False, header=None)
                    
                else:
                    df4.to_csv(f"{output_directory}/Output_File_{point_id}_{tr}.csv", mode='a',sep='\t', index=False)

    #return df2

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Process file with Point ids.")
    # Define arguments with flags
    parser.add_argument("-d", "--directory", type=str, required=True, help="The directory path where data is stored")
    parser.add_argument("-i", "--ids", nargs="+", required=True, help="one or more point ids")
    parser.add_argument("-r", "--req_time", type=str, required=True, help="Required time (format: YYYY-MM-DD HH:MM:SS)")
    
    # Parse arguments
    args = parser.parse_args()
    global a
    global output_directory
    a=0
    trr=str(args.req_time)
    tt="_".join(trr.split())
    while True:
        if os.path.exists(Path(str(Path.cwd()) + f"/Dynamic_Data_{a}_{tt}")):
            a+=1
        else:
            output_directory = Path(str(Path.cwd()) + f"/Dynamic_Data_{a}_{tt}")
            output_directory.mkdir(exist_ok = True)
            break
    #print(output_directory)
    
    #printing the given directory
    print(f"Directory: {args.directory}")
    print(f"Required Time: {args.req_time}")
    
    present_epoch = convert_time_to_epoch(args.req_time)
        
    root_dir = Path(args.directory)
    if root_dir is None or not root_dir:
        print("No directory for data archive")
        sys.exit(1)
        
    point_ids=[p.strip() for p in args.ids]
    for i in point_ids:
        L=["python3", "combined_data_of_point_ids.py", "-d", root_dir, "-i"]
        L.append(str(i))
        subprocess.run(L)
        df2 = pd.read_csv("output.csv", sep='\t')
        #print("df2", df2)
        #print("type of df2", type(df2))
        
        if os.path.exists(f"Output_File_{i}_{tt}.csv"):
            os.remove(f"Output_File_{i}_{tt}.csv")
    
        filtering_data_with_time(df2,present_epoch,i)
        
        if not os.path.exists(f"{output_directory}/Output_File_{i}_{tt}_UTC.csv"):
            print(f"Output file for {i} not made as {args.req_time} for the mentioned point id does NOT exist")
        else:
            print(f"Output file for {i} with time {args.req_time} created successfully")

    print("All required files have been created!")
    return

if __name__ == "__main__":
    main()
    print(f"Output Directory = {output_directory}")