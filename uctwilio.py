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
        messageBody = message.content.replace('<@&403060533017837569>', '@Hundy Chaser')
        messageBody += ('\n- tagged by ' + message.author.name + ' in #' + message.channel.name)

        for num in nums:
            twilioMessage = twilioClient.messages.create(
                    body=messageBody,
                    from_=environ['from'],
                    to=num
                )
            totalMessagesSent += 1

        print('message sent by ' + message.author.name + ', content: ' + message.content + ' - twilioMessage.sid -> ' + str(twilioMessage.sid))
        pyrebase_worker.log("SMS sent. Contents: " + messageBody)
        status = 'Successfully sent ' + str(totalMessagesSent) + ' messages.'
         
    except Exception as e:
        status = "ERROR!"
        print('ERROR sending twilio report! -> ' + str(e))
    finally:
        return 'Done: report3TS()  -  Status: ' + status




def reportAqua(message):
    status = 'Tagged'
    totalMessagesSent = 0
    try:
        status = 'Connected'
        print('calling twilio api..')
        nums = pyrebase_worker.getByServer("Team Aqua's Hideout")
        messageBody = message.content.replace('<@&398995832978014210>', '@HundyHunters')
        messageBody += ('\n- tagged by ' + message.author.name + ' in #' + message.channel.name)

        for num in nums:
            twilioMessage = twilioClient.messages.create(
                    body=messageBody,
                    from_=environ['from'],
                    to=num
                )
            totalMessagesSent += 1

        print('message sent by ' + message.author.name + ', content: ' + message.content + ' - twilioMessage.sid -> ' + str(twilioMessage.sid))
        pyrebase_worker.log("SMS sent. Contents: " + messageBody)
        status = 'Successfully sent ' + str(totalMessagesSent) + ' messages.'
         
    except Exception as e:
        status = "ERROR!"
        print('ERROR sending twilio report! -> ' + str(e))
    finally:
        return 'Done: reportAqua()  -  Status: ' + status






def check():
    twilioMessage = twilioClient.messages.create(
        body="Twilio check! Bot is working fine.",
        from_=environ['from'],
        to=environ['adminPhone']
    )
    print("twilioMessage.sid from twilio check " + str(twilioMessage.sid))
    return "Check is working fine!\ntwilioMessage.sid from twilio check -> " + str(twilioMessage.sid)