from fastapi import FastAPI, File, UploadFile, HTTPException, APIRouter
from app.api import db_manager
from typing import List

tables = APIRouter()


@tables.post("/uploadfile/")   #process new xlsx or csv file
async def create_upload_file(file: UploadFile = File(...), names: List[str] = None, index_col: List[str] = None, header: int = None):
    if(file.filename.split('.')[-1] == 'csv' or file.filename.split('.')[-1] == 'xlsx'):
        return await db_manager.new_file(file, names, index_col, header)
    raise HTTPException(status_code=406, detail="Wrong file format")

@tables.get("/")           #get list of existing tables names
async def get_tables_names():
    return await db_manager.get_table_names()
