#!/usr/bin/python
# -*- coding: UTF-8 -*-

# enable debugging
################

'''
Bot version: 1.1.2
Made by Hito
'''

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import time
from datetime import datetime

token = "VK API TOKEN REMOVED"
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


user_cmds = ["Создать тикет"]
moder_cmds = ["Список админов -> !админы", "Список открытых тикетов -> #list", "Список забаненых пользователей -> !banlist"]
admin_cmds = ["Добавить модера -> +модер", "Удалить модера -> -модер", "Забанить пользователя -> !ban", "Разбанить пользователя -> !unban"]
grandAdmin_cmds = ["Добавить админа -> +админ", "Удалить админа -> -админ"]

#Hito - 126345141
#Александр Тихонов - 273406837
grandAdmins = [126345141]
admins = []
moderators = []

all_staff = grandAdmins + admins + moderators
grandStaff = admins + grandAdmins

#Проверка модераторами тикетов
message_replying = dict()

#Этапы диалога
first_step = []
second_step = []
third_step = []

#тема, текст и окончательное сообщение тикета
message_theme = dict()
message_text = dict()
message_finished_text = dict()

#Список забаненых
banned_users = []


def errors_caused(user_id, typeOfError):
    if typeOfError == "NoPerms":
        vk_session.method("messages.send", {"peer_id": user_id, "message": "У Вас нет прав для использования данной комманды!", "random_id": 0})
        return 1
    if typeOfError == "CantBan":
        vk_session.method("messages.send", {"peer_id": user_id, "message": "Нельзя забанить данного пользователя!", "random_id": 0})
        return 1

def getCommands(user_id):
    allowed_cmds_string = ""
    for grandAdmin in grandAdmins:
        if user_id == grandAdmin:
            for command in user_cmds:
                allowed_cmds_string += (" - " + str(command) + "\n")
            for command in moder_cmds:
                allowed_cmds_string += (" - " + str(command) + "\n")
            for command in admin_cmds:
                allowed_cmds_string += (" - " + str(command) + "\n")
            for command in grandAdmin_cmds:
                allowed_cmds_string += (" - " + str(command) + "\n")
            vk_session.method("messages.send", {"peer_id": user_id,
                                                "message": "Непонятная команда!\n\nСписок доступных команд:\n" + allowed_cmds_string,
                                                "random_id": 0})
            return 1
    for admin in admins:
        if user_id == admin:
            for command in user_cmds:
                allowed_cmds_string += (" - " + str(command) + "\n")
            for command in moder_cmds:
                allowed_cmds_string += (" - " + str(command) + "\n")
            for command in admin_cmds:
                allowed_cmds_string += (" - " + str(command) + "\n")
            vk_session.method("messages.send", {"peer_id": user_id, "message": "Непонятная команда!\n\nСписок доступных команд:\n" + allowed_cmds_string, "random_id": 0})
            return 1
    for moder in moderators:
        if user_id == moder:
            for command in user_cmds:
                allowed_cmds_string += (" - " + str(command) + "\n")
            for command in moder_cmds:
                allowed_cmds_string += (" - " + str(command) + "\n")
            vk_session.method("messages.send", {"peer_id": user_id, "message": "Непонятная команда!\n\nСписок доступных команд:\n" + allowed_cmds_string, "random_id": 0})
            return 1
    #Если пользователь не стафф
    for command in user_cmds:
        allowed_cmds_string += (" - " + str(command) + "\n")
    vk_session.method("messages.send", {"peer_id": user_id, "message": "Непонятная команда!\n\nСписок доступных команд:\n" + allowed_cmds_string, "random_id": 0})
    return 1

#Указание темы сообщения

def add_to_first_step(user_id):
    first_step.append(user_id)
    print("Для ID ["+str(user_id) + "] была присвоена 1 стадия.")
def del_from_first_step(user_id):
    for i in first_step:
        if user_id == i:
            first_step.remove(i)
            print("У ID ["+str(user_id)+"] удалена 1 стадия.")
def check_first(user_id, msg_theme):
    for i in first_step:
        if user_id == i:
            msg_theme = (msg_theme[:20] + '..') if len(msg_theme) > 20 else msg_theme
            message_theme[str(user_id)] = msg_theme
            vk_session.method("messages.send", {"peer_id": user_id, "message": "Вы установили тему своего тикета. Теперь укажите текст своего тикета.", "random_id": 0})
            del_from_first_step(user_id=user_id)
            add_to_second_step(user_id=user_id)
            return 1
    return 0

#Указание текста сообщения

