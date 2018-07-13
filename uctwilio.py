from os import environ
from twilio.rest import Client

def report(message):
    status = 'Tagged'
    totalMessagesSent = 0
    try:
        account_sid = environ['account_sid']
        auth_token = environ['auth_token']
        twilioClient = Client(account_sid, auth_token)
        status = 'Connected'
        print('calling twilio api..')
        twilioMessage = twilioClient.messages.create(
                body= ':100: :100: :100:\n' + message.content + '\n- tagged by ' + message.author.name \
                    + ' in #' + message.channel.name + ' (' + message.server.name + ')',
                from_=environ['from'],
                to=environ['to']
            )
        totalMessagesSent += 1
        print('message sent by ' + message.author.name + ', content: ' + message.content + ' - twilioMessage.sid -> ' + str(twilioMessage.sid))

                

        status = 'Successfully sent ' + str(totalMessagesSent) + ' messages.'
       
       
    except Exception as e:
        status = "ERROR!"
        print('ERROR sending twilio report! -> ' + str(e))
    finally:
        return 'Done: ' + status