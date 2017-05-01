import re
import requests
import threading


class TestProxy(object):
    def __init__(self):
        self.sFile = r'proxy.txt'
        self.dFile = r'alive.txt'
        self.URL = r'http://www.baidu.com'
        self.threads = 10
        self.timeout = 3
        self.regex = re.compile(r'baidu.com')
        self.aliveList = []
        self.run()

    def run(self):
        with open(self.sFile, 'r') as fp:
            lines = fp.readlines()
            line = lines.pop()
            while lines:
                for i in range(self.threads):
                    t = threading.Thread(target=self.linkWithProxy, args=(line,))
                    t.start()
                    if lines:
                        line = lines.pop()
                    else:
                        continue

        with open(self.dFile, 'w') as fp:
            for i in range(len(self.aliveList)):
                fp.write(self.aliveList[i])

    def linkWithProxy(self, line):
        lineList = line.split('\t')
        protocol = lineList[2].lower()
        server = protocol + r'://' + lineList[0] + ":" + lineList[1]
        try:
            response = requests.get(self.URL, proxies={server}, timeout=self.timeout)
        except:
            print('%s connect failed' % server)
            return
        else:
            try:
                str = response.text
            except:
                print('%s connect failed' % server)
                return
            if self.regex.search(str):
                print('%s connect success .......' % server)
                self.aliveList.append(line)

if __name__ == '__main__':
   TP = TestProxy()