from validator import Validator


class AutofindValidator(Validator):
    host =      'required'
    port =      'required'
    username =  'required'
    password =  'required'
    

class ProvisioningValidator(Validator):
    host =             'required'
    port =             'required'
    username =         'required'
    password =         'required'
    mode =             'required'
    id =               'required'
    slot =             'required'
    pon =              'required'
    serial =           'required'
    desc =             'required'
    vlan =             'required'
    gemport =          'required'
    user_vlan =        'required'
    line_profile =     'required'
    name_srv_profile = 'required'
    

class UnprovisioningValidator(Validator):
    host =             'required'
    port =             'required'
    username =         'required'
    password =         'required'
    _id =              'required'
    slot =             'required'
    pon =              'required'


class CustomizedValidator(Validator):
    host =             'required'
    port =             'required'
    username =         'required'
    password =         'required'
    commands =         'required'