#!/usr/bin/env python

# Import necessary modules
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.storage.sql_storage import SQLStorageAdapter  # Correct import

import openai
import unittest
from unittest.mock import patch

# Set your OpenAI API key
openai.api_key = "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"

# Create a ChatBot instance with a name
def create_chatbot():
    chatbot = ChatBot(
        "MyBot",
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        logic_adapters=[
            "chatterbot.logic.BestMatch",
            {
                'import_path': 'chatterbot.logic.MathematicalEvaluation',
            },
            {
                'import_path': 'chatterbot.logic.SpecificResponseAdapter',
                'input_text': 'Help me!',
                'output_text': 'Okay, here is some help.'
            }
        ],
    )
    trainer = ListTrainer(chatbot)
    trainer.train([
        "Hi", "Hello",
        "I need your assistance regarding my order", "Please provide me with your order ID",
        "Can you help me with my order status?", "Sure, I can help. Please provide your order ID",
        "I want to track my order", "To track your order, I need your order ID",
        "What is the delivery time for orders?", "Orders usually take 3-5 business days to be delivered",
        "I have a complaint about my order", "I'm sorry to hear that. Please explain your concern in detail",
        "How can I return an item?", "To initiate a return, please provide your order ID",
        "How are you", "I'm just a computer program here to help you!",
        "Okay, thanks", "No problem! Have a good day!",
        "Exit", "Goodbye! If you have more questions, feel free to ask."
            # Handling unexpected tokens
        "I don't understand",
        "I'm sorry, I didn't get that. Can you please rephrase?",

        "Invalid input",
        "I'm sorry, but I couldn't understand your input. Please try again.",

        # Handling unexpected questions
        "What is the meaning of life?",
        "I'm not equipped to answer philosophical questions, but I can help you with certain topics. Try asking about orders or general assistance.",

        # Handling unexpected commands
        "Do a backflip!",
        "I'm just a text-based program, so I can't perform physical actions. How about I assist you with something else?",

        # Handling unexpected topics
        "Tell me a joke",
        "I'm programmed to assist with orders and related queries. If you have any order-related questions, feel free to ask!",

        # Handling unexpected language
        "Bonjour",
        "Hello! I understand English better. How can I assist you today?",

        # Handling unexpected symbols or characters
        "!@#$%",
        "I'm sorry, but I don't understand that input. Please provide a valid request or question.",

        # Handling unexpected length
        "a" * 100,
        "Your input is too long. Please provide a concise request or question.",
   


    ])
    return chatbot


# Function to generate a response using OpenAI
def generate_response(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
   
    message = completions.choices[0].text
   
    # Check if the response contains unexpected content
    if "php" in message.lower():
        # If PHP-related content is detected, generate a different response
        return "I'm sorry, but I can't provide information on that topic."
   
    return message

# Function to predict a class based on the query
def predict_class(query, chatbot):
    response = chatbot.get_response(query)
   
    if response and response.confidence >= 0.9:
        # If the response is not None and has high confidence, return the response
        return response.text
   
    # If the confidence is low or the response is None, use OpenAI
    return generate_response(query)

# Create a ChatBot instance
chatbot = create_chatbot()

def is_order_id(input_text):
    # Implement your logic to check whether the input is an order ID
    # This could involve checking the format or consulting a database of orders
    # For simplicity, let's assume an order ID is alphanumeric and has a specific length
    return input_text.isalnum() and len(input_text) == 4  # Adjust the conditions as needed
def handle_order_query(order_id, chatbot):
    # Implement your logic to handle order-related queries based on the provided order ID
    # This could involve querying a database for order information or providing a predefined response
    # For simplicity, let's assume we're just acknowledging the order ID for now
    return f"Got it! I will assist you with order {order_id}. How can I help you further?"


# Function for the main conversation loop
def chat_loop():
    print("Bot: Hi! How can I assist you today? (Type 'exit' or 'quit' to end the chat)")
    while True:
        query = input("You: ")
        if query.lower() in ["bye","exit", "quit"]:
            print("Bot: Goodbye!")
            break  # Exit the loop
        response = predict_class(query, chatbot)
        print("Bot:", response)

# Test Chatbot class
class TestChatbot(unittest.TestCase):
    def test_known_query(self):
        response = predict_class("Hi", chatbot)
        self.assertEqual(response, "Hello")

    @patch("openai.Completion.create")
    def test_unknown_query(self, mock_openai):
        mock_openai.return_value = "Mock response"
        response = predict_class("Who are you?", chatbot)
        self.assertEqual(response, "Mock response")

if __name__ == "__main__":
    chat_loop()
