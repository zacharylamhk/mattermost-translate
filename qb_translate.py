from mattermostdriver import Driver
import json
import langid
import chinese_converter

from deep_translator import GoogleTranslator
#print(GoogleTranslator(source='auto', target='de').translate("keep it up, you are awesome"))

team="secondteam"

mm = Driver({
    'url': 'mattermost.quebico.com',
    "token":"8tqjou18cpgpjd8iuu7tfjui4r",
    'scheme': 'https',
    'port': 443
    })
mm.login()
channel=["it-log","it-support"]
last_id=""
translate_breake="\n\n\n\n\n"

async def my_event_handler(e):
    global last_id,team

    message=json.loads(e)
    try :
        event=message['event']
    except :
        event="ok"
    if event=="posted" or event=="post_edited":
        print("Create or Edit Post")
        j=json.loads(message['data']['post'])
        post_id=j['id']
        if j['message'].find("MatterMostTranslate:")>-1:
            chunks = j['message'].split(' ')
            #translate(chunks[3],chunks[1],chunks[2])
        else:
						if post_id!=last_id:
                print("Message ID:" +post_id)
                print("Last ID:"+last_id)
                raw_message=j['message']

                #filter translated message
                message_end=j['message'].find(translate_breake)
                if message_end==-1:
                    source_message=j['message']
                else:
                    source_message=j['message'][:message_end]
                print(source_message)

                #get message language
                lang=langid.classify(j['message'])
                msg=source_message+""+translate_breake
                source_message=source_message.replace("\n\n","\n")

                #add translate signature
                msg+="MatterMostTranslate:\n\n"
                if lang[0].find('en')==-1:
                    msg+=">🇬 🇧 "  +GoogleTranslator(source='auto', target='en').translate(source_message.replace("@",""))+"\n\n"
                if lang[0].find('zh')==-1:
                    msg+=">🇹 🇼 "  +chinese_converter.to_traditional(GoogleTranslator(source='auto', target='zh-TW').translate(source_message.replace("@","")))+"\n\n"
                if lang[0].find('ja')==-1:
                    msg+=">🇯 🇵 "  +GoogleTranslator(source='auto', target='ja').translate(source_message.replace("@",""))+"\n\n"
                msg+="\n\n"
                try:
                    channel_type=message['data']['channel_type']
                except:
                    channel_type="F"


                if channel_type=="D":
                    channel_name=message['data']['channel_name']
                    channel=mm.channels.get_channel_by_name_and_team_name(team, channel_name)
                    channel_id=channel['id']
                    mm.posts.create_post(options={
                        'channel_id': channel_id,
                        'message': msg,
                        'root_id': post_id
                    })

                else:
                    mm.posts.update_post(post_id,options={
                        'message': msg,
                        'id':post_id
                    })

                last_id=post_id
            else :
last_id=""

mm.init_websocket(my_event_handler)