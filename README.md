# AI Assistant for Kids

This repository contains the codebase for an AI assistant specifically designed for children. The project is integrated with Streamlit for testing and currently supports text and speech modalities, with plans to incorporate vision in future updates. The AI assistant is tailored to interact with kids, remembering their preferences and previous interactions to provide personalized responses. This memory feature works both within and across sessions, allowing the assistant to maintain context and continuity in its conversations.

## Features

- **Text and Speech Interaction**: Kids can communicate with the assistant via typing or speaking.
- **Session Memory**: The assistant remembers previous interactions and adapts its responses accordingly.
- **Future Vision Integration**: Plans to integrate visual input to enhance interaction.

## Getting Started

To run the application locally, follow these steps:

1. **Install Dependencies**: Install the required packages by running the following command:
   ```bash
   pip install -r requirements.txt

2. Run the Application: Start the Streamlit app by executing:
   ```bash
   streamlit run app.py

3. Interact with the Assistant: Once the Streamlit UI launches, choose between the following options:

    Record and Get Response: Use speech input for interaction.
   
    Type and Get Response: Use text input for interaction.

## Code Structure
app.py: The main file that sets up the Streamlit UI.

speech2Text.py: Handles the conversion of voice input to text.

text2Speech.py: Converts the assistant's text responses into speech.

## Future Enhancements
Vision Modality: Integration of visual input to further enrich interactions.

Mobile App Development: The ultimate goal is to transition this project into a mobile application, making it easily accessible for kids.
