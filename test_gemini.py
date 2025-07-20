import google.generativeai as genai

genai.configure(api_key="AIzaSyAveH5p-m128V3QrgM_HiBTscAybhNwnIo")
model = genai.GenerativeModel("gemini-2.0-flash-exp")
response = model.generate_content("Write a simple Python hello world function")
print(response.text)