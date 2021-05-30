import telnetlib

 
class Connection:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        #
        self.telnet = None


    def connect(self):
        try:
            self.telnet = telnetlib.Telnet(self.host, port=self.port, timeout=5)
        except Exception:
            return False

        return True


    def authenticate(self):
        self.read('name:')
        self.execute(self.username)
        self.read('password:')
        self.execute(self.password)

        return True


    def disconnect(self):
        try:
            self.telnet.close()
        except Exception:
            pass
        return


    def execute(self, command):
        encoded = f'{command}\r\n'.encode('utf-8')
        self.telnet.write(encoded)

        return


    def read(self, text):
        encoded = text.encode('utf-8')
        response = self.telnet.read_until(encoded)

        return response.decode('utf-8')

    
    def read_all(self):
        end_phrase = b'portalgunc137'
        timeout = 5

        self.execute(end_phrase)
        return self.telnet.read_until(end_phrase, timeout=timeout)
