import json, os
from difflib import get_close_matches                                           #to predict matching words if user gives wrong spelling

Data = json.load(open("dict_data.json"))                         #Loading the data containing words and their meanings/definitions

def meaning(word):
    if word in Data.keys():
        return Data[word]
    else:  
        similarWords = get_close_matches(query, Data.keys(), cutoff = 0.75)

        if len(similarWords) > 0:
            print("Did you mean %s instead?" %(similarWords[0]))
            confirm = input("Enter Y for Yes any other key for No: ")

            if confirm.lower() == 'y':
                meanings = resolveWord(similarWords[0])
                return (meanings)
            else:
                return ('I am sorry, " %s " is not in my dictionary' %query)
        else:
            return ('I am sorry, " %s " is not in my dictionary' %query)


    
query = input("Enter word/phrase: ")
meanings = meaning(query.lower())

if type(meanings)==list:
    for j in meanings:
        print(j)
else:
    print(meanings)
