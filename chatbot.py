# ----- Email pase to JSON -----
import openai
import json


def parse_email_with_chatbot(email_obj: dict, api_key: str) -> dict:
    """
    Parses an email object string using OpenAI's GPT-3.5 Chat model to extract relevant fields.
    Args:
        email_obj (dict): A string containing the email object.
        api_key (str): Your OpenAI API key.
    Returns:
        dict: A dictionary containing the extracted fields - 'sender_email' (from),
              'sender_name', 'summary', 'client_company', 'request', 'mb_change'.
    """
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
                "content": "Extrat a JSON with the following fields: 'requests' array field. Each element of 'requests' has the following fields: 'sender_email', 'sender_name', 'email_subject', 'client_company', 'Location', 'VLAN/IP', 'Location_A_(DPLC)', 'Location_B_(DPLC)', 'request', 'current_bandwidth_(Mbps)', 'PIB_or_DPLC', 'requested_bandwidth', 'new_bandwidth' from the text given below. Remember that the 'client company' field is the text after @ in the sender email address. The 'request' field value should be one of 'feasibility', 'upgrade' or 'downgrade', (the default is feasibility). The prioritize sender info in the Body field of the input. All extracted fields should be strings, empty string if empty. 'Location' is the address/location/site given should be same as 'Location_A_(DPLC)' for DPLC case. 'Location_A_(DPLC)', 'Location_B_(DPLC)' refer to the 2 port/points/locations given in the case of DPLC (Both are 'Nil' if not DPLC). For feasibility requests 'current bandwidth' is empty. 'PIB_or_DPLC' is PIB if not mentioned."},
            {"role": "user", "content": str(email_obj)}],
    )

    try:
        # Deserialize the JSON-like string response into a Python dictionary
        response_data = json.loads(
            response['choices'][0]['message']['content'])
        return response_data

    except json.JSONDecodeError as e:
        print("Error decoding JSON:")
        print(e)
        print("JSON content causing the error:")
        print(response['choices'][0]['message']['content'])
        return {}  # Return an empty dictionary or handle the error as needed
        return {}  # Return an empty dictionary or handle the error as needed
