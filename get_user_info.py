#coding=utf-8

import itchat
import json
import codecs

sex_dict = {}
sex_dict['0'] = "其他"
sex_dict['1'] = "男"
sex_dict['2'] = "女"

#下载好友头像
def download_images(frined_list):
    image_dir = "../images/"
    num = 1
    for friend in frined_list:
        image_name = str(num)+'.jpg' #给头像命名
        num+=1
        img = itchat.get_head_img(userName=friend["UserName"])
        with open(image_dir+image_name, 'wb') as file: ##写入图片
            file.write(img)

def save_data(frined_list):
    out_file_name = "../data/friends.json"
    with codecs.open(out_file_name, 'w', encoding='utf-8') as json_file:    #解决打开时的编码问题
        json_file.write(json.dumps(frined_list,ensure_ascii=False)) #将Python文件转换成json

#定义指定回复的触发队列
message_dict = {
    "狗子":"么么哒",
    "你好":"你好啊，这条消息是自动回复的。"
}
@itchat.msg_register(itchat.content.TEXT)
#itchat的注册命令
#可选参数
# 图片对应itchat.content.PICTURE
# 语音对应itchat.content.RECORDING
# 名片对应itchat.content.CARD
def print_content(msg):
    NickName = msg['User']['NickName']
    user = itchat.search_friends(name=NickName)[0]
    text = msg['Text']
    if text in message_dict.keys():
        user.send(message_dict[text])
    else:
        user.send(u"你好啊%s,我目前还不支持这个功能"%NickName)

# import itchat
#
# @itchat.msg_register(itchat.content.TEXT)
# def print_content(msg):
#     print(msg['Text'])
#
# itchat.auto_login()
# itchat.run()

if __name__ == '__main__':
    itchat.auto_login()
    
    friends = itchat.get_friends(update=True)[0:]#获取好友信息

    friends_list = [] #将微信好友列表里的相关信息
    for friend in friends: #用一层循环获取列表里friend的基本信息
        item = {}
        item['NickName'] = friend['NickName']
        item['HeadImgUrl'] = friend['HeadImgUrl']
        item['Sex'] = sex_dict[str(friend['Sex'])]
        item['Province'] = friend['Province']
        item['Signature'] = friend['Signature']
        item['UserName'] = friend['UserName']

        #print(item)

    save_data(friends_list)
    download_images(friends_list)


    user = itchat.search_friends(name=u'杜温鑫🐽')[0]
    user.send(u'hello,这是一条来自机器人的消息')
    itchat.run()
