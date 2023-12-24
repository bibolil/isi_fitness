from bardapi import Bard
import bardapi

def bard_output(recommandation):    
    file_path = 'query.txt'  
    with open(file_path, 'r') as file:
        query_header = file.read()
    Bard_query=""
    for i in range(len(recommandation)):
        Bard_query+=str(recommandation[i])+"\n"
    token="xxxxxxxxxxx"
    try:
        bard = Bard(token=token)
    except Exception as e:
        print(e)
        return "Error: Token expired"
    input_text=query_header+"\n"+Bard_query
    # Send an API request and get a response.
    try:
        response = bardapi.core.Bard(token).get_answer(input_text)
    except Exception as e:
        print(e)
        return "Error: Token expired"
    # Print the response.
    return response["content"]