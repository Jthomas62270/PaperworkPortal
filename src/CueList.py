"""
Author: John Garcia 
Last Modified: Feb. 28, 2024

extract_cue(str show)
    parameters: 
        string containing the shows name as specified in the show file 
    returns:
        a list of cues with appropraite cue data  

"""

import pandas as pd

def extract_cue(show):
    try: 

        PATH = "./CUE_LISTS/"
        temp = PATH + show

        print("Watcher: Opening File -", temp)
        # read showfile information into data frame
        infile = pd.read_csv(temp, skiprows=1) 

        # use forward fill to continue Scenes
        infile["DURATION"] = infile["DURATION"].fillna(0)
        infile["SCENE_TEXT"] = infile["SCENE_TEXT"].fillna(method='ffill')
        infile["TIME_DATA"] = infile["TIME_DATA"].fillna(0)
        infile["FOLLOW"] = infile["FOLLOW"].str.replace("F", "")

        # write to file 
        cue_data = pd.DataFrame(infile.loc[:, ["TARGET_ID", "PART_NUMBER", "SCENE_TEXT", "LABEL", "DURATION", "TIME_DATA", "DOWN_TIME", "UP_DELAY", "DOWN_DELAY", "FOLLOW"]])
        cue_data = cue_data.rename(columns={"TARGET_ID": "CUE_NUMBER", "SCENE_TEXT": "SCENE_NAME", "TIME_DATA": "UP_TIME"})
        cue_data = cue_data.set_index("CUE_NUMBER")
        cue_data = cue_data.iloc[:-2]

        file = "./FORMATTED_CUES/" + show
        print("Cue List: Writing Data to File - ", file)
        cue_data.to_csv(file)
    except FileNotFoundError: 
        print("Cue List: File Not Found")
    except PermissionError: 
        print("Cue List: Privledge Error")
    except Exception as e: 
        print("Error: ", e)
    finally: 
        print("Cue List: returning to main thread")