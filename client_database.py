from sqlalchemy import __version__, create_engine, Table, Column, Integer, String, MetaData, ForeignKey, DateTime
from sqlalchemy.orm import mapper, registry, declarative_base, Session
from datetime import datetime

print("Версия SQLAlchemy:", __version__)
class ClientDataBase():

    db_engine = create_engine('sqlite:///client_db.db3', echo=False, pool_recycle = 7200)
    Base = declarative_base()
    
    session = Session(autoflush=False, bind=db_engine)

    class Contacts_list(Base):

        __tablename__ = 'contacts_list'
        login = Column(Integer, primary_key=True)

        def __init__(self, id, contact_id): 
            self.id =id
            self.contact_id = contact_id

    class Massages_history(Base):

        __tablename__ = 'massages_history'
        id = Column(Integer, primary_key=True) 
        time = Column(DateTime, default = datetime.now())
        sender = Column(String)
        text = Column(String)

        def __init__(self, sender, text): 
                self.sender = sender
                self.text = text
                
    Base.metadata.create_all(bind=db_engine)

    def history(self, sender, text):
        try:
            history_line = self.Massages_history(sender, text)
            self.session.add(history_line)
            self.session.commit()
        except:
            self.session.rollback()

        


