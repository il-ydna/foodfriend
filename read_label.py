import sys
import math
import cv2
import numpy as np
import pytesseract
from fuzzywuzzy import fuzz

pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
macro_categories = ["About  servings per", "Serving size", "Amount per serving",
             "Total Fat", "Calories", "Cholesterol", "Sodium", "Total Carbohydrates", "Protein", ]

def read_nutrition_facts(img):
    custom_config = r'--oem 3 --psm 6'  # Page segmentation mode 6: Assume a single uniform block of text.
    text = pytesseract.image_to_string(img, config=custom_config)

    # Split the text into lines
    lines = text.split('\n')


    # Print each line
    print("#################### UNFILTERED ####################")
    for line in lines:
        print(line)

    cv2.imshow('image', img)
    cv2.waitKey(0)

    return lines

def fuzzy_search(example_list, query_list, threshold = 70):
    res = {}
    for query in query_list:

        # Find the closest match to the query in the list of words
        best_match = max(example_list, key=lambda word: fuzz.ratio(word, query))

        # Calculate the similarity ratio of the best match
        similarity_ratio = fuzz.ratio(best_match, query)

        if similarity_ratio >= threshold:
            print(query, " MAPS TO --> ", best_match)
            for token in query.split():
                if any(char.isdigit() for char in token):
                    res[best_match.lower()] = token
                    break

    return res

def match_macros(readings):
    print("#################### MACROS ####################")

    return fuzzy_search(macro_categories, readings, 70)

def match_other(readings):
    print("#################### OTHER ####################")
    words = ["Vitamin D", "Iron", "Calcium", "Potassium"]
    fuzzy_search(words, readings, 40)

def fix_value(user_in, dictionary):
    new_value = input(f"Changing: {user_in}. What should the new value be?")
    if not new_value.isdigit():
        print("invalid value! try again")
    else:
        dictionary[user_in] = new_value
        print(f"{user_in} corrected to {new_value}, thanks for the input!")

def parse_text(readings):
    macros = match_macros(readings)
    print(macros)
    needsFixing = True
    while needsFixing:
        user_in = input("Write the name of any categories that need fixing. \n"
              "Once everything looks good, enter \"done\"")
        if macros.get(user_in.lower()):
            fix_value(user_in, macros)
        else:
            best_match = max(macro_categories, key=lambda word: fuzz.ratio(word, user_in))
            similarity_ratio = fuzz.ratio(best_match, user_in)
            if(similarity_ratio >= 70):
                if input(f"Did you mean {best_match}? (y/n)").lower() == 'y':
                    fix_value(best_match.lower(), macros)
            else:
                break;

    return macros