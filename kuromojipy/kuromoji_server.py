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
    def __init__(self, kuromoji_jar=None):
        '''
        Open Java gateway and Get kuromoji Class
        '''
        if not kuromoji_jar:
            kuromoji_jar = self.__find_kuromoji_jar()
        py4j_jar = os.path.abspath(os.path.join(here, 'lib/py4j0.10.6.jar'))
        # Execute .class with classpath to jar files
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

    def __find_kuromoji_jar(self):
        '''
        Find kuromoji jar file path in library directory
        '''
        # Find jar by regex matching from files in lib dir
        all_paths = glob(os.path.join(here, 'lib/*'))
        re_kuromoji_jar \
            = re.compile(u'^kuromoji-[0-9]+\.[0-9]+\.[0-9]+.*\.jar$', re.U)
        kuromoji_jar_paths \
            = [path for path in all_paths
               if re_kuromoji_jar.match(os.path.basename(path))]

        # Sort by descending order -> Find the newest jar file
        if kuromoji_jar_paths:
            kuromoji_jar = sorted(kuromoji_jar_paths, reverse=True)[0]
        else:
            raise OSError('Kuromoji jar file is not found.')

        return os.path.abspath(kuromoji_jar)


def main():
    print('''
When you execute the following code...

from kuromojipy.kuromoji_server import KuromojiServer

with KuromojiServer(kuromoji_jar='lib/kuromoji-0.7.7.jar') as kuro_server:
    kuromoji = kuro_server.kuromoji
    tokenizer = kuromoji.Tokenizer.builder().build()
    tokens = tokenizer.tokenize(u'お寿司が食べたい。')
    for token in tokens:
        print(token.getSurfaceForm() + \'\\t\' + token.getAllFeatures())

you will get the following output.
''')
    from kuromojipy.kuromoji_server import KuromojiServer

    with KuromojiServer(kuromoji_jar='lib/kuromoji-0.7.7.jar') as kuro_server:
        kuromoji = kuro_server.kuromoji
        tokenizer = kuromoji.Tokenizer.builder().build()
        tokens = tokenizer.tokenize(u'お寿司が食べたい。')
        for token in tokens:
            print(token.getSurfaceForm() + '\t' + token.getAllFeatures())


if __name__ == '__main__':
    main()
