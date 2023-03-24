import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import openai
import config
import pywhatkit
import cv2
from simple_facerec import SimpleFacerec

openai.api_key = config.Api

from Features.voice import speak

# initialize speech recognition
r = sr.Recognizer()


engine =pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)



def speak(audio):
    print("Reply: " + audio)
    engine.say(audio)
    engine.runAndWait()


def face_verify():
    # Encode faces from a folder
    sfr = SimpleFacerec()
    sfr.load_encoding_images("images/")

    # Load Camera
    cap = cv2.VideoCapture(0)

    ret, frame = cap.read()

    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)
        print(name)
        return name

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)

    cap.release()
    cv2.destroyAllWindows()


# define the function that will take in voice input and return text output
def listen():
    # with sr.Microphone() as source:
    #     print("Listening...")
    #     r.pause_threshold = 1
    #     audio = r.listen(source)
    
    #     try:
    #         print("Recognizing...")
    #         query = r.recognize_google(audio, language='en-US')
    #         print(f"You said: {query}")
    #     except Exception as e:
    #         print(e)
    #         speak("Sorry, I didn't catch that. Can you please repeat?")
    #         return "None"
    #     return query

    query = input("Speak ")
    return query

def wish_me():
    hour = datetime.datetime.now().hour

    name = str(face_verify())

    if hour >= 0 and hour < 12:
        
        speak("Good morning! " + name)

    elif hour >= 12 and hour < 18:
        
        speak("Good afternoon! " + name)

    else:
        
        speak("Good evening! " + name)

    speak("What are the tasks for today")


def send_msg():
    speak("What Should i say Sir")
    msg = listen()
    pywhatkit.sendwhatmsg_instantly(user, msg)



if __name__ == "__main__":
    # face_verify()
    wish_me()
    while True:
        query = listen().lower()

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia...")
            speak(results)

        elif 'your' in query and 'name' in query:
            speak("My name is Veronica.")

        elif 'open youtube' in query:
            speak("Opening YouTube...")
            webbrowser.open("youtube.com")

        elif 'open vs code' in query:
            os.startfile("C:\\Users\\Uday Ahire\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
        

        elif 'open google' in query:
            speak("Opening Google...")
            webbrowser.open("google.com")

        elif 'created you' in query:
            speak("I was created by Abhinav.")

        elif 'send message' in query:
            if 'sanket' in query:
                user = "+917666308427"

            if 'uday' in query:
                user = "+919421548907"

            if 'ankita' in query:
                user = "+918805025921"

            if 'purva' in query:
                user = "+918530060344"

            send_msg()

        elif 'know her' in query and 'know him' in query:
            print(str(face_verify))
            if (str(face_verify()) != None):
                speak("Yes, Hello" + str(face_verify()) +" Nice to meet you")

            else:
                speak("Sorry I did not recognize you. ")

        


        elif 'quit' in query:
            speak("Goodbye!")
            break

        


        else:

            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=query,
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=[" Human:", " AI:"]
            )

            text = response['choices'][0]['text']
            # print('Reply: ' + text)
            speak(text)
