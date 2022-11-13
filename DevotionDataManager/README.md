# README

# Documentation
## 1 Create template text file
Creates a new text file. This text file is where text from the PDF can be copy-pasted into for further processing.

## 2 Validate input text file
Parses an input text file to see if it has all the fields filled out.

## 3 Generate devotion data from input
Takes a validated text file as input, and creates the output text file with the compressed devotion data. Can generate data in various formats.

### 3.1 Generate json format
Generates an output text file as a json file. This is meant to be easy to read as a human. It is also easy to use in the Swift environment.

### 3.2 Generate old format
Generates an output text file in the old format. The old format has non-standard dividing characters, and is hard to interpret as a human. This output is kept just in case it is needed, but is not intended to be used frequently.

# Development
## Standard order of input data
*last updated Nov. 12th, 2022*
```
- 00: Date
- 01: JapaneseDate
- 02: Title
- 03: BibleReading
- 04: BiblePassage
- 05: BibleText
- 06: DevotionText
- 07: Prayer
- 08: Thought
- 09: PrayerFocus
- 10: Author
```
