from twilio.rest import Client 


account_sid = 'AC6fef09b4af2e0d882ad3370a10c354db' 
auth_token = 'f86f30b6b825dbb2c41a5d7dccb4a8d4' 
client = Client(account_sid, auth_token) 

def auto_message():
    tmp = ""
    with open('./message.txt', 'r+') as f:
        data = f.readlines() 
        tmp = data[0]
        f.close()
    with open('./message.txt', 'w+') as f:
        f.write(data[1])
        f.writelines(data[2:]) 
        f.close()
    message = client.messages.create( 
                              from_='whatsapp:+14155238886',  
                              body= "Hi today's problem: *"+tmp[:-1]+"*",      
                              to='whatsapp:+919492973997' 
                          ) 
    print(message.sid)


