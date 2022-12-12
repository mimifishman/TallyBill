from multiprocessing.connection import Client
from veryfi import Client
import pprint
import json
from bidi import algorithm 
from langdetect import detect
from googletrans import Translator
from ipdata import IPData

def get_ip_currency(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    elif request.META.get('HTTP_X_REAL_IP'):        
        ip = request.META.get('HTTP_X_REAL_IP')    
    else:
        ip = request.META.get('REMOTE_ADDR')         
    ipd = IPData('e746ebdfefa52a544a343bce00d69acd2a4cc4cc205253ecbb8fa999')
    try:
        response = ipd.lookup(ip)
        currency_symbol = response['currency']['symbol']
    except ValueError as e:  
        currency_symbol = '$'
    return currency_symbol    


# Function to reverse words of string   
def rev_sentence_word(sentence): 
    # change letters to RTL   
    sentence = algorithm.get_display(sentence)
    sentence = sentence.replace('\n',' ')    
    return sentence 

def veryfi(file_path): 
    # # veryfi client information
    client_id = 'vrfjMpUekCvNsJ2OkgBc24d45Rug9clEZNXU8Bv'
    client_secret = 'e68trrF9a07d0MEFI5NT6cGcHUwUXboXtVzGpV6mE4ytHN2TUFg792guRgCL6DHtHW9pJA1WzLlPX1J5fdyzbWlgvYopMTwdAGNVeVuc40ke8J4HEDevMSTkZCg3OIGj'
    username = 'mimi.fishman'
    api_key = 'fd9accff3ece9a80e9fb7ba0c9f97319'

    # # set receipt categories
    categories = ['Restaurant']
    # # set file path
    file_path = file_path

    # # This submits document for processing (takes 3-5 seconds to get response)
    veryfi_client = Client(client_id, client_secret, username, api_key)
    response = veryfi_client.process_document(file_path, categories=categories)


    # pprint.pprint(response["line_items"])

    # # save the json data to a file 
    # with open('json_data.json', 'w', encoding='utf-8') as outfile:     
    #     json.dump(response, outfile, indent=4, ensure_ascii=False)

    # # open the json data
    # with open('json_data.json', encoding='utf-8') as json_file:
    #     data = json.load(json_file)

    # create the translator
    # translator = Translator()   

    # get the line items
    # for line in response["line_items"]: 
    #     description = line["description"].replace('\n',' ')
    #     # detect the language 
    #     lang = detect(description) 
    #     # reverse the description if lang = hebrew and translate to english  
    #     if lang == 'he':
    #         desc = rev_sentence_word(description)        
    #         eng_desc = translator.translate(description, src = lang, dest = 'en').text
    #     else:
    #         desc = description
    #         eng_desc = description

    #     # print the line items
    #     print( response["id"], response["date"], response["currency_code"],line["id"], line["order"], desc, eng_desc,
    #     line["quantity"], line["price"], line["total"] )

    return response 
