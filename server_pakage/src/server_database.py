from sqlalchemy import __version__, create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime, LargeBinary, and_
from sqlalchemy.orm import mapper, registry, declarative_base, Session
from datetime import datetime

print("Версия SQLAlchemy:", __version__)
class ServerDataBase():

    db_engine = create_engine('sqlite:///server_db.db3', echo=False, pool_recycle = 7200)
    Base = declarative_base()
    
    session = Session(autoflush=False, bind=db_engine)
        
    class User(Base):

        __tablename__ = 'users'
        id = Column(Integer, primary_key=True) 
        login = Column(String, unique = True)
        info = Column(String, default = 'Пусто')
        pass_hash = Column(LargeBinary)

        def __init__(self, login, pass_hash): 
            self.login = login
            self.pass_hash = pass_hash
        

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
        connection_time = Column(DateTime, default = datetime.now())
        ip = Column(String)

        def __init__(self, id, ip): 
                self.id = id
                self.ip = ip
                
    Base.metadata.create_all(bind=db_engine)

    def add_user(self, login, pass_hash):
        try:
            user = self.User(login, pass_hash)
            self.session.add(user)
            self.session.commit()
        except:
            self.session.rollback()

    def add_contact(self, client_login, contact_login):
        try:
            contact = self.Contacts_list(self.get_id_by_login(client_login), self.get_id_by_login(contact_login))
            self.session.add(contact)
            self.session.commit()
        except:
            self.session.rollback()
    
    def del_contact(self, client_login, contact_login):
        try:
            instanse = self.session.query(self.Contacts_list).filter(and_(
                self.Contacts_list.id == self.get_id_by_login(client_login), 
                self.Contacts_list.contact_id == self.get_id_by_login(contact_login))
                ).first()
            self.session.delete(instanse)
            self.session.commit()
        except:
            self.session.rollback()
        
    
    def history(self, id, ip):
        try:
            history_line = self.Users_history(id, ip)
            self.session.add(history_line)
            self.session.commit()
        except:
            self.session.rollback()

    
    def get_id_by_login(self, log):
        return self.session.query(self.User).filter_by(login=log).first().id
        

# отладка
if __name__ == '__main__':
    db = ServerDataBase()
  