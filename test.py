


import json
import random
from locust import HttpUser, TaskSet, task, between


class SubClassTest(TaskSet):

    # @task
    # def main_page(self):
    #     f = open('mock_data.json')
    #     dataSet = json.load(f)

    #     self.client.post(
    #         '/authorization',
    #         data = random.choice(dataSet),
    #         headers = header_auth_token,
    #         catch_response = True
    #     )

    @task
    def main_page(self):
        # load mock data
        f = open('mock_data.json', 'r', encoding='utf-8')
        dataSet = json.load(f)

        testData = random.choice(dataSet)
        # Create rokok mock
        rokok = [{"id": random.randint(1, 10),
                 "stock": random.randint(10, 300)},
                 {"id": random.randint(1, 10),
                 "stock": random.randint(10, 300)}]
        testData.update(rokok)
        request_body_token = {
                'username': "spgstresstest",
                'password': "123456saga"
            }
        # Get token
        with self.client.post(
            '/auth/login',
            json=request_body_token,
            headers={'Content-Type': 'application/json'},
            catch_response=True
        )as response_token:
            if response_token.status_code == 200:
                response_token.success()
                res_payload_token = json.loads(response_token.text)
                token = res_payload_token['access_token']

                # Request with auth token
                with self.client.request(
                    method='POST',
                    url='/member',
                    headers={
                        'Authorization': 'Bearer ' + token
                    },
                    json=random.choice(dataSet),
                    catch_response=True
                ) as response_me:
                    if response_me.status_code == 201:
                        response_me.success()
                    else:
                        response_me.failure(
                            'Error request' + response_me.text)
            else:
                response_token.failure(
                    'Error request token ' + response_token.text)


class MainClassTest(HttpUser):
    tasks = [SubClassTest]
    wait_time = between(5, 10)