def add_to_second_step(user_id):
    second_step.append(user_id)
    print("Для ID ["+str(user_id) + "] была присвоена 2 стадия.")

def del_from_second_step(user_id):
    for i in second_step:
        if user_id == i:
            second_step.remove(i)
            print("У ID ["+str(user_id)+"] удалена 2 стадия.")
def check_second(user_id,msg_text, msg_id):
    for i in second_step:
        if user_id == i:
            message_text[str(user_id)] = msg_text
            message_replying[str(user_id)] = msg_id
            message_finished_text[str(user_id)] = "Тема: " + message_theme[str(user_id)] + "\nСообщение: " + message_text[str(user_id)]
            vk_session.method("messages.send", {"peer_id": user_id, "message": "Ваш тикет подготовлен к отправке!\n"+message_finished_text[str(user_id)]+"\n\n\nДля отправки тикета модераторам, напишите 'отправить'\nДля отмены, отправьте любое другое сообщение.", "random_id": 0})
            del_from_second_step(user_id=user_id)
            add_to_third_step(user_id=user_id)
            return 1
    return 0

#Проверка отправки сообщения

def add_to_third_step(user_id):
    third_step.append(user_id)
    print("Для ID ["+str(user_id) + "] была присвоена 3 стадия.")
def del_from_third_step(user_id):
    for i in third_step:
        if user_id == i:
            third_step.remove(i)
            print("У ID ["+str(user_id)+"] удалена 3 стадия.")
def check_third(user_id, confirmation):
    for i in third_step:
        if user_id == i:
            user = vk_session.method("users.get", {"user_ids": user_id})
            if(confirmation.lower() == "отправить"):
                vk_session.method("messages.send", {"peer_id": i, "message": "Ваш тикет #"+str(message_replying[str(user_id)])+" был отправлен модераторам. В скором времени вам придет ответ.", "random_id": 0})
                for staff in all_staff:
                    vk_session.method("messages.send", {"peer_id": staff, "forward_messages": message_replying[str(user_id)], "message": "Новый тикет от пользователя @id" + str(user_id)+"(" + user[0]["first_name"] + " " + user[0]["last_name"]+")(#"+str(message_replying[str(user_id)])+")"+"\n"+message_finished_text[str(user_id)].split("\nСообщение: ")[0] + "\nДля ответа на этот тикет, напишите #"+str(message_replying[str(user_id)])+" и на следующей строке оставьте ответ на тикет.", "random_id": 0})
            else:
                vk_session.method("messages.send", {"peer_id": i, "message": "Тикет успешно отменен.", "random_id": 0})
                message_replying.pop(str(user_id))

            del_from_third_step(user_id=user_id)
            return 1
    return 0

#Проверка на наличие открытых тикетов
def check_has_ticket(user_id):
    for i in message_replying.keys():
        if str(i) == str(user_id):
            vk_session.method("messages.send", {"peer_id": user_id, "message": "У Вас уже есть открытый тикет!", "random_id": 0})
            return 1
    return 0

#Проверка тикетов модераторами
def moderator_checking(user_id, reply):
    for staff in all_staff:
        if staff == user_id:
            if reply == "#list":
                all_msg_ids = ""
                for i in message_replying.values():
                    all_msg_ids += "  #" + str(i) + "\n"
                vk_session.method("messages.send",
                                  {"peer_id": user_id, "message": "Список открытых тикетов:\n" + all_msg_ids,
                                   "random_id": 0})
                return 1
            try:
                reply_splitted = reply.split("\n")
                #reply_message_recievermsg_id = reply.split("\n")[0]
                reply_message_recievermsg_id = reply_splitted[0].split("#")[1]
                reply_message_recievermsg_body = reply_splitted[1]

                user_to_reply = message_replying.keys()[message_replying.values().index(int(reply_message_recievermsg_id))]

                #######################################ТОЛЬКО ДЛЯ ОТЛАДКИ БЫЛО######################################
                #vk_session.method("messages.send",{"peer_id":user_id,"message": "Список сообщений для ответа\n"+str(message_replying),"random_id":0})
                #vk_session.method("messages.send", {"peer_id": user_id, "message": "Указанный id сообщения\n" + reply_message_recievermsg_id, "random_id": 0})
                #vk_session.method("messages.send", {"peer_id": user_id, "message": "Пара из message_replying\n" + str(user_to_reply), "random_id": 0})
                ####################################################################################################

                moder_info = vk_session.method("users.get", {"user_ids": user_id})
                message_replying.pop(str(user_to_reply))
                vk_session.method("messages.send",
                                  {"peer_id": user_to_reply,
                                   "message": "Модератор ответил на Ваш тикет #" + reply_message_recievermsg_id +"\n\n"+ str(reply_message_recievermsg_body) + "\n======\nС уважением, @id" + str(user_id) + "(" + moder_info[0]["first_name"] + " " + moder_info[0]["last_name"] + ")",
                                   "random_id": 0})
                for i in all_staff:
                    vk_session.method("messages.send", {"peer_id": i, "message": "@id" + str(user_id) + "(" + moder_info[0]["first_name"] + " " + moder_info[0]["last_name"] + ")"  + " закрыл тикет #" + reply_message_recievermsg_id, "random_id": 0})
            except:
                vk_session.method("messages.send", {"peer_id": user_id, "message": "Введено неверные данные!\nПросмотреть список тикетов: \n - #list", "random_id": 0})
            return 1
    errors_caused(user_id, "NoPerms")
    return 0


