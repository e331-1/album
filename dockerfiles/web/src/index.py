import json
import mimetypes
import os
from huggingface_hub import hf_hub_download
from ultralytics import YOLO
from PIL import Image
import cv2
import numpy as np
import database
#lang_open = open('lang.json', 'r')
#lang_load = json.load(lang_open)


model_path = hf_hub_download(repo_id="davsolai/yolov8x-p2-coco", filename="model.pt")
#model_path="/app/model.pt"
model = YOLO(model_path)

def index(postULID:str):
    #image_path = "/workspaces/tensorflow/BurgerKing.jpg"
    cursor = database.conn.cursor()
    cursor.execute('''
    select
        file_name,
        content_type,
        file_path
    from post 
    where post_ULID=%s;
                ''',
                    (
                        postULID,
                    )
                )
    postFileData = cursor.fetchone()
    contentType=postFileData[1]
    if postFileData[2]=="":
        postFilePath=os.path.join( "/storage",postULID+mimetypes.guess_extension(contentType))
    else:
        postFilePath=postFileData[2]
    cursor.close()                    

    cursor = database.conn.cursor()
    targetImage=Image.open(postFilePath)
    
    results = model(targetImage)
    print(f"検出された物体: {len(results[0].boxes)} 個")

    for r in results:
        boxes = r.boxes
        for box in boxes:
            
            #print(lang_load[str(f"{box.cls[0]:.0f}")])
            try:
                cursor.execute('''
                        INSERT INTO album.tag_post_relation (
                            `post_ULID`,
                            `tag_ID`
                        ) values (
                            %s,
                            %s
                        );
                        ''',
                        (
                            postULID,
                            int(f"{box.cls[0]:.0f}")+1

                        )
                )
            except Exception as e:
                #print("mysql error(index) : ",e)
                continue
    database.conn.commit()
    cursor.close()