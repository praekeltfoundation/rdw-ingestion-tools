from api.flow_results import pyFlows

flows = pyFlows().flows.get_flows()

print(flows.keys())