#Добавление модератора
def add_moder(user_id, moder_id):
    for i in grandStaff:
        if i == user_id:
            try:
                moder_id = moder_id[7:]
                newModer_info = vk_session.method("users.get", {"user_ids": int(moder_id)})
                admin_info = vk_session.method("users.get", {"user_ids": int(user_id)})

                for moder in moderators:
                    if int(moder_id) == moder:
                        vk_session.method("messages.send", {"peer_id": i, "message": "@id" + str(moder_id) + "(" + newModer_info[0]["first_name"] + " " + newModer_info[0]["last_name"] + ")" + " уже есть в списке модераторов!", "random_id": 0})
                        return 1
                moderators.append(int(moder_id))
                for grand in all_staff:
                    vk_session.method("messages.send", {"peer_id": grand, "message": "@id" + str(moder_id) + "(" + newModer_info[0]["first_name"] + " " + newModer_info[0]["last_name"] + ")" + " добавлен в список модераторов администратором " + "@id" + str(user_id) + "(" + admin_info[0]["first_name"] + " " + admin_info[0]["last_name"] + ")", "random_id": 0})
                return 1
            except:
                vk_session.method("messages.send", {"peer_id": user_id, "message": "Пример использования команды:\n+модер 126345141", "random_id": 0})
            return 1
    errors_caused(user_id, "NoPerms")
    return 0
#Удаление модератора
def remove_moder(user_id, moder_id):
    for i in grandStaff:
        if i == user_id:
            try:
                moder_id = moder_id[7:]

                oldModer_info = vk_session.method("users.get", {"user_ids": int(moder_id)})
                admin_info = vk_session.method("users.get", {"user_ids": int(user_id)})

                moderators.remove(int(moder_id))
                for grand in all_staff:
                    vk_session.method("messages.send", {"peer_id": grand,
                                                        "message": "@id" + str(moder_id) + "(" + oldModer_info[0]["first_name"] + " " + oldModer_info[0]["last_name"] + ")" + " удален из списка модераторов администратором " + "@id" + str(user_id) + "(" + admin_info[0]["first_name"] + " " + admin_info[0]["last_name"] + ")",
                                                        "random_id": 0})
            except:
                vk_session.method("messages.send", {"peer_id": user_id, "message": "Пользователя с ID [" + moder_id + "] нет в списке модераторов!\n\nПример использования команды:\n-модер 126345141", "random_id": 0})
            return 1
    errors_caused(user_id, "NoPerms")
    return 0

#####ТОЛЬКО ДЛЯ ГЛ АДМИНИСТРАТОРОВ#####

#Добавление администратора
def add_admin(user_id, admin_id):
    for grandAdmin in grandAdmins:
        if user_id == grandAdmin:
        #try:
            admin_id = admin_id[7:]
            print("Выдача админки для ID" + str(admin_id) + " гл админом " + str(user_id))
            for moder in moderators:
                if int(admin_id) == moder:
                    print("У " + str(admin_id) + " обнаружена модерка. Снятие...")
                    moderators.remove(int(admin_id))
                    print("Модерка снята!\n")
            newAdmin_info = vk_session.method("users.get", {"user_ids": int(admin_id)})
            grandAdmin_info = vk_session.method("users.get", {"user_ids": int(user_id)})
            for admin in admins:
                if int(admin_id) == admin:
                    vk_session.method("messages.send", {"peer_id": user_id, "message": "@id" + str(admin_id) + "(" + newAdmin_info[0]["first_name"] + " " + newAdmin_info[0]["last_name"] + ")" + " уже есть в списке администраторов!", "random_id": 0})
                    admin_adding.remove(user_id)
                    return 1
            admins.append(int(admin_id))
            for grand in grandStaff:
                vk_session.method("messages.send",
                                  {"peer_id": grand, "message": "@id" + str(admin_id) + "(" + newAdmin_info[0]["first_name"] + " " + newAdmin_info[0]["last_name"] + ")" + " добавлен в список администраторов гл.администратором " + "@id" + str(user_id) + "(" + grandAdmin_info[0]["first_name"] + " " + grandAdmin_info[0]["last_name"] + ")",
                                   "random_id": 0})
        #except:
        #    vk_session.method("messages.send", {"peer_id": user_id, "message": "Некорректный ID!\n\nПример использования команды:\n+админ 126345141", "random_id": 0})
            return 1
    errors_caused(user_id, "NoPerms")
    return 0

