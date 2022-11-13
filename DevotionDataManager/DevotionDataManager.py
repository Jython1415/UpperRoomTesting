import os
import unicodedata
from datetime import datetime
import time
import json

# Characters to remove
characterBlacklist = ['　', '\n', '\r', ' ', u"\u000A", u"\u0009", u"\u2424", u"\u000D", u"\u23CE", u"\u240D", u"\u2B90", u"\u2B91", u"\u2B92", u"\u2B93", u"\u4DD7", u"\u0008", u"\u0020", u"\u00A0", u"\u1361", u"\u1680", u"\u2000", u"\u2002", u"\u2003", u"\u2004", u"\u2005", u"\u2006", u"\u2007", u"\u2008", u"\u2009", u"\u200A", u"\u200B", u"\u202F", u"\u205F", u"\u3000", u"\uFEFF", unicodedata.lookup("SPACE"), '\t']

# Stores all devotions (separated into paragraphs)
allDevotions = []

# Devotion class
class Devotion:
    
    def __init__(self, date, japaneseDate, title, bibleReading, biblePassage, bibleText, devotionText, prayer, thought, prayerFocus, author):
        self.date = date
        self.japaneseDate = japaneseDate
        self.title = title
        self.bibleReading = bibleReading
        self.biblePassage = biblePassage
        self.bibleText = bibleText
        self.devotionText = devotionText
        self.prayer = prayer
        self.thought = thought
        self.prayerFocus = prayerFocus
        self.author = author
        
        self.dict = {
            "date": date,
            "japaneseDate": japaneseDate,
            "title": title,
            "bibleReading": bibleReading,
            "biblePassage": biblePassage,
            "bibleText": bibleText,
            "devotionText": devotionText,
            "prayer": prayer,
            "thought": thought,
            "prayerFocus": prayerFocus,
            "author": author
        }

# Main function ###################################################################################
def main():
    print("\n0 Cancel\n1 Create template text file\n2 Validate input text file\n3 Generate devotion data from input")
    userSelection = input("Select: ")
    
    if userSelection == "1":
        createTemplateTextFile()
        
        # Home or finish
        print("0 Home\n1 Finish")
        userSelection = input("Select: ")
        if userSelection == "0":
            main()
        elif userSelection == "1":
            print("Done")
            
    elif userSelection == "2":
        validateInputTextFile()
        
                # Home or finish
        print("0 Home\n1 Finish")
        userSelection = input("Select: ")
        if userSelection == "0":
            main()
        elif userSelection == "1":
            print("Done")
            
    elif userSelection == "3":
        print("\n3.0 Back\n3.1 JSON Output\n3.2 Old Output (deprecated)")
        userSelection = input("Select: ")
        
        if userSelection == "0" or userSelection == "3.0":
            main()
            
        elif userSelection == "1" or userSelection == "3.1":
            generateJSONfromInput()
            
            # Home or finish
            print("0 Home\n1 Finish")
            userSelection = input("Select: ")
            if userSelection == "0":
                main()
            elif userSelection == "1":
                print("Done")
                
        elif userSelection == "2" or userSelection == "3.2":
            generateOldDevotionDataFromInput()
            
            # Home or finish
            print("0 Home\n1 Finish")
            userSelection = input("Select: ")
            if userSelection == "0":
                main()
            elif userSelection == "1":
                print("Done")

# Add leading zeros
def withLeadingZeros(number, desiredNumOfDigits):
    return "0"*(desiredNumOfDigits - len(str(number))) + str(number)

# Ask user for folder path (allows for dragging)
def getDraggablePath(message):
	filePath = input(message + "\nDrag file/folder or paste path: ")
	if filePath[len(filePath) - 1] == " ":
		filePath = filePath[:len(filePath) - 1]
	return filePath

# Creates a text file with the input name (and input location)
def createTextFile(name, folderPath=""):
    fileName = folderPath + "/" + name + "_" + datetime.now().strftime("%H-%M-%S") + ".txt"
    file = open(fileName, 'x', encoding='utf8')
    
    return file

# Creates a json file with the input name (and input location)
def createJSONFile(name, folderPath=""):
    fileName = folderPath + "/" + name + "_" + datetime.now().strftime("%H-%M-%S") + ".json"
    file = open(fileName, 'x', encoding='utf8')
    
    return file

# Create template text file #######################################################################
def createTemplateTextFile(): 
    month = int(input("What month is this for?\nInput as number: "))
    year = int(input("What year is it?\nInput as number: "))
    numDays = numDaysInMonth(month, year)
    
    folderPath = getDraggablePath("What folder should the template file go in?")
    
    startTime = time.perf_counter()
    
    templateText = ""
    for day in range(numDays):
        # Date
        templateText += f"{year}-{withLeadingZeros(month,2)}-{withLeadingZeros(day+1,2)}\n"
        
        # Dividers
        templateText += "-s-\n\n"*6 + "</p>\n\n"*3 + "-s-\n\n"*4 + "---\n"
    
    templateText = templateText[:len(templateText) - 4]
    
    print("Creating file...")
    fileName = f'{year}-{withLeadingZeros(month,2)}-input'
    file = createTextFile(fileName, folderPath)
    file.write(templateText)
    file.close()
    
    endTime = time.perf_counter()
    
    print(f"Template file created in {round(endTime-startTime,5)} seconds")
    
def numDaysInMonth(month, year):
    if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
        return 31
    elif month == 4 or month == 6 or month == 9 or month == 11:
        return 30
    elif month == 2:
        if year % 4 == 0:
            return 29
        else:
            return 28
    else:
        return 0

