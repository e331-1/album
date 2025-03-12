import base64
import json
import os
import re
import requests
import uvicorn # type: ignore
from typing import Annotated

from fastapi import FastAPI, File, Response, UploadFile,Request,Header # type: ignore
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse

import account
app = FastAPI()

#import dockerfiles.web.src.index as index


if(os.environ.get('DEBUG')=="1"):
    import traceback
    import logging

    def stacktraceLines():
        tb = traceback.format_stack()
        ret = []
        for l in tb:
            p = l.find("\n")
            if p >= 0:
                # l には改行が含まれており、
                # 1行目はファイル名と行番号を含む
                # 2行目はその行のソースコード
                # それらを1行につなげる
                l = l[:p].strip() + ": " + l[p+1:].strip()
            if (
                # ライブラリのスタックトレースを除外して、自分で書いたコードのスタックトレースのみに絞る
                l.startswith("File \"/home/ubuntu/sample/") and
                not l.startswith("File \"/home/ubuntu/sample/initlog.py\"") # stacktraceLinesを定義しているソースを除外
            ):
                ret.insert(0, l) # スタックトレースの並び順をJava方式にするならば
                # ret.append(l) # スタックトレースの並び順をPython方式にするならば
        return ret

    class StackLogger(logging.Logger):
        def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, **kwargs):
            stacktraces = ["\n  " + l.replace("%", "%%") for l in stacktraceLines()]
            if len(stacktraces) > 0:
                msg = str(msg) + "".join(stacktraces)
            super()._log(level, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info, **kwargs)

    logging.setLoggerClass(StackLogger)

    import debugpy
    # port : 受付port
    port = 5678
    
    debugpy.listen(port)
    # addressとportを指定する場合はtupleでまとめて指定
    # debugpy.listen((address, port))

    # デバッガが接続されるまで待機
    debugpy.wait_for_client()

@app.post("/upload")
async def create_upload_files(request: Request,uploadFiles: list[UploadFile]):
    user=account.User(request)
    for uploadFile in uploadFiles:
        user.put(uploadFile)

    return {"filenames": [file.filename for file in uploadFiles]}


@app.get("/get")
async def get_post(request: Request,id:str,size:str="full"):
    user=account.User(request)
    try:
        return user.getPost(id,size)
    except Exception as e:
        return PlainTextResponse(content="404", status_code=404)

@app.get("/search")
async def search_post(request: Request,s:str=""):
    user=account.User(request)
    try:
        return user.search(s)
    except Exception as e:
        return PlainTextResponse(content="500", status_code=500)

@app.get("/registorsFromLocal")
async def search_post(request: Request):
    user=account.User(request)
    try:
        user.registerFileFromPath()
        return PlainTextResponse(content="done", status_code=200)
    except Exception as e:
        return PlainTextResponse(content="500", status_code=500)


@app.get("/test")
async def main():
    content = """
test
    """
    return HTMLResponse(content=content)


