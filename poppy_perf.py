from locust import HttpLocust, TaskSet, task
import json
import uuid


class MyTaskSet(TaskSet):

    @task
    def create_service(self):

        service_name = str(uuid.uuid1())

        post_data = {
            "domains": [
			    {"domain": "mywebsite.com"}, {"domain": "blog.mywebsite.com"}],
			"caching": [
			    {"name": "default", "ttl": 3600},
			    {"name": "home", "ttl": 1200,
		        "rules": [{"name": "index", "request_url": "/index.htm"}]}
			],
			"flavorRef": "standard",
			"name": service_name,
			"origins": [
			    {"origin": "mywebsite1.com", "ssl": False, "port": 443}]}

        post_data2 = """
        {"domains": [{"domain": "orange2.cnamecdn.com"}], "caching": [{"name": "default", "ttl": 3600},{"name": "home","ttl": 1200,"rules": [{"name" : "index","request_url" : "/index.htm"}]}], "flavor_id": "cdn", "name": "manual-1", "origins": [{"origin": "104.130.27.124", "ssl": false, "port": 80}]}
        """

        response = self.client.post("/services", data=post_data2,  headers={"Content-Type": "application/json", "X-Project-ID": "862456", "Accept": "application/json", "X-Auth-Token": "0502f17c47554f5e961af3477240fa31"})
        print "Response for post is:", response.status_code
        print "Response content is:", response.content


    @task
	def get_service(self):
		self.client.get('/service/service_name')

class MyLocust(HttpLocust):
    host = "https://preview.cdn.api.rackspacecloud.com/v1.0"
    task_set = MyTaskSet
    min_wait = 5000
    max_wait = 15000

