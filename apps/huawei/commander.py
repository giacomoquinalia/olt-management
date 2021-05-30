from utils.connection import Connection


class Huawei(Connection):
    """
    This class handles huawei OLTs functionalities
    """
    def __init__(self, host, port, username, password):
        super().__init__(host, port, username, password)
        #
        self.log = ''


    def connect(self):
        return super().connect()


    def autenticate(self):
        return super().autenticate()


    def disconnect(self):
        return super().disconnect()


    def has_failure(self, text):
        return 'Failure' in text

    
    def generate_log(self):
        self.read('enable')

        events = self.read_all().decode('utf-8').splitlines()

        log = ['enable\r\n']
        log.extend(events)
        log.pop(-1)
        
        return '\n'.join(log)


    def autofind(self, commands):
        """
        Returns a list of ONUs
        """
        for command in commands:
            self.execute(command)
            
        result = self.read_all().decode('utf-8')
            
        # If failure then there is no ONU
        if self.has_failure(result):
            return []

        ont_found = result.splitlines()
        ont_list = []
        ont_info = {
            'slot': None,
            'pon': None,
            'serial': None,
            'mac': None
        }

        for line in ont_found:
            temp = line.split()
             
            if 'F/S/P' in line:
                temp = temp[2].split('/')

                ont_info['slot'] = temp[1]
                ont_info['pon'] = temp[2]
                continue

            if 'Ont SN' in line:
                ont_info['serial'] = temp[3]
                continue

            if 'Ont MAC' in line:
                ont_info['mac'] = temp[3]

                ont_list.append(ont_info)

        return ont_list


    def send(self, commands):
        for command in commands:
            self.execute(command)

        self.log = self.generate_log()
        
        return self.log