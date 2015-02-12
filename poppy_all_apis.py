import json
import uuid
import locust
import random


class PoppyTasks(locust.TaskSet):

    tenant_id = "862456"
    token = "fa0c1b8e1baf47ab9d97197d2e23ce03"
    headers = {"Content-Type": "application/json",
                                  "X-Project-ID": tenant_id,
                                  "Accept": "application/json",
                                  "X-Auth-Token": token}
    service_ids = []

    @locust.task(2)
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
                                    headers=self.headers)
        print "Response for get is:", response.status_code
        print "Response content is:", response.content
        print "Response extra content is: ", response.headers['location']
        service_id = response.headers['location'].split('/')[-1]
        print "Service id:", service_id
        self.service_ids.append(service_id)

    @locust.task(2)
    def update_service(self):
        patch_data_update = [{
            "op": "add",
            "path": "/domains/-",
            "value": {
                "domain": "newDomain.com",
                "protocol": "http"
            }
        }]
        service_id = self.service_ids.pop()
        update_response = self.client.patch('/'+self.tenant_id+'/services/'
                                            +service_id,
                                            data=json.dumps(patch_data_update),
                                            headers=self.headers)
        self.service_ids.put(service_id)
        print "Response for update is:", update_response.status_code
        print "Response content is:", update_response.content
        print "Response xtra content is: ", update_response.headers['location']

    @locust.task(1)
    def delete_service(self):
        service_id = self.service_ids.pop()
        delete_response = self.client.delete('/'+self.tenant_id+'/services/'
                                             +service_id,
                                             headers=self.headers)
        print "Response for delete is:", delete_response.status_code
        print "Response content is:", delete_response.content
        print "Response xtra content is: ", delete_response.headers['location']

    @locust.task(10)
    def delete_asset(self):
        service_id = self.service_ids.pop()
        self.client.delete('/'+self.tenant_id+'/services/'+service_id
                           +'/assets',
                           headers=self.headers,
                           params={'url': self._pick_asset()})
        self.service_ids.put(service_id)

    @locust.task(10)
    def delete_all_assets(self):
        service_id = self.service_ids.pop()
        self.client.delete('/'+self.tenant_id+'/services/'+service_id
                           +'/assets',
                           headers=self.headers,
                           params={'all': True})
        self.service_ids.put(service_id)

    @locust.task(20)
    def list_services(self):
        self.client.get('/'+self.tenant_id+'/services', headers=self.headers)

    @locust.task(10)
    def get_service(self):
        service_id = self.service_ids.pop()
        self.client.get('/'+self.tenant_id+'/services/'+service_id,
                        headers=self.headers)
        self.service_ids.put(service_id)

    @locust.task(4)
    def list_flavors(self):
        self.client.get('/'+self.tenant_id+'/flavors', headers=self.headers)

    @locust.task(4)
    def get_flavors(self):
        self.client.get('/'+self.tenant_id+'/flavors/'+self._pick_flavor(),
                        headers=self.headers)

    def _pick_flavor(self):
    # what if new flavors? do we care?
        return random.choice(('cdn', 'երանգ'))

    def _pick_asset(self):
    # TODO: idk my bff jill
        return '/index.html'


class PoppyLocust(locust.HttpLocust):

    host = "https://preview.cdn.api.rackspacecloud.com/v1.0"
    task_set = PoppyTasks
    min_wait = 1000
    max_wait = 1000
