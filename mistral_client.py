import os
from mistralai import Mistral

class MistralWrapper:
    def __init__(self, api_key=None):
        # Use API key from the environment if not explicitly provided
        self.api_key = '1TNjHnTyCxWE0K4zUfNyeGt1oMYSDCPV' #api_key or os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("Mistral API key is required. Set it in the environment or pass it explicitly.")
        self.client = Mistral(api_key=self.api_key)

    def request(self, endpoint, payload):
        url = f"https://mistral-api.example.com/{endpoint}"
        response = requests.post(url, json=payload, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code} - {response.text}")
        return response.json()

    def generate_completion(self, prompt, suffix="", model="codestral-latest", temperature=0.1, top_p=1):
        try:
            response = self.client.fim.complete(
                model=model,
                prompt=prompt,
                suffix=suffix,
                temperature=temperature,
                top_p=top_p,
            )
            if response and response.choices:
                return response.choices[0].message.content
            return None
        except Exception as e:
            print(f"Error generating completion: {e}")
            return None

    def _load_credentials(self):
        """
        Loads credentials from environment variables or raises an exception if not set.
        """
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("Mistral credentials (MISTRAL_API_KEY) are not set.")
        
        return {"api_key": api_key, "api_url": api_url}

    def _initialize_client(self):
        """
        Initializes and returns a Mistral client.
        """
        return MistralClient(api_key=self.credentials["api_key"], api_url=self.credentials["api_url"])

    def send_data(self, data, endpoint):
        """
        Sends data to a specific Mistral endpoint.
        
        Args:
            data (dict): The data to send.
            endpoint (str): The endpoint to interact with.

        Returns:
            dict: The response from Mistral.
        """
        try:
            response = self.client.post(endpoint, json=data)
            return response.json()
        except Exception as e:
            raise RuntimeError(f"Failed to send data to Mistral: {e}")

    def retrieve_data(self, endpoint, params=None):
        """
        Retrieves data from a specific Mistral endpoint.

        Args:
            endpoint (str): The endpoint to interact with.
            params (dict, optional): Query parameters.

        Returns:
            dict: The response from Mistral.
        """
        try:
            response = self.client.get(endpoint, params=params)
            return response.json()
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve data from Mistral: {e}")