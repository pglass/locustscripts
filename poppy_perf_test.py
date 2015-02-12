__author__ = 'sabe6191'

import json
import uuid
import locust
import Queue

class PoppyTasks(locust.TaskSet):

    tenant_id = "862456"
    token = "ba80cd82227545e688ad0c649dcc91cb"
    headers = {"Content-Type": "application/json",
                                  "X-Project-ID": tenant_id,
                                  "Accept": "application/json",
                                  "X-Auth-Token": token}
    service_ids = Queue.Queue()

    @locust.task(1)
    def post_service(self):

        service_name = str(uuid.uuid1())

        domain_name = "qe_blog"+service_name

        post_data = {
            "domains": [
			    {"domain": domain_name+"mywebsite3.com"},
                {"domain": domain_name+".mywebsite.com"}],
			"caching": [
			    {"name": "default", "ttl": 3600},
			    {"name": "home", "ttl": 1200,
		        "rules": [{"name": "index", "request_url": "/index.htm"}]}
			],
			"flavorRef": "standard",
			"name": service_name,
            "flavor_id": "cdn",
			"origins": [
			    {"origin": "mywebsite1.com", "ssl": False, "port": 443}]}

        response = self.client.post('/'+self.tenant_id+'/services',
                                    data=json.dumps(post_data),
                                    headers=self.headers)
        print "Response for get is:", response.status_code
        print "Response content is:", response.content
        print "Response extra content is: ", response.headers['location']
        service_id = response.headers['location'].split('/')[-1]
        print "Service id:", service_id
        #self.service_ids.append(service_id)
        self.service_ids.put(service_id)

    @locust.task(1)
    def list_services(self):
        self.client.get('/'+self.tenant_id+'/services', headers=self.headers)

    @locust.task(1)
    def get_service(self):
        self.client.get('/'+self.tenant_id+'/services', headers=self.headers)

    @locust.task(1)
    def list_flavors(self):
        self.client.get('/'+self.tenant_id+'/services', headers=self.headers)

    @locust.task(1)
    def get_flavors(self):
        self.client.get('/'+self.tenant_id+'/flavors', headers=self.headers)

    @locust.task(1)
    def update_service(self):
        patch_data_update = [{
            "op": "add",
            "path": "/domains/-",
            "value": {
                "domain": "newDomain.com",
                "protocol": "http"
            }
        }]

        service_id = self.service_ids.get()
        update_response = self.client.patch('/'+self.tenant_id+'/services'+service_id,
                                            data=json.dumps(patch_data_update),
                                            headers=self.headers)
        self.service_ids.put(service_id)
        print "Response for update is:", update_response.status_code
        print "Response content is:", update_response.content
        print "Response xtra content is: ", update_response.headers['location']

    @locust.task(1)
    def delete_service(self):
        service_id = self.service_ids.get()
        delete_response = self.client.delete('/'+self.tenant_id+'/services'+service_id,
                                             headers=self.headers)
        print "Response for delete is:", delete_response.status_code
        print "Response content is:", delete_response.content
        print "Response xtra content is: ", delete_response.headers['location']


class PoppyLocust(locust.HttpLocust):

    host = "https://preview.cdn.api.rackspacecloud.com/v1.0"
    task_set = PoppyTasks
    min_wait = 1000
    max_wait = 1000