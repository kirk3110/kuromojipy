kuromojipy
===========

A python I/F for `kuromoji <https://github.com/downloads/atilika/kuromoji>`_ (powered by `Py4J <https://github.com/bartdag/py4j>`_).


Installation
------------

1) Clone kuromojipy project directory.

2) Get kuromoji package from `download page <https://github.com/atilika/kuromoji/downloads>`_ and unzip.

3) Put kuromoji JAR file into kuromojipy library directory (kuromojipy/kuromojipy/lib).

4) Put kuromojipy module directory (kuromojipy/kuromojipy) into $PYTHONPATH.

Installation Step Example
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ cd yourworkspace
    $ git clone https://github.com/kirk3110/kuromojipy.git
    $ wget https://github.com/downloads/atilika/kuromoji/kuromoji-0.7.7.tar.gz
    $ tar zxvf kuromoji-0.7.7.tar.gz
    $ cp kuromoji-0.7.7/lib/kuromoji-0.7.7.jar kuromojipy/kuromojipy/lib
    $ cp -r kuromojipy/kuromojipy path/to/python/env/Lib/site-packages


Examples
--------

When you execute the following code...

.. code-block:: python

    from kuromojipy.kuromoji_server import KuromojiServer

    with KuromojiServer() as kuro_server:
        kuromoji = kuro_server.kuromoji
        tokenizer = kuromoji.Tokenizer.builder().build()
        tokens = tokenizer.tokenize(u'お寿司が食べたい。')
        for token in tokens:
            print(token.getSurfaceForm() + '\t' + token.getAllFeatures())

you will get the following output.

.. code-block::

    お      接頭詞,名詞接続,*,*,*,*,お,オ,オ
    寿司    名詞,一般,*,*,*,*,寿司,スシ,スシ
    が      助詞,格助詞,一般,*,*,*,が,ガ,ガ
    食べ    動詞,自立,*,*,一段,連用形,食べる,タベ,タベ
    たい    助動詞,*,*,*,特殊・タイ,基本形,たい,タイ,タイ
    。      記号,句点,*,*,*,*,。,。,。


    
