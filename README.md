# savePhrase
API for receiving mp3 file, converting it to wav, saving it to disk and retrieving it

Database: database.db
Tables: 
users, (id primary key, userID string)
phrases, (id primary key, phraseID string)
pathsToFiles, (id primary key, userID string, phraseID string, pathToFile string)


Usage:
Build with docker
docker compose up --build

Exposes two endpoints on localhost:8000

GET /audio/user/{user_id}/phrase/{phrase_id}/{audio_format}
Retrieve an audio file with given userID and phraseID, returned in the given format. Currently only supports mp3

POST /audio/user/{user_id}/phrase/{phrase_id}
Send an mp3 file in the POST request (for example: --form ‘audio_file=@"./test.mp3"’). The file will be assigned 
to the given userID and phraseID. File is saved on disk on the server.

Remarks:
User input is currently not sanitised, so use with care to not destroy the database.
Sent files are not checked, so providing a non-mp3 file may cause unexpected behaviours because of the conversion.
