import pika, json, tempfile, os
import pika.spec
from bson.objectid import ObjectId
from moviepy.editor import *
def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)
    #empty temp file
    try:
        tf = tempfile.NamedTemporaryFile() #automatically gets deleted
        #video contents
        out = fs_videos.get(ObjectId(message["video_fid"]))  #to get the file from mongodb
        print("file taken from mongodb : ",out)
        #add video contents to empty file
        tf.write(out.read())
        print("writen in empty file : ",tf.name)
        #create audio from temp video file
        audio = VideoFileClip(tf.name).audio
        print("created audio from temp file : ",audio.duration)
        tf.close()

        #write the audio to the file
        tf_path = tempfile.gettempdir()+ f"/{message['video_fid']}.mp3"
        audio.write_audiofile(tf_path) #creating the temp file for audio
        print("audio wrote in file : ",tf_path)
    except Exception as e:
        print("Error : ",e)
        return str(e)
    # save the file to mongo
    f = open(tf_path,"rb")
    data = f.read()
    fid = fs_mp3s.put(data)
    f.close()
    os.remove(tf_path) #not made with tempfile so doesn't auto delete
    
    message["mp3_fid"] = str(fid)
    print("message : ",message)
    try: #put the message on the queue that mp3 is available
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
    except Exception as err: # if we cant publish message on the queue then delete the mp3
        fs_mp3s.delete(fid)
        return "failed to publish message"