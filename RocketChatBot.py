from pprint import pprint
from random import choice
from threading import Thread
from time import sleep

from rocketchat_API.rocketchat import RocketChat


class RocketChatBot(object):
    def __init__(self, botname, passwd, server, command_character=None):
        self.botname = botname
        self.api = RocketChat(user=botname, password=passwd, server_url=server)
        self.commands = [(['echo', ], self.echo)]
        self.auto_answers = []
        self.direct_answers = []
        self.unknow_command = ['command not found', ]
        self.lastts = {}
        self.command_character = command_character

    def echo(self, msg, user, channel_id):
        self.send_message('@' + user + ' : ' + msg, channel_id)

    def get_status(self, auser):
        return self.api.users_get_presence(username=auser)

    def send_message(self, msg, channel_id):
        self.api.chat_post_message(channel=channel_id, text=msg)

    def add_dm_handler(self, command, action):
        self.commands.append((command, action))

    def add_auto_answer(self, triggers, answers):
        self.auto_answers.append((triggers, answers))

    def add_direct_answer(self, triggers, answers):
        self.direct_answers.append((triggers, answers))
        
    def handle_command_character_message(self, message, channel_id):
        msg = message['msg'].lstrip(self.command_character)

        command = msg.split()[0].lower()
        arguments = " ".join(msg.split()[1:])
        user = message['u']['username']

        for cmd_list in self.commands:
                if command.lower() in cmd_list[0]:
                    cmd_list[1](arguments, user, channel_id)
                    return
                
        if not self.handle_auto_answer(message, self.direct_answers, channel_id):
                self.send_message('@' + user + ' :' + choice(self.unknow_command), channel_id)

    def handle_direct_message(self, message, channel_id):
        msg = message['msg'].lstrip('@' + self.botname).strip()
        if len(msg) > 0:
            command = msg.split()[0].lower()
            arguments = " ".join(msg.split()[1:])
            user = message['u']['username']
            for cmd_list in self.commands:
                if command.lower() in cmd_list[0]:
                    cmd_list[1](arguments, user, channel_id)
                    return

            if not self.handle_auto_answer(message, self.direct_answers, channel_id):
                self.send_message('@' + user + ' :' + choice(self.unknow_command), channel_id)
        else:
            self.send_message('Here I am', channel_id)

    def handle_auto_answer(self, message, answers, channel_id):
        for kind in answers:
            for k in kind[0]:
                if k in message['msg'].lower():
                    self.send_message(choice(kind[1]) + ' @' + message['u']['username'], channel_id)
                    return True
        return False

    def handle_messages(self, messages, channel_id):
        for message in messages['messages']:
            if message['u']['username'] != self.botname:
                pprint(message)
                if message['u']['username'] == 'rocket.cat':
                    continue
                if message['msg'].startswith('@' + self.botname):
                    Thread(target=self.handle_direct_message, args=(message, channel_id)).start()
                elif self.command_character is not None and message['msg'].startswith(self.command_character):
                    Thread(target=self.handle_command_character_message, args=(message, channel_id)).start()
                elif 'mentions' not in message or message.get('mentions') == []:
                    Thread(target=self.handle_auto_answer, args=(message, self.auto_answers, channel_id)).start()

    def load_ts(self, channel_id, messages):
        if len(messages) > 0:
            self.lastts[channel_id] = messages[0]['ts']
        else:
            self.lastts[channel_id] = ''

    def load_channel_ts(self, channel_id):
        self.load_ts(channel_id, self.api.channels_history(channel_id).json()['messages'])

    def load_group_ts(self, channel_id):
        self.load_ts(channel_id, self.api.groups_history(channel_id).json()['messages'])

    def load_im_ts(self, channel_id):
        response = self.api.im_history(channel_id).json()
        if response.get('success'):
            self.load_ts(channel_id, self.api.im_history(channel_id).json()['messages'])

    def process_messages(self, messages, channel_id):
        try:
            if "success" in messages:
                if messages['success'] == False:
                    raise RuntimeError(messages['error'])
            if len(messages['messages']) > 0:
                self.lastts[channel_id] = messages['messages'][0]['ts']
            self.handle_messages(messages, channel_id)
        except Exception as e:
            pprint(e)

    def process_channel(self, channel_id):
        if channel_id not in self.lastts:
            self.lastts[channel_id] = ''

        self.process_messages(self.api.channels_history(channel_id, oldest=self.lastts[channel_id]).json(),
                              channel_id)

    def process_group(self, channel_id):
        if channel_id not in self.lastts:
            self.lastts[channel_id] = ''

        self.process_messages(self.api.groups_history(channel_id, oldest=self.lastts[channel_id]).json(),
                              channel_id)

    def process_im(self, channel_id):
        if channel_id not in self.lastts:
            self.lastts[channel_id] = ''

        self.process_messages(self.api.im_history(channel_id, oldest=self.lastts[channel_id]).json(),
                              channel_id)

    def run(self):
        for channel in self.api.channels_list_joined().json().get('channels'):
            self.load_channel_ts(channel.get('_id'))

        for group in self.api.groups_list().json().get('groups'):
            self.load_group_ts(group.get('_id'))

        for im in self.api.im_list().json().get('ims'):
            self.load_im_ts(im.get('_id'))

        while 1:
            for channel in self.api.channels_list_joined().json().get('channels'):
                Thread(target=self.process_channel, args=(channel.get('_id'),)).start()

            for group in self.api.groups_list().json().get('groups'):
                Thread(target=self.process_group, args=(group.get('_id'),)).start()

            for im in self.api.im_list().json().get('ims'):
                Thread(target=self.process_im, args=(im.get('_id'),)).start()

            sleep(1)
