import pika,json

import pika.spec

def upload(f,fs,channel,access):
    try:
        fid = fs.put(f)
    except Exception as err:
        return str(err),500
    
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"]
    }
    
    try:
        channel.basic_publish(
            exchange="", # default exchange
            routing_key="video", #queue name
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
    except Exception as e:
        fs.delete(fid)
        return str(e),500