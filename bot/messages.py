import client


def Messages(user):

    if client.getUserLanguage(user)=="RU":
    
        MESSAGES = {
            "justStarted" : client.getMessage(number=1),
            
        }
            

    return MESSAGES
