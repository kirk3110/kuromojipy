# -*- coding: utf-8 -*-
'''
Connect to JVM and use kuromoji through socket (by Py4J)
'''

import subprocess
import time
import os.path
from contextlib import contextmanager
from argparse import ArgumentParser
from py4j.java_gateway import JavaGateway


class KuromojiServer:
    '''
    Wrapper for JVM Server provided by Py4J
    '''
    def __init__(self):
        '''
        Open Java gateway and Get kuromoji Class
        '''
        # Execute .class with classpath to jar files
        cmd = 'cd {} && java -cp lib/*;. Py4JEntryPoint'.format(
            os.path.abspath(os.path.join(__file__, '..')))
        self.__proc = subprocess.Popen(cmd, shell=True)

        count = 0
        while True:
            try:
                self.__gateway = JavaGateway()
                break
            except:
                # almost 10 second -> timeout
                time.sleep(1)
                count += 1
                if count == 10:
                    self.__proc.kill()
                    raise TimeoutError('Failed to connect to kuromoji server.')
        self.kuromoji = self.__gateway.jvm.org.atilika.kuromoji

    def close(self):
        '''
        Close Java gateway and kill Java process
        '''
        self.__gateway.shutdown()
        self.__proc.kill()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()


def main():
    print('''
When you execute the following code...

from kuromoji_server import KuromojiServer

with KuromojiServer() as kuro_server:
    kuromoji = kuro_server.kuromoji
    tokenizer = kuromoji.Tokenizer.builder().build()
    a = tokenizer.tokenize(u'お寿司が食べたい。')
    for token in a:
        print token.getSurfaceForm() + \'\\t\' + token.getAllFeatures()

you will get the following output.
''')
    from kuromoji_server import KuromojiServer

    with KuromojiServer() as kuro_server:
        kuromoji = kuro_server.kuromoji
        tokenizer = kuromoji.Tokenizer.builder().build()
        tokens = tokenizer.tokenize(u'お寿司が食べたい。')
        for token in tokens:
            print(token.getSurfaceForm() + '\t' + token.getAllFeatures())


if __name__ == '__main__':
    main()
