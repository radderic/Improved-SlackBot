from slackclient import SlackClient
from time import sleep
from sys import exit
from os import environ
from commands.event import Event
from commands.commands import commands

class Bot(object):
    def __init__(self):
        self.username = None
        self.userid = None
        self.token = None
        self.slackclient = None

    def _getTokenFromFile(self, filename):
        '''
        Returns token as a string without newline char from specified file.
        '''
        print('Retrieving Auth Token from file...')
        try:
            tokenFile = open(filename, 'r')
            token = tokenFile.read().rstrip()
            tokenFile.close()
        except IOError:
            print('File does not exist')
            exit(1)
        return token

    def _getTokenFromEnv(self):
        '''
        Returns token as string from env variable
        '''
        print('Retriving Auth Token from env...')
        if(environ.get('SLACK_BOT_TOKEN') is not None):
            return environ.get('SLACK_BOT_TOKEN')
        else:
            print('Failed to get token from env')
            exit(2)

    def _setToken(self):
        '''
        You can use whichever method you prefer to get the token.
        Comment and uncomment if you prefer the other.
        '''
        self.token = self._getTokenFromFile('token.txt')
#        self.token = self._getTokenFromEnv()

    def _connect(self):
        self._setToken()
        self.slackclient = SlackClient(self.token)
        print('Attempting to connect...')
        if(self.slackclient.rtm_connect()):
            print('Connection successful!')
            return True
        else:
            print('Failed to connect')
            return False

    def _setUserID(self):
        print('Retrieving self ID...')
        data = self.slackclient.api_call('auth.test')
        self.userid = data['user_id']
        print("ID: ", self.userid)

    def _setup(self):
        '''
        Minimal setup getting userid and displayname
        '''
        self._setUserID()
        self._getDisplayName();

    def _getCommand(self, text):
        '''
        Parses command (if it exists) out of event text
        '''
        parsed_message = text.split(' ', 2)
        if(len(parsed_message) > 1):
            command = parsed_message[1]
            return command
        else:
            return None

    def _getDisplayName(self):
        '''
        Attempts to get bots own name
        '''
        data = self.slackclient.api_call(
                'users.info',
                user=self.userid
        )
        if(data):
            self.username = data['user']['real_name']
            print('Username:', self.username)
        else:
            print('Failed to get display name')

    def lookup(self, who):
        '''
        Attempts to look a user's display name based on their user id
        '''
        data = self.slackclient.api_call(
                'users.info',
                user=who
        )
        if(data):
            return data['user']['profile']['display_name']
        else:
            return None

    def mention(self, who):
        return '<@' + who + '> '

    def message(self, text, channel):
        self.slackclient.api_call(
            'chat.postMessage',
            channel=channel,
            text=text
        )

    def mentioned(self, text):
        if(text):
            if(text.startswith('<@{}>'.format(self.userid))):
                return True
            else:
                return False
        return False

    def run(self):
        if(self._connect()):
            self._setup()
            print('Bot running...')
            while True:
                slackevent = self.slackclient.rtm_read()
                #ignore if there is nothing to read
                if(len(slackevent) != 0):
                    event = Event(**slackevent[0])
                    if(self.mentioned(event.text)):
                        command = self._getCommand(event.text)
                        print('{}: {}({}) - command={}'.format(event.formattedTime(), self.lookup(event.who), event.who, command))
                        #print(event.getUTC() + ' ' + self.lookup(event.who) + '(' + event.who + ') - command:', command)
                        if(command):
                            if(command in commands):
                                commands[command](self, event)
                            else:
                                self.message('?', event.where)
                                print('command not found')
                        else:
                            pass
                            #commandless mention to bot
                            #do something else perhaps?
                    else:
                        pass
                        #Bot isn't being talked to
                        #maybe do something else

                #Gives the CPU a small break so it's not constantly checking
                sleep(1)

