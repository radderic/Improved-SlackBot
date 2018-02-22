
from slackclient import SlackClient
from time import sleep
from pprint import pprint
from sys import exit
from os import environ

class Bot(object):
    #contructor, called when an instance is created
    def __init__(self):
        self.username = None
        self.userid = None
        self.teamid = None
        self.token = None
        self.slackclient = None

    def getTokenFromFile(self, filename):
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

    def getTokenFromEnv(self):
        '''
        Returns token as string from env variable
        '''
        print('Retriving Auth Token from env...')
        if(environ.get('SLACK_BOT_TOKEN') is not None):
            return environ.get('SLACK_BOT_TOKEN')
        else:
            print('Failed to get token from env')
            exit(2)

    def setToken(self):
        '''
        You can use whichever method you prefer to get the token.
        Comment and uncomment if you prefer the other.
        '''
        self.token = self.getTokenFromFile('token.txt')
#        self.token = self.getTokenFromEnv()

    def connect(self):
        self.setToken()
        self.slackclient = SlackClient(self.token)
        print('Attempting to connect...')
        if(self.slackclient.rtm_connect()):
            print('Connection successful!')
            return True
        else:
            print('Failed to connect')
            return False

    def setUserID(self):
        print('Retrieving self ID...')
        data = self.slackclient.api_call('auth.test')
        self.userid = data['user_id']

    def run(self):
        if(self.connect()):
            self.setUserID()
            print('Bot running...')
            while True:
                event = self.slackclient.rtm_read()
                #ignore if there is nothing to read
                if(len(event) != 0):
                    pprint(event)
                    #handle event here...
                    #your code starts here
                #Gives the CPU a small break so it's not constantly checking
                sleep(1)

