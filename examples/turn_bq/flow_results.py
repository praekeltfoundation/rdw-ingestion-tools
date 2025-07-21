from api.turn_bq import pyTurnBQ

flow_results = pyTurnBQ().flow_results.get_flow_results_by_id(
    stack_uuid="e060a3c1-d758-531f-b07b-9cc20895f572"
)

print(flow_results.collect().head(5))

flow_results = pyTurnBQ().flow_results.get_flow_results_by_updated_at(
    from_timestamp="2024-10-01T00:00:00", to_timestamp="2024-10-02T00:00:00"
)

print(flow_results.collect().head(5))
