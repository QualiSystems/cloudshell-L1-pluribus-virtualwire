from cloudshell.layer_one.core.response.resource_info.entities.base import ResourceInfo
from cloudshell.layer_one.core.response.resource_info.entities.port import Port


class VWPort(Port):
    MODEL_NAME = 'Generic L1 Port'

    def __init__(self, logical_id, phys_id, serial_number):
        name = self.NAME_TEMPLATE.format(logical_id)
        ResourceInfo.__init__(self, phys_id, name, self.FAMILY_NAME, self.MODEL_NAME, serial_number)
