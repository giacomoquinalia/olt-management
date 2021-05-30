from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .commander import Huawei
from .validators import (
    AutofindValidator, 
    ProvisioningValidator,
    UnprovisioningValidator,
    CustomizedValidator
)


class Autofind(APIView):
    """
    Returns a list of ONUs waiting for authorization.
    Send commands via CLI and parse the result returnung an array of ONU's informations.
    """
    permission_classes = [ IsAuthenticated ]
    

    def post(self, request, *args, **kwargs):
        # Assign data
        host =      request.data.get('host')
        port =      request.data.get('port')
        username =  request.data.get('username')
        password =  request.data.get('password')

        # Validating request parameters
        validator = AutofindValidator({
            'host':     host,
            'port':     port,
            'username': username,
            'password': password
        })

        if not validator.validate():
            errors = validator.get_message()
            return Response({
                'success': False,
                'data': {
                    'errors': errors
                }
            })

        # Preparing commands
        commands = [
            'enable',
            'scroll 512',
            'display ont autofind all\r\n'
        ]

        # Instancing huawei class
        huawei = Huawei(host, port, username, password)

        if huawei.connect():
            huawei.authenticate()
            # Send commands for autofind
            ont_list = huawei.autofind(commands)
            success, message = (True, 'Scripts executed successfully.')
        else:
            # Response states
            success, ont_list, message = (
                False, [], 'Could not connect to the OLT.'
            )
        
        # Close telnet connection
        huawei.disconnect()

        return Response({
            'success': success,
            'message': message,
            'data': {
                'ont_list': ont_list
            }
        })


class Provisioning(APIView):
    permission_classes = [ IsAuthenticated ]


    def post(self, request, *args, **kwargs):
        # Assign data
        mode =              request.data.get('mode')
        host =              request.data.get('host')
        port =              request.data.get('port')
        username =          request.data.get('username')
        password =          request.data.get('password')
        _id =               request.data.get('id')
        slot =              request.data.get('slot')
        pon =               request.data.get('pon')
        serial =            request.data.get('serial')
        vlan =              request.data.get('vlan')
        desc =              request.data.get('desc')
        gemport =           request.data.get('gemport')
        user_vlan =         request.data.get('user_vlan')
        line_profile =      request.data.get('line_profile')
        name_srv_profile =  request.data.get('name_srv_profile')

        # Validating request parameters
        validator = ProvisioningValidator({
            'host':             host,
            'port':             port,
            'username':         username,
            'password':         password,
            'mode':             mode,
            'id':               _id,
            'slot':             port,
            'pon':              pon,
            'serial':           serial,
            'desc':             desc,
            'vlan':             vlan,
            'gemport':          gemport,
            'user_vlan':        user_vlan,
            'line_profile':     line_profile,
            'name_srv_profile': line_profile
        })

        if not validator.validate():
            errors = validator.get_message()
            return Response({
                'success': False,
                'data': {
                    'errors': errors
                }
            })

        # Instancing huawei class
        huawei = Huawei(host, port, username, password)

        if not mode in ['router', 'brige']:
            message = 'Mode not valid.'
            log = ''
        elif not huawei.connect() :
            message = 'Could not connect to OLT.'
            log = ''
        else:
            huawei.authenticate()

            if mode == 'bridge':
                commands = [
                    'enable',
                    'config',
                    f'interface gpon 0/{slot}',
                    f'ont add {pon} {_id} sn-auth {serial} omci ont-lineprofile-name {line_profile} ont-srvprofile-name {name_srv_profile} desc {desc}\r\n',
                    f'ont port native-vlan {pon} {_id} eth 1 vlan {vlan} priority 0',
                    'quit',
                    f'service-port vlan {vlan} gpon 0/{slot}/{pon} ont {_id} gemport {gemport} multi-service user-vlan {user_vlan} tag-transform translate\r\n',
                    f'interface gpon 0/{slot}',
                    f'ont reset {pon} {_id}',
                    'y'
                ]
            else:
                commands = [
                    'enable',
                    'config',
                    # f'interface gpon 0/{slot}',
                    # f'ont add {pon} {_id} sn-auth {serial} omci ont-lineprofile-name {line_profile} ont-srvprofile-name {name_srv_profile} desc {desc}\n',
                    # f'ont port native-vlan {pon} {_id} eth 1 vlan {vlan} priority 0',
                    # 'quit',
                    # f'service-port vlan {vlan} gpon 0/{slot}/{pon} ont {_id} gemport {gemport} multi-service user-vlan {user_vlan} tag-transform translate\n',
                    # f'interface gpon 0/{slot}',
                    # f'ont reset {pon} {_id}',
                    # 'y'
                ]

            log = huawei.send(commands)
            message = 'Scripts executed successfully!'
            
        # Close telnet connection
        huawei.disconnect()

        success = huawei.has_failure(log) and len(log) != 0

        return Response({
            'success': success,
            'message': message,
            'data': {
                'log': log
            }
        })


class Unprovisioning(APIView):
    permission_classes = [ IsAuthenticated ]


    def post(self, request, *args, **kwargs):
        # Assign data
        host =      request.data.get('host')
        port =      request.data.get('port')
        username =  request.data.get('username')
        password =  request.data.get('password')
        _id =       request.data.get('id')
        slot =      request.data.get('slot')
        pon =       request.data.get('pon')

        # Validating request parameters
        validator = UnprovisioningValidator({
            'host':     host,
            'port':     port,
            'username': username,
            'password': password,
            '_id':      _id,
            'slot':     slot,
            'pon':      pon
        })

        if not validator.validate():
            errors = validator.get_message()
            return Response({
                'success': False,
                'data': {
                    'errors': errors
                }
            })

        # Instancing huawei class
        huawei = Huawei(host, port, username, password)

        if not huawei.connect():
            return Response({
                'success': False,
                'message': 'Could not connect to OLT.',
                'data': {
                    'ont_data': None,
                }
            })

        commands = [
            'enable',
            'config',
            f'undo service-port port 0/{slot}/{pon} ont {_id}\r\n',
            'y',
            f'interface gpon 0/{slot}',
            f'ont delete {pon} {_id}'
        ]

        huawei.authenticate()

        log = huawei.send(commands)

        huawei.disconnect()

        success = huawei.has_failure(log)

        return Response({
            'success': success,
            'message': 'Commands executed successfuly.',
            'data': {
                'log': log
            },
        })


class Customized(APIView):
    permission_classes = [ IsAuthenticated ]
    

    def post(self, request, *args, **kwargs):  
        # Assign data
        host =      request.data.get('host')
        port =      request.data.get('port')
        username =  request.data.get('username')
        password =  request.data.get('password')
        commands =  request.data.get('commmands')

        # Validating request parameters
        validator = CustomizedValidator({
            'host':     host,
            'port':     port,
            'username': username,
            'password': password,
            'commands': commands
        })

        if not validator.validate():
            errors = validator.get_message()
            return Response({
                'success': False,
                'data': {
                    'errors': errors
                }
            })

        # Instancing huawei class
        huawei = Huawei(host, port, username, password)

        if huawei.connect():
            huawei.authenticate()
            log = huawei.send(commands)
            success = True
        else:
            success = False
            log = ''
            
        # Close telnet connection
        huawei.disconnect()

        return Response({
            'success': success,
            'data': {
                'log': log
            }
        })