#Удаление администратора
def remove_admin(user_id, admin_id):
    for i in grandAdmins:
        if i == user_id:
            try:
                admin_id = admin_id[7:]
                oldAdmin_info = vk_session.method("users.get", {"user_ids": int(admin_id)})
                grandAdmin_info = vk_session.method("users.get", {"user_ids": int(user_id)})

                admins.remove(int(admin_id))
                for grand in grandStaff:
                    vk_session.method("messages.send", {"peer_id": grand,
                                                        "message": "@id" + str(admin_id) + "(" + oldAdmin_info[0]["first_name"] + " " + oldAdmin_info[0]["last_name"] + ")" + " удален из списка администраторов Гл.Админом " + "@id" + str(user_id) + "(" + grandAdmin_info[0]["first_name"] + " " + grandAdmin_info[0]["last_name"] + ")",
                                                        "random_id": 0})
            except:
                vk_session.method("messages.send", {"peer_id": user_id, "message": "Пользователя с ID [" + admin_id + "] нет в списке администраторов!\n\nПример использования команды:\n-админ 126345141", "random_id": 0})
            return 1
    errors_caused(user_id, "NoPerms")
    return 0

#получить список админов/модеров
def get_admin_list(user_id):
    for adm in all_staff:
        if user_id == adm:
            AdminsModers_string = "Главные администраторы:\n"
            for grandAdmin in grandAdmins:
                grandAdmin_info = vk_session.method("users.get", {"user_ids": grandAdmin})
                AdminsModers_string += "@id" + str(grandAdmin) + "(" + grandAdmin_info[0]["first_name"] + " " + grandAdmin_info[0]["last_name"] + ")" + "\n"

            AdminsModers_string += "--------------------\nАдминистраторы:\n"
            for admin in admins:
                admin_info = vk_session.method("users.get", {"user_ids": admin})
                AdminsModers_string += "@id" + str(admin) + "(" + admin_info[0]["first_name"] + " " + admin_info[0]["last_name"] + ")" + "\n"

            AdminsModers_string +="---------------------\nМодераторы:\n"
            for moder in moderators:
                moder_info = vk_session.method("users.get", {"user_ids": moder})
                AdminsModers_string += "@id" + str(moder) + "(" + moder_info[0]["first_name"] + " " + moder_info[0]["last_name"] + ")" + "\n"

            vk_session.method("messages.send", {"peer_id": user_id, "message": AdminsModers_string, "random_id": 0})
            return 1
    errors_caused(user_id, "NoPerms")
    return 1

#Бан пользователей
def ban(user_id, banned_id):
    for staff in grandStaff:
        if user_id == staff:
            try:
                banned_id = banned_id[5:]
                for grandAdmin in grandAdmins:
                    if str(banned_id) == str(grandAdmin):
                        errors_caused(user_id=user_id, typeOfError="CantBan")
                        return 1
                for banned in banned_users:
                    if banned == banned_id:
                        vk_session.method("messages.send", {"peer_id": user_id, "message": "Пользователь уже забанен!", "random_id": 0})
                        return 1
                banned_info = vk_session.method("users.get", {"user_ids": int(banned_id)})
                staff_info = vk_session.method("users.get", {"user_ids": int(user_id)})

                banned_users.append(banned_id)
                vk_session.method("messages.send", {"peer_id": int(banned_id), "message": "Вы были заблокированы! Любое Ваше сообщение будет игнорироваться!", "random_id": 0})
                for i in all_staff:
                    vk_session.method("messages.send", {"peer_id": i, "message": "Пользователь "+"@id" + str(banned_id) + "(" + banned_info[0]["first_name"] + " " + banned_info[0]["last_name"] + ")" + " был забанен администратором " + "@id" + str(user_id) + "(" + staff_info[0]["first_name"] + " " + staff_info[0]["last_name"] + ")", "random_id": 0})
            except:
                vk_session.method("messages.send", {"peer_id": user_id, "message": "Введено неверные данные!\n\nПример использования команды:\n!ban 126345141", "random_id": 0})
            return 1
    errors_caused(user_id, "NoPerms")
    return 1

