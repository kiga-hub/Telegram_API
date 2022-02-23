import csv
import socks
import os
import configparser
import socks
import socket
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.tl.types import (
    PeerChannel
)

# import asyncio
# asyncio.set_event_loop(asyncio.SelectorEventLoop())

config = configparser.ConfigParser()
path = './tgconfigure.ini'
config.read(path)

print(config.get('proxy','server'))

# socks.set_default_proxy(socks.HTTP, config.get('proxy','server'), config.getint('proxy','port'))
# socket.socket = socks.socksocket

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

def banner():
    print(f"""
{re}Check api_id & api_hash first 
{gr}Set socks5 
{cy}Start!
        """)
    
api_id = config.getint('api','api_id')
api_hash = config.get('api','api_hash')
api_hash = str(api_hash)

phone = config.get('api','phone')

proxy = (socks.HTTP, config.get('proxy','server'), config.getint('proxy','port'))
# Create the client and connect
client = TelegramClient(phone, api_id, api_hash,proxy=proxy)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    banner()
    client.sign_in(phone, input(gr+'[+] Enter the code: '+re))
os.system('clear')

banner()
chats = []
last_date = None
chunk_size = 20000
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
 
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
 
print(gr+'[+] Choose a group to scrape members :'+re)
i=0
for g in groups:
    print(gr+'['+cy+str(i)+']' + ' - ' + g.title)
    i+=1
 
print('')
g_index = input(gr+"[+] Enter a Number : "+re)

target_group=groups[int(g_index)]

# target_group = 'Test'
friend_info = client.get_entity(target_group)
channel_id = friend_info.id
channel_title = friend_info.title


async def main(phone):
    await client.start()
    print("Client Created")
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()
    print(me)

    entity = PeerChannel(int(channel_id))

    my_channel = await client.get_entity(entity)

    offset = 0
    limit = 100
    all_participants = []
    dict = {}
    #queryKey = ['!','@','#','$','%','^','&','*','(',')','_','+','-','=','0','1','2','3','4','5','6','7','8','9','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    queryKey = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    #queryKey = ['']
    for key in queryKey:
        offset = 0
        limit = 100
        while True:
            participants = await client(GetParticipantsRequest(
                my_channel, ChannelParticipantsSearch(key), offset, limit,
                hash=0
            ))
            if not participants.users:
                break
            # all_participants.extend(participants.users)
            # all_participants.sort
            for user in participants.users:
                dict[user.id] = user
            #     # all_participants.append(user)
            #     # print(re.findall(r"\b[a-zA-Z]", user.first_name)[0].lower())
            #     all_participants.append(user)
                # try:
                #     if user.first_name[0].lower() == key:
                #         # all_participants.extend(participants.users)
                #         print(user)
                #         all_participants.append(user)
        
                # except:
                #     pass

            offset += len(participants.users)
            print('check search: '+str(offset))


    # for participant in all_participants:
    #     dict[participant.id] = participant
            
            
    with open("./"+str(channel_title)+"_"+str(channel_id)+".csv","w",encoding='UTF-8') as f:
        writer = csv.writer(f,delimiter=",",lineterminator="\n")
        writer.writerow(['id', 'username'])
        # count = 0
        for key in dict: 
            print(dict[key].username)
            writer.writerow([dict[key].id,dict[key].username])
            #writer.writerow([dict[key].id,dict[key].first_name,dict[key].last_name,dict[key].username,dict[key].phone,dict[key].bot])


with client:
    client.loop.run_until_complete(main(phone))