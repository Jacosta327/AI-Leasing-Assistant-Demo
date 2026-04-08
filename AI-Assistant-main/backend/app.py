# app.py
import gradio as gr
from chatbot import generate_reply  # Assumes your code is saved in chatbot.py

# Initialize the chat history
def respond(user_message, history, property_name):
    if not property_name:
        return "Please specify the property.", history

    reply = generate_reply(user_message, property_name)
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": reply})
    return "", history

with gr.Blocks() as demo:
    gr.Markdown("## 🏘️ AI Leasing Assistant\nAsk a question about a property.")
    
    with gr.Row():
        property_input = gr.Textbox(label="Property Name", placeholder="e.g., The Scarlet")
    
    msg = gr.Textbox(placeholder="Ask your leasing question here...", label="Message")
    chatbot = gr.Chatbot(label="AI Assistant", type="messages")
    clear = gr.Button("Clear")

    msg.submit(respond, [msg, chatbot, property_input], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()
