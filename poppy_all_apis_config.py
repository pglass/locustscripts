# coding:utf-8
host = "https://preview.cdn.api.rackspacecloud.com/v1.0"
min_wait = 3 * 1000
max_wait = 3 * 1000

tenant_id = None
token = None

create_service_weight = 5
update_service_domain_weight = 0
update_service_rule_weight = 5
delete_service_weight = 5
delete_asset_weight = 50
delete_all_assets_weight = 50
list_services_weight = 100
get_service_weight = 50
list_flavors_weight = 20
get_flavors_weight = 20

flavors = ['cdn', 'երանգ']
