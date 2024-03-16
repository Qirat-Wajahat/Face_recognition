import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
	'databaseURL':"https://facerecognition-fe087-default-rtdb.firebaseio.com/"
})

ref = db.reference('Student')

data = {
	"Iqbal":
		{
			"Name":"Iqbal",
			"major":"Poet",
			"starting_year":1969,
			"total_attendance":600,
			"standing":"G",
			"year":4,
			"last_attendance_time":"2024"
		},
	"Mujtaba":
		{
			"Name":"Mujtaba",
			"major":"Poet",
			"starting_year":1969,
			"total_attendance":0,
			"standing":"B",
			"year":2,
			"last_attendance_time":"2024"
		},
	"Quaid":
		{
			"Name":"Quaid",
			"major":"Lawer",
			"starting_year":1969,
			"total_attendance":1110,
			"standing":"G",
			"year":5,
			"last_attendance_time":"2024-1-6 00:54:36"
		}
}

for key, value in data.items():
	ref.child(key).set(value)