# coding:utf-8
host = "https://preview.cdn.api.rackspacecloud.com/v1.0"
min_wait = 1000
max_wait = 1000

tenant_id = None
token = None

create_service_weight = 2
update_service_weight = 2
delete_service_weight = 1
delete_asset_weight = 10
delete_all_assets_weight = 10
list_services_weight = 20
get_service_weight = 10
list_flavors_weight = 4
get_flavors_weight = 4

flavors = ['cdn', 'երանգ']
