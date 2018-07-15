from os import environ
from twilio.rest import Client
import pyrebase_worker


account_sid = environ['account_sid']
auth_token = environ['auth_token']
twilioClient = Client(account_sid, auth_token)


def report3TS(message):
    status = 'Tagged'
    totalMessagesSent = 0
    try:
        status = 'Connected'
        print('calling twilio api..')

        nums = pyrebase_worker.getByServer("BCS Pokemon Go")  

        for num in nums:
            twilioMessage = twilioClient.messages.create(
                    body=message.content + '\n- tagged by ' + message.author.name \
                        + ' in #' + message.channel.name + '\n(' + message.server.name + ')',
                    from_=environ['from'],
                    to=num
                )
            totalMessagesSent += 1

        print('message sent by ' + message.author.name + ', content: ' + message.content + ' - twilioMessage.sid -> ' + str(twilioMessage.sid))

        status = 'Successfully sent ' + str(totalMessagesSent) + ' messages.'
         
    except Exception as e:
        status = "ERROR!"
        print('ERROR sending twilio report! -> ' + str(e))
    finally:
        return 'Done: ' + status




def reportAqua(message):
    status = 'Tagged'
    totalMessagesSent = 0
    try:
        status = 'Connected'
        print('calling twilio api..')

        nums = pyrebase_worker.getByServer("Team Aqua's Hideout")

        for num in nums:
            twilioMessage = twilioClient.messages.create(
                    body=message.content + '\n- tagged by ' + message.author.name \
                        + ' in #' + message.channel.name + '\n(' + message.server.name + ')',
                    from_=environ['from'],
                    to=num
                )
            totalMessagesSent += 1

        print('message sent by ' + message.author.name + ', content: ' + message.content + ' - twilioMessage.sid -> ' + str(twilioMessage.sid))

        status = 'Successfully sent ' + str(totalMessagesSent) + ' messages.'
         
    except Exception as e:
        status = "ERROR!"
        print('ERROR sending twilio report! -> ' + str(e))
    finally:
        return 'Done: ' + status






def check():
    twilioMessage = twilioClient.messages.create(
        body="Twilio check! Bot is working fine.",
        from_=environ['from'],
        to=environ['j']
    )
    print("twilioMessage.sid from twilio check " + str(twilioMessage.sid))