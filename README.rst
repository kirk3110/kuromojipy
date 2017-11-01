kuromojipy
===========

A python I/F for `kuromoji <https://github.com/downloads/atilika/kuromoji>`_ (powered by `Py4J <https://github.com/bartdag/py4j>`_).


Installation
------------

.. code-block:: bash

    $ pip install git+https://github.com/kirk3110/kuromojipy

or

.. code-block:: bash

    $ cd yourworkspace
    $ git clone https://github.com/kirk3110/kuromojipy.git
    $ cd kuromojipy
    $ python setup.py install


Requirement
-----------
- Java 6.0+
- Python 2.7+/3.4+
- `Py4J <https://github.com/bartdag/py4j>`_


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

References
-----------

Thanks!

- https://qiita.com/mojaie/items/f16b97b1388f73e56b86
- https://qiita.com/arc279/items/5f547de8978a790e8523
- https://qiita.com/riverwell/items/e90cbbfdac439e6e9d30
