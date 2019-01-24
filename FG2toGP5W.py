import re

def FG2_to_GP5W(FG2_file, new_file):
    ''' convert FG2 geoprecision csv export to old-style (GP5W)
    
    Args 
        FG2_file (str) : path to a FG2-style csv
        new_file (str) : path to output file
    '''
    
    with open(FG2_file, 'r') as old:
        if not "FG2" in old.readline():
            raise Exception("Not a valid FG2 file")

        with open(new_file, 'w') as new:
            for line in old:
                
                # check if it is an info line
                if "<" in line:
                    
                    # reformat header rows to match old-style
                    if "LOGGER" in line:
                        logger = re.sub("<LOGGER: \\$(\w{6})>.*", "\\1", line).strip()
                        line = "Logger: #{} 'PT1000TEMP' - USP_EXP2 - (CGI) Expander for GP5W - (V2.7, Jan 12 2016)\n".format(logger)
                        new.writelines(line)               
                        
                    # skip all other comment lines
                    else:
                        continue

                # non comment lines   
                else:
                    
                    # reformat header rows to match old-style
                    if "TIME" in line:
                        line = re.sub("NO", "No", line)
                        line = re.sub("TIME", "Time", line)
                        line = re.sub("HK-BAT", "#HK-Bat", line)
                        line = re.sub("\\((\w*)\\)", ":\\1", line)
                        
                        new.writelines(line)
                    
                    # write all data lines
                    else:
                        new.writelines(line)
                        
                                        
if __name__ == "__main__":
    import argparse
    import glob
    import os
    
    parser = argparse.ArgumentParser(description="Convert geoprecision csv exports",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--f',    default=None, type=str, help="single file path to convert")
    parser.add_argument('--n',    default=None, type=str, help="single file new output")
    parser.add_argument('--d',    default=None, type=str, help="directory of csv files to convert")

    
    args = parser.parse_args()
    
    # Processing a single file
    if args.f:    
        in_file = args.f
        out_file = args.n
        FG2_to_GP5W(in_file, out_file)
        
        print("Created: {}".format(out_file))
    
    # Processing a directory of files
    if args.d:
        files = glob.glob(os.path.join(args.d, "*.csv"))
        
        for f in files:
            out_file = re.sub("\\.csv$", "_GP5Wfmt.csv", f)
            
            try:
                FG2_to_GP5W(f, out_file)
            except:
                print("could not convert file {}".format(os.path.basename(f)))
                        
