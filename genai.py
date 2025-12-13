from google import genai

api_key=""

client =genai.Client(api_key=api_key)
#in order to retain history or memory in this use this list of messages like this
messages =[{"role": "user", "parts":[{"{text}": "Your name is Tom"}]}] #in place of user you can also use "model" research changes

while True:
    user_input =input("YOU: ")
    if user_input.lower() == "exit":
        print("Goodbye")
        break

    response =client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_input
    )
    print(f"AI:", end="")
    full_reply=""
    for chunk in response:
        full_reply += chunk.text
        print(chunk.text, end="")
 #thus far we have only been using user input but there is no history hence the repetitive response to the same question
 #this is because it forgets what it said before
    messages.append({"role": "model", "parts":[{"{text}": full_reply}]})

