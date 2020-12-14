import speech_recognition as sr
r=sr.Recognizer()
print("Please Talk!")
with sr.Microphone() as source:
	audio_data=r.record(source, duration=5)
	print("Recognizing...")
	text=r.recognize_google(audio_data)
	print("You said: ")
	print(text)
	# find if certain words exist within said phrase
	if(text.find("begin") != -1 or text.find("start") != -1):
		print("The game will start soon!")
	elif(text.find("fight") != -1):
		print("Fighting mode!")
	elif(text.find("stop") != -1 or text.find("pause") != -1):
		print("Game has stopped! Say 'Resume' or 'Restart' or 'Continue' to come back!")
		with sr.Microphone() as source2:
			audio_data2=r.record(source2, duration=5)
			print("Recognizing...")
			text2=r.recognize_google(audio_data2)
			print("You said: " + text2)
			if(text2.find("resume") != -1 or text2.find("restart") != -1 or text2.find("continue") != -1):
				print("Welcome back!")