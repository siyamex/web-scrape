from bs4 import BeautifulSoup
import requests
import xlsxwriter

# Create a new Excel file
excel = xlsxwriter.Workbook('Dhivehi Dictionary.xlsx')

# Create a new worksheet and set the column widths
sheet = excel.add_worksheet('Words')
sheet.set_column('A:A', 30)
sheet.set_column('B:B', 100)

# Add the column headers
sheet.write('A1', 'Words')
sheet.write('B1', 'Meaning')

try:
    # Make a request to the website
    source = requests.get('https://www.hassanhameed.com/dhivehi-language/a-english-dhivehi-dictionary/')
    source.raise_for_status()

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(source.text, 'html.parser')
    
    # Find all the <p> tags with class "definition"
    definition_tags = soup.find_all('p', class_='definition')
    
    # Create a dictionary to store the meanings for each headword
    meanings_dict = {}
    
    # Loop through each <p> tag and extract the text
    for definition_tag in definition_tags:
        # Find the previous sibling tag with class "headword"
        headword_tag = definition_tag.find_previous_sibling('p', class_='headword')
        
        # Extract the word and definition
        word = headword_tag.text.strip()
        definition = definition_tag.text.strip()
        
        if word in meanings_dict:
            # If the word is already in the dictionary, append the new definition
            meanings_dict[word].append(definition)
        else:
            # If the word is not in the dictionary, create a new entry with the definition
            meanings_dict[word] = [definition]
        
    # Loop through the meanings dictionary and write the words and meanings to the worksheet
    for index, (word, definitions) in enumerate(meanings_dict.items()):
        meaning = '; '.join(list(set(definitions))) # remove duplicates
        sheet.write(index + 1, 0, word)
        sheet.write(index + 1, 1, meaning)

except Exception as err:
    print(err)
    
finally:
    # Close the Excel file
    excel.close()
