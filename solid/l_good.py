from abc import ABC, abstractmethod
from dataclasses import dataclass

# regrouper certaines propriétés sous une seule entité ?

class Message:
    
    def __init__(self, text):
        self.__text = text

@dataclass
class Contact:
    email: str
    phone: str
    discordid: str

class Notification(ABC):

    @abstractmethod
    def notify(self, message: Message, contact: Contact):
        pass

class Email(Notification):
    
    def notify(self, message: Message, contact: Contact):
        print(f'Send {message} to {contact.email}')

class SMS(Notification):
    
    def notify(self, message: Message, contact: Contact):
        print(f'Send {message} to {contact.phone}')
        
class Discord(Notification):
    
    def notify(self, message: Message, contact: Contact):
        print(f'Send {message} to {contact.discordid}')

if __name__ == '__main__':
    notification = SMS()
    gael = Contact(email='john@test.com', phone='007', discordid='gael')
    notification.notify(Message('Hello'), gael)
    discord_notification = Discord()
    discord_notification.notify(Message('Hello'), gael)
    