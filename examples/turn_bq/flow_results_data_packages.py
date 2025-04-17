from api.turn_bq import pyTurnBQ

flow_results_data_packages = (
    pyTurnBQ().flow_results_data_packages.get_flow_results_data_packages_by_id(
        stack_uuid="e6e2a502-c7f1-54c2-977e-fbe392a61bbf"
    )
)

print(flow_results_data_packages.head(5))

flow_results_data_packages = (
    pyTurnBQ().flow_results_data_packages.get_flow_results_data_packages_by_updated_at(  # noqa: E501
        from_timestamp="2023-10-01T00:00:00", to_timestamp="2023-10-10T00:00:00"
    )
)

print(flow_results_data_packages.head(5))
