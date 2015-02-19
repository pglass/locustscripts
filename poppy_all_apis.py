import json
import uuid
import locust
import random

import poppy_all_apis_config as CONFIG


class PoppyTasks(locust.TaskSet):

    tenant_id = CONFIG.tenant_id

    headers = {
        "Content-Type": "application/json",
        "X-Project-ID": CONFIG.tenant_id,
        "Accept": "application/json",
        "X-Auth-Token": CONFIG.token
    }
    service_ids = []

    def __init__(self, *args, **kwargs):
        super(PoppyTasks, self).__init__(*args, **kwargs)
        # create a service so everything doesn't fail initially
        print "Creating initial services"
        for _ in xrange(3):
            self.post_service()

    @locust.task(CONFIG.create_service_weight)
    def post_service(self):

        service_name = str(uuid.uuid1())
        domain_name = "qe_blog"+service_name

        post_data = {
            "domains": [{"domain": domain_name+"mywebsite3.com"},
                        {"domain": domain_name+".mywebsite.com"}],
            "caching": [{"name": "default", "ttl": 3600},
                        {"name": "home", "ttl": 1200,
                         "rules": [{"name": "index",
                                    "request_url": "/index.htm"}]}],
            "flavorRef": "standard", "name": service_name, "flavor_id": "cdn",
            "origins": [{"origin": "mywebsite1.com",
                         "ssl": False,
                         "port": 443}]}

        response = self.client.post('/'+self.tenant_id+'/services',
                                    data=json.dumps(post_data),
                                    headers=self.headers,
                                    name="/{tenant}/services")
        print "Response for get is:", response.status_code
        print "Response content is:", response.content
        print "Response extra content is: ", response.headers.get('location')
        if response.ok:
            service_id = response.headers['location'].split('/')[-1]
            print "Service id:", service_id
            self.service_ids.append(service_id)

    @locust.task(CONFIG.update_service_domain_weight)
    def update_service_domain(self):
        if not self.service_ids:
            print "WARNING: service_ids list is empty"
            return

        domain = "new_domain" + str(uuid.uuid1()) + ".com"
        patch_data_update = [{
            "op": "add",
            "path": "/domains/-",
            "value": {
                "domain": domain,
                "protocol": "http"
            }
        }]
        service_id = random.choice(self.service_ids)
        update_response = self.client.patch('/'+self.tenant_id+'/services/'
                                            +service_id,
                                            data=json.dumps(patch_data_update),
                                            headers=self.headers,
                                            name="/{tenant}/services/{id}")
        print "Response for patch service domain:", update_response.status_code
        print "Response content is:", update_response.content

    @locust.task(CONFIG.update_service_rule_weight)
    def update_service_rule(self):
        if not self.service_ids:
            print "WARNING: service_ids list is empty"
            return

        patch_data = [{
            "op": "replace",
            "path": "/caching/0",
            "value": {
                "name": "home",
                "ttl": random.randint(500, 2500),
            }
        }]

        service_id = random.choice(self.service_ids)
        update_response = self.client.patch('/'+self.tenant_id+'/services/'
                                            +service_id,
                                            data=json.dumps(patch_data),
                                            headers=self.headers,
                                            name="/{tenant}/services/{id}")
        print "Response for patch service rule:", update_response.status_code
        print "Response content is:", update_response.content

    @locust.task(CONFIG.update_service_origin_weight)
    def update_service_origin(self):
        if not self.service_ids:
            print "WARNING: service_ids list is empty"
            return

        random_origin = "mywebsite%s.com." % random.randint(1000000000,
                                                            9999999999)
        patch_data = [{
            "op": "replace",
            "path": "/origins/0",
            "value": {
                "origin": random_origin,
                "port": 80,
                "rules": [],
                "ssl": False
            }
        }]

        service_id = random.choice(self.service_ids)
        update_response = self.client.patch('/'+self.tenant_id+'/services/'
                                            +service_id,
                                            data=json.dumps(patch_data),
                                            headers=self.headers,
                                            name="/{tenant}/services/{id}")
        print "Response for patch service origin:", update_response.status_code
        print "Response content is:", update_response.content

    @locust.task(CONFIG.delete_service_weight)
    def delete_service(self):
        if not self.service_ids:
            print "WARNING: service_ids list is empty"
            return

        service_id = self.service_ids.pop()
        delete_response = self.client.delete('/'+self.tenant_id+'/services/'
                                             +service_id,
                                             headers=self.headers,
                                             name="/{tenant}/services/{id}")
        print "Response for delete is:", delete_response.status_code
        print "Response content is:", delete_response.content

    @locust.task(CONFIG.delete_asset_weight)
    def delete_asset(self):
        if not self.service_ids:
            print "WARNING: service_ids list is empty"
            return

        service_id = random.choice(self.service_ids)
        self.client.delete('/'+self.tenant_id+'/services/'+service_id
                           +'/assets',
                           headers=self.headers,
                           params={'url': self._pick_asset()},
                           name="/{tenant}/services/{id}/assets")

    @locust.task(CONFIG.delete_all_assets_weight)
    def delete_all_assets(self):
        if not self.service_ids:
            print "WARNING: service_ids list is empty"
            return
        service_id = random.choice(self.service_ids)
        self.client.delete('/'+self.tenant_id+'/services/'+service_id
                           +'/assets',
                           headers=self.headers,
                           params={'all': True},
                           name="/{tenant}/services/{id}/assets")

    @locust.task(CONFIG.list_services_weight)
    def list_services(self):
        self.client.get('/'+self.tenant_id+'/services', headers=self.headers,
                        name="/{tenant}/services")

    @locust.task(CONFIG.get_service_weight)
    def get_service(self):
        if not self.service_ids:
            print "WARNING: service_ids list is empty"
            return

        service_id = random.choice(self.service_ids)
        self.client.get('/'+self.tenant_id+'/services/'+service_id,
                        headers=self.headers, name="/{tenant}/services/{id}")

    @locust.task(CONFIG.list_flavors_weight)
    def list_flavors(self):
        self.client.get('/'+self.tenant_id+'/flavors', headers=self.headers,
                        name="/{tenant}/flavors")

    @locust.task(CONFIG.get_flavors_weight)
    def get_flavors(self):
        self.client.get('/'+self.tenant_id+'/flavors/'+self._pick_flavor(),
                        headers=self.headers,
                        name="/{tenant}/flavors/{flavor}")

    def _pick_flavor(self):
        return random.choice(CONFIG.flavors)

    def _pick_asset(self):
        return '/index.html'


class PoppyLocust(locust.HttpLocust):

    host = CONFIG.host
    task_set = PoppyTasks
    min_wait = CONFIG.min_wait
    max_wait = CONFIG.max_wait
