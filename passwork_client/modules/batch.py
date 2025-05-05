class Batch:
    """
        Batch request method
    """
    def send_batch(self, requests: list):

        batch = 25
        responses = []
        batch_request = []
        for request in requests:
            batch_request.append(request)

            if (len(batch_request) % batch) == 0:
                responses.extend(self.batch_request(batch_request))
                batch_request.clear()

        if len(requests) > 0:
            responses.extend(self.batch_request(requests))

        return responses

    def batch_request(self, requests: list):
        responses = self.call("POST", "/api/v1/batch", {"requests": requests})

        response_data = []
        for response in responses["responses"]:
            if response["statusCode"] == 200:
                response_data.append(response["body"])

        return response_data