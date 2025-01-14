if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Mistral Client Tester")
    parser.add_argument("--endpoint", required=True, help="Mistral API endpoint to interact with.")
    parser.add_argument("--data", help="Data to send as JSON string (for POST requests).")
    parser.add_argument("--params", help="Query parameters as JSON string (for GET requests).")
    parser.add_argument("--method", choices=["GET", "POST"], required=True, help="HTTP method to use.")

    args = parser.parse_args()

    mistral = MistralWrapper()

    if args.method == "POST" and args.data:
        import json
        data = json.loads(args.data)
        response = mistral.send_data(data, args.endpoint)
    elif args.method == "GET":
        import json
        params = json.loads(args.params) if args.params else None
        response = mistral.retrieve_data(args.endpoint, params=params)
    else:
        raise ValueError("Invalid combination of method and data/params.")

    print("Response from Mistral:")
    print(response)