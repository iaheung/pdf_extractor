# FILE: pdf_extract.py

import pandas as pd
import numpy as np
import pymupdf as pdf
import os

# Set pandas display options
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)

def make_df(bold_array, text_array):
    """
    Creates pandas dataframe from the two arrays of text 

    Args:
        bold_array (list): list of bolded text (keywords)
        text_array (list): list of text (keyword description)

    Returns:
        df: Pandas dataframe ready to be saved into csv format
    """
    df = pd.DataFrame({
        "Bold Text": bold_array,
        "Description": text_array[:-1] # remove last term because of last row of red characters in PDF (A, B, C, D...)
    })
    return df

def fail_make_df(bold_array, text_array):
    """
    When make_df() fails, this function will be run, 
    which allows for unequal lengths for the bold and text arrays
    """
    min_length = min(len(bold_array), len(text_array))
    df = pd.DataFrame({
        "Bold Text": bold_array[:min_length],
        "Description": text_array[:min_length]
    })
    return df

def extract_text(letter):
    """
    Given an input letter (Must be capital), references the file to extract and outputs 
    two arrays, one of the keywords (bolded phrases), and their respective descriptions (text following bolder phrases)

    Args:
        letter (str): letter corresponding to PDF file

    Returns:
        bold_array (list): list of bolded text (keywords)
        text_array (list): list of text (keyword description)
    """
    file = pdf.open(f"raw_data/Guardian and Observer style guide_ {letter} _ Information _ The Guardian.pdf")
    bold_array = []
    text_array = []

    prev_string = False # there are parts where the explanation of a term spans multiple blocks
    first_bold = False # to prevent extracting the first few title page words before first term

    bold_text = ""
    for page_num in range(len(file)):
        page = file[page_num] # each pdf page
        blocks = page.get_text("dict")["blocks"] # a page is separated into "blocks"

        for block in blocks:
            # see if the key 'lines' exists, so to not extract things like images
            if 'lines' in block: 
                lines = block['lines'] # each block contains lines of text
                # see if key 'spans' is in the dict of the first line
                if 'spans' in lines[0]:
                    # font size of desired text is 12.75 
                    if lines[0]['spans'][0]['size'] == 12.75:
                        num_lines = len(lines)
                        firstline = lines[0]['spans'][0]
                        # check if they are the correct color (black)
                        if (firstline['color'] == -15592942):
                            # add condition for C stuff (capital)
                            if firstline['font'] == 'GuardianTextEgyptian-Bol':
                                bold_text = firstline['text']
                                bold_array.append(bold_text)
                                first_bold = True # first bold character has appeared
                            elif firstline['font'] == 'GuardianTextEgyptian-Reg':
                                # there is a previous string we need to add more text to
                                prev_string = True
                            else:
                                print("Unknown Font")
                        
                        if prev_string:
                            current_string = text_array[-1]
                            for i in range(0, num_lines):
                                for j in range(len(lines[i]['spans'])):
                                    current_string += lines[i]['spans'][j]['text']
                                    current_string += " "
                            text_array[-1] = current_string.rstrip()
                        elif first_bold:
                            full_string = ""
                            for i in range(1, num_lines):
                                for j in range(len(lines[i]['spans'])):
                                    full_string += lines[i]['spans'][j]['text']
                                    full_string += " "
                            text_array.append(full_string.rstrip())
                        prev_string = False
    return bold_array, text_array

def main():
    letter_array = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',  'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    save_folder = "csv_formatted"
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    for letter in letter_array:
        try:
            bold_array, text_array = extract_text(letter)
            df = make_df(bold_array, text_array)
        except Exception as e:
            print(f"Error processing {letter}: {e}")
            # Fallback to test_make_df
            df = fail_make_df(bold_array, text_array)
        
        filename = f"{letter}.csv"
        df.to_csv(os.path.join(save_folder, filename), index=False)

if __name__ == "__main__":
    main()