# Validate input text file ########################################################################
def validateInputTextFile():
	# Read the file contents
    fileName = getDraggablePath("What file do you want to validate?")
    
    startTime = time.perf_counter()
    
    file = open(fileName, "r")
    allLines = file.readlines()
    file.close()

    errors = [] # where all error messages will be stored

    # Combine into one string
    allText = ""
    for line in allLines:
        allText += line
    
    # Split into days
    days = allText.split("---")
    
    # Check on days
    if len(days) < 28 or len(days) > 31:
        errors.append(f"Invalid number of days; {len(days)} days detected")

    # Check each day
    dayNum = 0
    for day in days:
        dayNum += 1
        
        # Split into sections
        sections = day.split("-s-")
        # Check number of sections
        if len(sections) != 11:
            errors.append(f"Invalid number of sections for day {dayNum}: {len(sections)} sections")
        # Check devotion processing
        else:
            # Clean the sections
            for i in range(len(sections)):
                sections[i] = cleanParagraph(sections[i])
            
            # Devotion cleaning
            cleanDevotion = []
            paragraphs = sections[6].split("</>")
            for paragraph in paragraphs:
                cleanDevotion.append(paragraph)
            devotionText = genDevotion(cleanDevotion)
            
            # Check devotion
            if devotionText[len(devotionText) - 1] != "。":
                errors.append(f"Devotion for day {dayNum} ends in a character that is not \"。\"")
    
    # Print errors
    errorNum = 0
    for error in errors:
        errorNum += 1
        print(f"Error {withLeadingZeros(errorNum, 3)}: {error}")
    
    endTime = time.perf_counter()
    
    # Print validation message
    if len(errors) == 0:
        print("Validation successful; No errors were detected")
    print(f"Validation completed in {round(endTime-startTime,5)} seconds")    

# Generate devotion data from input ###############################################################
# Creates and returns a list of  devotion objects from the input in the specified file
def createDevotionObjectsFromInput(fileName):
    allDevotions = []
    
    file = open(fileName, "r")
    allLines = file.readlines()
    file.close()
    
    # Combine into one string
    allText = ""
    for line in allLines:
        allText += line
        
    # Split into days
    days = allText.split("---")
    
    # Process each day
    for day in days:
        # Split into sections
        sections = day.split("-s-")
        # Clean the sections
        for i in range(len(sections)):
            sections[i] = cleanParagraph(sections[i])
        
        # Devotion cleaning
        cleanDevotion = []
        paragraphs = sections[6].split("</p>")
        for paragraph in paragraphs:
            cleanDevotion.append(paragraph)
        devotionText = genDevotion(cleanDevotion)
        
        # Create the devotion object
        devotion = Devotion(sections[0], sections[1], sections[2], sections[3], sections[4], sections[5], devotionText, sections[7], sections[8], sections[9], sections[10])
        allDevotions.append(devotion)
    
    return allDevotions

# Generates output in the old data format
def generateOldDevotionDataFromInput():
    # Read the file contents
    month = int(input("What month is this for?\nInput as number: "))
    year = int(input("What year is it?\nInput as number: "))
    fileName = getDraggablePath("What file do you want to process?")
    folderPath = getDraggablePath("What folder should the results go into?")
    
    startTime = time.perf_counter()
    
    allDevotions = createDevotionObjectsFromInput(fileName)

    # Add all data to a results file
    file = createTextFile(f"{year}-{withLeadingZeros(month,2)}", folderPath)
    for devotion in allDevotions:
        delim = '^'
        file.write(devotion.date + delim + devotion.japaneseDate + delim + devotion.title + delim + devotion.bibleReading + delim + devotion.biblePassage + delim + devotion.bibleText + delim + devotion.devotionText + delim + devotion.prayer + delim + devotion.thought + delim + devotion.prayerFocus + delim + devotion.author + "_")
    file.close()
    
    # Print validation message
    endTime = time.perf_counter()
    print(f"Output generated in {round(endTime-startTime,5)} seconds")

# Generate json devotion data from input
def generateJSONfromInput():
    # Read the file contents
    month = int(input("What month is this for?\nInput as number: "))
    year = int(input("What year is it?\nInput as number: "))
    fileName = getDraggablePath("What file do you want to process?")
    folderPath = getDraggablePath("What folder should the results go into?")
    
    startTime = time.perf_counter()
    
    allDevotions = createDevotionObjectsFromInput(fileName)
    
    # Extract the dictionaries
    listOfDicts = []
    for devotion in allDevotions:
        listOfDicts.append(devotion.dict)
    
    # Output to JSON
    # jsonOutput = json.dumps(listOfDicts, indent=4, ensure_ascii=False).encode('utf8')
    
    # Add to result file
    file = createJSONFile(f"{year}-{withLeadingZeros(month,2)}", folderPath)
    json.dump(listOfDicts, file, indent=4, ensure_ascii=False)
    file.close()
    
    # Print validation message
    endTime = time.perf_counter()
    print(f"Output generated in {round(endTime-startTime,5)} seconds")

# Cleans a paragraph of text
def cleanParagraph(paragraph):
	p = paragraph
	for char in characterBlacklist:
		p = p.replace(char, '')

	return p

# Generate a string for a devotion that is split into paragraphs
def genDevotion(devotion):
	result = ""
	
	for paragraph in devotion:
		result += paragraph + "|" 
	
	result = result[:-1]
	
	return result

main()