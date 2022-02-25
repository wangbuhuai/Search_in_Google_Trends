# Created by Dayu Wang (dwang@stchas.edu) on 2022-02-25

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-02-25


import json
import requests
import tkinter
from datetime import datetime
from pytrends.request import TrendReq
from tkinter import filedialog

# Constant parameters
SEARCH_PARAMETERS = {
    "c2coff": 1,
    "hl": "en",
    "lr": "lang_en"
}


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
    suggestions, final_suggestion = [], None
    key, cx, q = None, None, None
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        colon = line.find(':')
        if colon == -1:
            if stage == "KEYWORDS":
                # Find the CEO of the company.
                q = (line + " CEO").replace(' ', "%20").replace('&', "%26")
                response = requests.get(
                    "https://www.googleapis.com/customsearch/v1?c2coff=%dhl=%s&lr=%s&key=%s&cx=%s&q=%s" % (
                        SEARCH_PARAMETERS["c2coff"], SEARCH_PARAMETERS["hl"], SEARCH_PARAMETERS["lr"], key, cx, q
                    ))
                item = json.loads(response.text)
                ceo = item["items"][0]["title"].split('-')[0].strip()
                print(ceo)

                # Find the SVI of the CEO.
                current_keyword, refined_keyword = ceo, ceo

                # Get the closest search keyword.
                final_suggestion = None
                num_of_suggestions = len(pytrends.suggestions(current_keyword))
                for suggestion in pytrends.suggestions(current_keyword):
                    for sug in suggestions:
                        if sug in suggestion["type"].strip().lower():
                            refined_keyword = suggestion["mid"].strip()
                            final_suggestion = suggestion["type"].strip().lower()
                            break

                # Search the current keyword using Google Trends.
                pytrends.build_payload([refined_keyword], timeframe=time_begin + ' ' + time_end, geo=region)
                result = pytrends.interest_over_time()

                # Prepare and save the result to the output file.
                now = datetime.now().strftime("%Y-%m-%dT%H%M")
                o_filename = '' if num_of_suggestions == 0 or current_keyword != refined_keyword else '!'
                o_filename += (("%03d - " % index) + current_keyword + " - " + now + " - CSV.csv").replace(' ', '_')
                index += 1
                if not result.empty:
                    new_col_name = current_keyword
                    if final_suggestion is not None:
                        new_col_name += " (" + final_suggestion + ')'
                    result.rename(columns={refined_keyword: new_col_name}, inplace=True)
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
            if line[:colon] == "KEY":
                key = line[colon + 1:].strip()
            if line[:colon] == "CX":
                cx = line[colon + 1:].strip()

    # Close the files
    input_file.close()


if __name__ == "__main__":
    main()
