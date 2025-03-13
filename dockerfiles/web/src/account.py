import base64
import glob
import io
import json
import os
import re
import shutil

import mimetypes
from fastapi import Request, Response, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import mysql.connector
import requests

from ulid import ULID
from PIL import Image, ImageFilter,ImageOps

import index
import database

from PIL import Image
from PIL.ExifTags import TAGS,GPSTAGS


def load_exif(path):
    ifd_dict = {}
    with Image.open(path) as im:
        exif = im.getexif()
    # {タグID: 値}の辞書を{タグ名: 値}の辞書に変換
    ifd_dict["Zeroth"] =  {TAGS[tag_id]: value for tag_id, value in exif.items() }
    ifd_dict["Exif"] =    {TAGS[tag_id]: value for tag_id, value in exif.get_ifd(0x8769).items()}
    ifd_dict["GPSInfo"] = {GPSTAGS[tag_id]: value for tag_id, value in exif.get_ifd(0x8825).items()}
    return ifd_dict,exif

class User:
    def __init__(self,request: Request):
        try:
            userResponse=requests.get(re.sub('$/', '', os.environ['account_server'])+'/getUserProfile/?token='+request.cookies.get('token'))
            user=json.loads(userResponse.text)
        except Exception as e:
            print("failed to auth : ",e)
            self.__ID=bytes(4)
            self.__emailAddress=""
            self.__displayName="anonymous"    
        else:
            self.__ID=base64.b64decode(user["ID"])
            self.__emailAddress=user["emailAddress"]
            self.__displayName=user["displayName"]

    @property
    def ID(self):
        return self.__ID
    @property
    def emailAddress(self):
        return self.__emailAddress
    @property
    def displayName(self):
        return self.__displayName
    
    def search(self,input:str=""):
        cursor = database.conn.cursor()
        try:
            if input=="":
                cursor.execute('''
                    select
                        post_ULID,
                        posted_by,
                        posted_at,
                        taken_at
                    from post;
                        '''
                        )
                postFilesData = cursor.fetchall()
            else:
                inputLoad=json.loads(input)
                tag=inputLoad["tag"][0]
                cursor.execute('''
                    select 
  post.post_ULID,
  posted_by,
  posted_at,
  taken_at
from tag_post_relation
inner join post on tag_post_relation.post_ULID = post.post_ULID
where tag_post_relation.tag_ID=%s;
                    ''',
                    (tag,)
                )
                postFilesData = cursor.fetchall()
        except Exception as e:
            print('failed to get (mysql error)')
            print(e)

        else:
            try:        
                searchResult=[]
                for postFileData in postFilesData:
                    searchResultFile={}
                    searchResultFile["ULID"]=postFileData[0]
                    searchResultFile["postedBy"]=postFileData[1]
                    searchResultFile["postedAt"]=postFileData[2].timestamp()
                    searchResultFile["takenAt"]=postFileData[3].timestamp()
                    searchResult.append(searchResultFile)
                return JSONResponse(content=searchResult)

            except Exception as e:
                print('failed to get (python error)')
                print(e)
        finally:
            cursor.close()

    def getPost(self,postID:str,size:str="full"):
        def crop_center(pil_img, crop_width, crop_height):
            img_width, img_height = pil_img.size
            return pil_img.crop(((img_width - crop_width) // 2,
                                (img_height - crop_height) // 2,
                                (img_width + crop_width) // 2,
                                (img_height + crop_height) // 2))
        def crop_max_square(pil_img):
            return crop_center(pil_img, min(pil_img.size), min(pil_img.size))
        def rotate(gazou):
            exif = gazou._getexif()
            if(exif and 274 in exif and exif[274]!=1):
                gazou = ImageOps.exif_transpose(gazou)
            return gazou
        cursor = database.conn.cursor()
        try:
            cursor.execute('''
    select
        file_name,
        content_type,
        file_path
    from post 
    where post_ULID=%s;
                ''',
                    (
                        postID,
                    )
                )
            postFileData = cursor.fetchone()
        except Exception as e:
            print('failed to get (mysql error)')
            print(e)
        else:
            try:        
                print(postFileData)
                if postFileData[2]=="":
                    postFilePath=os.path.join( "/storage",postID+mimetypes.guess_extension(postFileData[1]))
                else:
                    postFilePath=postFileData[2]
                if(size=="full"):
                    return FileResponse(path=postFilePath,media_type=postFileData[1])
                
                if(size=="thumbnail"):
                    im = Image.open(postFilePath)
                    img_bytes = io.BytesIO()
                    crop_max_square(rotate(im)).resize((100, 100)).save(img_bytes, format='webp')
                    img_bytes = img_bytes.getvalue()
                    return Response(content=img_bytes,media_type="image/webp")
            except Exception as e:
                print('failed to get (python error)')
                print(e)
        finally:
            cursor.close()
    def put(self,file:UploadFile):
        try:
            cursor = database.conn.cursor()
            try:
                print(
                    str(int.from_bytes(self.__ID, 'little'))+","+
                    file.filename+","
                )
                postULID=str(ULID())
                cursor.execute('''
                    INSERT INTO album.post (
                        `post_ULID`,
                        `posted_by`,
                        `file_name`,
                        `content_type`
                    ) values (
                        %s,
                        %s,
                        %s,
                        %s
                    );
                    ''',
                    (
                        postULID,
                        int.from_bytes(self.__ID, 'little'),
                        file.filename,
                        file.content_type
                    )
                )
                
                shutil.copyfileobj(file.file,open(os.path.join( "/storage", postULID+mimetypes.guess_extension(file.content_type)),'wb+'))
            except Exception as e:
                print('failed to index (mysql error)')
                print(e)
            database.conn.commit()
            cursor.close()
            index.index(postULID)
            print("hello")
        except Exception as e:
            print('failed to index (python error)')
            print(e)
    def registerFileFromPath(self):
        #for name in glob.glob('/Pictures/.*\.jpg'):
        #paths=glob.glob(r'/Pictures/スマホ写真/**/*.jpg', recursive=True)
        paths=glob.glob(r'/local/**/*.jpg', recursive=True)
        cursor = database.conn.cursor()
        for i,path in  enumerate(paths):
            try:
                print("\n\n")
                print("["+str(len(paths))+"/"+str(i)+"] : "+str(path))
                postULID=str(ULID())
                exif=load_exif(path)[0]
                cursor.execute('''
                    INSERT INTO album.post (
                        `post_ULID`,
                        `posted_by`,
                        `file_name`,
                        `content_type`,
                        `file_path`,
                        `taken_at`
                    ) values (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    );
                    ''',
                    (
                        postULID,
                        int.from_bytes(self.__ID, 'little'),
                        re.search('(?<=/)[^/]*?$', path).group(),
                        "image/jpeg",
                        path,
                        exif["Exif"]["DateTimeOriginal"]
                    )
                )
                #if i>=3:
                    #break
            except Exception as e:
                print('failed to index (mysql error)')
                print(e)
                continue
            else:
                index.index(postULID)
                database.conn.commit()
        cursor.close()