# Created by Dayu Wang (dwang@stchas.edu) on 2022-02-23

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-02-23

import tkinter
from datetime import datetime
from pytrends.request import TrendReq
from tkinter import filedialog


def main():
    # Open the input file.
    tkinter.Tk().withdraw()
    input_file = filedialog.askopenfilename()
    input_file = open(input_file)

    # Create an instance of "pytrends".
    pytrends = TrendReq(hl="en-US", tz=360)

    # Read the data from the input file.
    lines = input_file.readlines()
    time_begin, time_end, region, index, stage = None, None, None, None, None
    suggestions = []
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        colon = line.find(':')
        if colon == -1:
            if stage == "KEYWORDS":
                current_keyword, refined_keyword = line, line

                # Get the closest search keyword.
                for suggestion in pytrends.suggestions(current_keyword):
                    if suggestion["type"].strip().lower() in suggestions:
                        refined_keyword = suggestion["mid"].strip()
                        break

                # Search the current keyword using Google Trends.
                pytrends.build_payload([refined_keyword], timeframe=time_begin + ' ' + time_end, geo=region)
                result = pytrends.interest_over_time()

                # Prepare and save the result to the output file.
                now = datetime.now().strftime("%Y-%m-%dT%H%M")
                o_filename = '!' if current_keyword == refined_keyword else ''
                o_filename += (("%03d - " % index) + current_keyword + " - " + now + " - CSV.csv").replace(' ', '_')
                index += 1
                if not result.empty:
                    result.rename(columns={refined_keyword: current_keyword}, inplace=True)
                    result.drop(labels=["isPartial"], axis=1, inplace=True)
                result.to_csv(o_filename)
                print("File \"%s\" created" % o_filename)
            if stage == "SUGGESTIONS":
                suggestions.append(line.lower())
        else:
            if line[:colon] == "TIME BEGIN":
                time_begin = line[colon + 1:].strip()
            if line[:colon] == "TIME END":
                time_end = line[colon + 1:].strip()
            if line[:colon] == "REGION":
                region = line[colon + 1:].strip()
            if line[:colon] == "INDEX":
                index = int(line[colon + 1:].strip())
            if line[:colon] == "SUGGESTIONS" or line[:colon] == "KEYWORDS":
                stage = line[:colon]

    # Close the files
    input_file.close()


if __name__ == "__main__":
    main()
