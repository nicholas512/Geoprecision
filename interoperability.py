""" Convert Geoprecision csv files to different formats """

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
