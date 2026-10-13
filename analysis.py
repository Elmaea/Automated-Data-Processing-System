import pandas as pd
import argparse

from pathlib import Path

def checking_value_abnormality(file, max_range):
    df = pd.read_csv(file, sep='\t')
    k=df.iloc[:,4:5].mean()
    a=float(k+max_range)
    b=float(k-max_range)
    if b>a:
        max_v=b
        min_v=a
        
    else:
        max_v=a
        min_v=b
    global L
    L=[]
    #n=df.shape[0]
    for idx, j in df.iterrows():
        #print("HEREE!!!", j[1], type(j[1]))
        g = int(j[4])
        time=str(j[6])
        #print("g",g,"\nmax_v",max_v,"\nmin_v",min_v)
        #print("HEREE!!!", k, type(k))
        if (g<min_v or g>max_v):
            #print("J THIS",j)
            L.append(time)
    #print("ALERT",f"value has gotten out of range at {L}")
    


def main():
    parser = argparse.ArgumentParser(description="Analyse values of chosen point ids")
    # Define arguments with flags
    parser.add_argument("-d", "--directory", type=str, required=True, help="The directory path where data is stored")
    parser.add_argument("-i", "--maxrange",type=float, required=True, help="maximum amt before alert")
    
    # Parse arguments
    args = parser.parse_args()
    #ishfpodsihfodsif
    out_file = Path(args.directory)
    max_range=args.maxrange
    checking_value_abnormality(out_file, max_range)
if __name__ == "__main__":
        main()
        print(L)