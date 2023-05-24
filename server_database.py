from sqlalchemy import __version__, create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import mapper, registry, declarative_base, Session

print("Версия SQLAlchemy:", __version__)

engine = create_engine('sqlite:///server_db.db3', echo=False, pool_recycle = 7200)

Base = declarative_base()

class User(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True) 
    login = Column(String)
    info = Column(String)

    def __init__(self, login): 
        self.login = login

class Contacts_list(Base):

    __tablename__ = 'contacts_list'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    contact_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    def __init__(self, id, contact_id): 
        self.id =id
        self.contact_id = contact_id

class Users_history(Base):

    __tablename__ = 'users_history'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True) 
    connection_time = Column(DateTime)
    ip = Column(String)

    def __init__(self, id, ip): 
            self.id = id
            self.ip = ip

Base.metadata.create_all(bind=engine)

# отладка
with Session(autoflush=False, bind=engine) as db:
    user1 = User('Ars')
    user2 = User('Val')
    db.add(user1)
    db.add(user2)    
    db.commit()    
    print(user1.id)
    print(user2.id)

