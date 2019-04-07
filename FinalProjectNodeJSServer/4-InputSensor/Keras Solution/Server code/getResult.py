
import sys
arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg3 = sys.argv[3]
arg4 = sys.argv[4]
arg5 = sys.argv[5]


print({
	"id": arg5,
	"nodeInput": [1, 2, 3, 4],
	"alarmCondition": "No",
	"recomendationList": [
	{
		"id": "1",
		"databaseID":"101",
		"result": " a ROjhhhhit fndsjko; thsis"
	}, {
		"id": "2",
		"databaseID":"105",
		"result": " b do this"
	}, {
		"id": "3",
		"databaseID":"106",
		"result": " c do this"
	}, {
		"id": "4",
		"databaseID":"113",
		"result": " d do this"
	}, {
		"id": "5",
		"databaseID":"131",
		"result": " e do this"
	}]
})
sys.stdout.flush()