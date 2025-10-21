
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model, ModelInference
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames
import credentials as creds
import utils

model_id = "meta-llama/llama-4-maverick-17b-128e-instruct-fp8"

credentials = Credentials(
                   url = creds.url,
                   api_key = creds.api_key
                  )

client = APIClient(credentials)


params = TextChatParameters()

model = ModelInference(
            model_id= model_id,
            credentials=credentials,
            project_id=creds.project_id,
            params=params
        )   

def generate_model_response(encoded_image, user_query, assistant_prompt):
    """
    Sends an image and a query to the model and retrieves the description or answer.
    Formats the response using HTML elements for better presentation.
    """
    # Create the messages object
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": assistant_prompt + "\n\n" + user_query},
                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + encoded_image}}
            ]
        }
    ]

    try:
        # Send the request to the model
        response = model.chat(messages=messages)
        raw_response = response['choices'][0]['message']['content']

        # Format the raw response text using the format_response function
        formatted_response = utils.format_response(raw_response)
        return formatted_response
    except Exception as e:
        print(f"Error in generating response: {e}")
        return "<p>An error occurred while generating the response.</p>"
    

