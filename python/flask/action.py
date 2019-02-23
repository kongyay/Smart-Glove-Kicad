import requests
import json

class ActionMaker(object):
    def __init__(self):
        return

    def setDisplay(self,display):
        self.display = display

    def do(self,type='Display',args={'text':'No argument'}):
        print("Doing Action:",type)
        if type == 'Display':
            return self.doDisplay(args)
        elif type == 'Http':
            return self.doSendHTTP(args)
        elif type == 'Draw':
            return self.doDraw(args)
        elif type == 'Screen':
            return self.doScreen(args)

    def doDisplay(self,args,row=6):
        if 'text' not in args:
            return 'Error display (args)'
        texts = args['text'].splitlines()
        r = self.display.numRow-1
        for t in texts[::-1]:
            self.display.write_row(text=t,row=r)
            r -= 1
        return 'Displayed: ' + '\\n'.join(texts)

    def doSendHTTP(self,args):
        if 'type' not in args or 'url' not in args or 'params' not in args:
            return 'Error Sending Reqeust (args)'
        self.display.write_row(text='Sending Request...',row=self.display.numRow-1)
        try:
            with requests.Session() as session:
                if args['type']=='POST':
                    with session.post(args['url'],data=args['params'],headers=json.loads(args['headers'])) as response:
                        result = response.text 
                        self.display.write_row(text=result,row=self.display.numRow-1)
                else:
                    with session.get(args['url'],params=args['params']) as response:
                        result = response.text
                        self.display.write_row(text=result,row=self.display.numRow-1)
        except (Exception):
            return 'Error Sending Reqeust'

        return 'Sending Request...'

    def doDraw(self,args):
        if 'pixels' not in args:
            return 'Error Draw (args)'
        self.display.drawPixel(args['pixels'])
        return 'Drawn'

    def doScreen(self,args):
        if 'screen' not in args:
            return 'Error Screen Shown (args)'
        if args['screen'] == 'Clock':
            self.display.show_clock()
        return 'Screen Shown'

actionMaker = ActionMaker()