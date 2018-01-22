from cloudshell.layer_one.core.response.resource_info.entities.base import ResourceInfo
from cloudshell.layer_one.core.response.resource_info.entities.port import Port


class VWPort(Port):

    def __init__(self, logical_id, phys_id):
        name = self.NAME_TEMPLATE.format(logical_id if len(str(logical_id)) > 1 else '0' + str(logical_id))
        ResourceInfo.__init__(self, phys_id, name, self.FAMILY_NAME, self.MODEL_NAME, 'NA')
