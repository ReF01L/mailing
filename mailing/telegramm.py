import telepot

from fabrique_test import settings


class TeleMessage:
    def __init__(self):
        self.token = settings.config['TELEGRAM']['TOKEN']
        self._id = '1328466861'
        self.bot = telepot.Bot(self.token)

    def send_message(self, text: str, to_id: str = None):
        self.bot.sendMessage(to_id or self._id, text, parse_mode='Markdown')

    def test(self):
        print(self.bot.getChat(self._id))


if __name__ == '__main__':
    tel = TeleMessage()
    tel.test()
