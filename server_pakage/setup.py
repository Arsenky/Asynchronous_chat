from setuptools import setup 

setup( name='server_package',
        version ="0.1", 
        description ="Server for asynch_chat", 
        author ="Arseny Sychevsky", 
        author_email ="arsenky@yandex.ru", 
        url ="https://upload.pypi.org/legacy/", 
        packages=["src"],
        install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
        )