def check_banned(user_id):
    for banned_user in banned_users:
        if str(user_id) == str(banned_user):
            print("id" + str(user_id) + "(ЗАБАНЕН) пытался написать.")
            return 1
    return 0

def unban(user_id, unbanned_id):
    for staff in grandStaff:
        if user_id == staff:
            try:
                unbanned_id = unbanned_id[7:]
                unbanned_info = vk_session.method("users.get", {"user_ids": int(unbanned_id)})
                adm_info = vk_session.method("users.get", {"user_ids": int(user_id)})

                banned_users.pop(banned_users.index(unbanned_id))
                vk_session.method("messages.send", {"peer_id": int(unbanned_id), "message": "Вы были разблокированы!", "random_id": 0})
                for i in all_staff:
                    vk_session.method("messages.send", {"peer_id": i, "message": "Пользователь "+"@id" + str(unbanned_id) + "(" + unbanned_info[0]["first_name"] + " " + unbanned_info[0]["last_name"] + ")" + " был разбанен администратором " + "@id" + str(user_id) + "(" + adm_info[0]["first_name"] + " " + adm_info[0]["last_name"] + ")", "random_id": 0})
            except:
                vk_session.method("messages.send", {"peer_id": user_id, "message": "Пользователь не забанен!\n\nПример использования команды:\n!unban 126345141", "random_id": 0})
            return 1
    errors_caused(user_id, "NoPerms")
    return 1

def banlist(user_id):
    for adm in all_staff:
        if user_id == adm:
            all_banned = ""
            for banned in banned_users:
                banned_info = vk_session.method("users.get", {"user_ids": int(banned)})
                all_banned += " - @id" + str(banned) + "(" + banned_info[0]["first_name"] + " " + banned_info[0]["last_name"] + ")\n"
            vk_session.method("messages.send", {"peer_id": user_id, "message": "Список заблокированных пользователей:\n" + all_banned, "random_id": 0})
            return 1
    errors_caused(user_id, "NoPerms")
    return 1

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            messages = vk_session.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unread"})
            if messages["count"] >= 1:
                id = messages["items"][0]["last_message"]["from_id"]
                body = messages["items"][0]["last_message"]["text"]
                msg_id = messages["items"][0]["last_message"]["id"]

                print("\nMessage come at: " + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
                print("From user: " + str(id))
                print("Text: " + str(body) + "\n")

                if check_first(user_id=id, msg_theme=body) or check_second(user_id=id, msg_text=body, msg_id=msg_id) or check_third(user_id=id, confirmation=body) or check_banned(user_id=id):
                    break
                if body.lower() == "":
                    vk_session.method("messages.send", {"peer_id": id, "message": "Введи сообщение, еблан", "random_id": 0})
                    break
                elif body.lower()[:6] == "+модер":
                    add_moder(user_id=id, moder_id=body)
                    break
                elif body.lower()[:6] == "-модер":
                    remove_moder(user_id=id, moder_id=body)
                    break
                elif body.lower()[:6] == "+админ":
                    add_admin(user_id=id, admin_id=body)
                    break
                elif body.lower()[:6] == "-админ":
                    remove_admin(user_id=id, admin_id=body)
                    break
                elif body.lower() == "!админы":
                    get_admin_list(user_id=id)
                    break
                elif body.lower()[0] == "#":
                    moderator_checking(user_id=id, reply=body)
                    break
                elif body.lower() == "!banlist":
                    banlist(user_id=id)
                    break
                elif body.lower()[:4] == "!ban":
                    ban(user_id=id, banned_id=body)
                    break
                elif body.lower()[:6] == "!unban":
                    unban(user_id=id, unbanned_id=body)
                    break
                elif body.lower() == "создать тикет":
                    if check_has_ticket(user_id=id):
                        break
                    vk_session.method("messages.send", {"peer_id": id, "message": "Вы начали создавать тикет. Выберите тему сообщения, и отправьте ее сюда (не больше 20 символов).", "random_id": 0})
                    add_to_first_step(user_id=id)
                    break
                else:
                    getCommands(user_id=id)
                    break
    time.sleep(1)