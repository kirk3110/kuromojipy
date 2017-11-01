# -*- coding: utf-8 -*-
'''
Connect to JVM and use kuromoji through socket (by Py4J)
'''

import subprocess
import time
import os.path
import re
from glob import glob
from py4j.java_gateway import JavaGateway

here = os.path.abspath(os.path.join(__file__, '..'))


class KuromojiServer:
    '''
    Wrapper for JVM Server provided by Py4J
    '''
    def __init__(self,
                 kuromoji_jar=os.path.join(here, 'lib/kuromoji-0.7.7.jar')):
        '''
        Constructor
        Open Java gateway and Get kuromoji Class

        @param kuromoji_jar: Kuromoji jarfile path \
(if default, lib/kuromoji-0.7.7.jar is used.)
        '''
        py4j_jar = os.path.abspath(os.path.join(here, 'lib/py4j0.10.6.jar'))

        # Check existance of jarfiles
        if not os.path.isfile(kuromoji_jar):
            raise IOError('Kuromoji jarfile ({}) is not found.'
                          .format(kuromoji_jar))
        elif not os.path.isfile(py4j_jar):
            raise IOError('Py4J jarfile is not found.'
                          .format(kuromoji_jar))

        # Execute .class with classpath to jarfiles
        cmd = 'cd {} && java -cp {};{};. Py4JEntryPoint'.format(
            here, kuromoji_jar, py4j_jar)
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
    print(u'''
When you execute the following code...

from kuromojipy.kuromoji_server import KuromojiServer

with KuromojiServer() as kuro_server:
    kuromoji = kuro_server.kuromoji
    tokenizer = kuromoji.Tokenizer.builder().build()
    tokens = tokenizer.tokenize(u'お寿司が食べたい。')
    for token in tokens:
        print(token.getSurfaceForm() + \'\\t\' + token.getAllFeatures())

you will get the following output.
''')
    from kuromojipy.kuromoji_server import KuromojiServer

    with KuromojiServer() as kuro_server:
        kuromoji = kuro_server.kuromoji
        tokenizer = kuromoji.Tokenizer.builder().build()
        tokens = tokenizer.tokenize(u'お寿司が食べたい。')
        for token in tokens:
            print(token.getSurfaceForm() + '\t' + token.getAllFeatures())


if __name__ == '__main__':
    main()
