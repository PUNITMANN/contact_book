import logging
import traceback
from fastapi import FastAPI, Request, Path, HTTPException, Depends
from typing import List, Dict

from helpers.my_sql_connector import my_sql_execute_query
from signup_api.signup import sign_up
from login_api.login import log_in
from signup_api.utils import generate_api_key
from authorizer.authorizer import token_required
from phone_book.phone_book import phone_book, get_phone_book, update_phone_book, delete_phone_log


app = FastAPI()


@app.post("/signup")
@app.post("/signup/")
async def signup_api(request: Request):
    response = {"status": "Internal Server Error", "status_code": 500}
    try:
        data = await request.json()
        response = sign_up(data)

    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response


@app.post("/login")
@app.post("/login/")
async def login_api(request: Request):
    response = {"status": "Internal Server Error", "status_code": 500}
    try:
        data = await request.json()
        response = log_in(data)

    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response


@app.get("/create_x_api_key")
@app.get("/create_x_api_key/")
async def create_x_api_key(request: Request):
    response = {"status": "Internal Server Error", "status_code": 500}
    try:
        response = generate_api_key()
    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response


@app.post("/log_phone_entry")
@app.post("/log_phone_entry/")
@token_required
async def add_phone_number(request: Request):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:
        data = await request.json()
        user_id_payload = request.state.user_id
        user_id = user_id_payload.get("user_id", "")
        response = phone_book(data, user_id)
    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response


@app.get("/get_phone_logs")
@app.get("/get_phone_logs/")
@token_required
async def get_phone_number(request: Request):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:
        user_id_payload = request.state.user_id
        user_id = user_id_payload.get("user_id")
        response = get_phone_book(user_id)
    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response


@app.put("/update_phone_log/")
@app.put("/update_phone_log/{phone_number}")
@app.put("/update_phone_log/{phone_number}")
@token_required
async def update_phone_number(request: Request, phone_number: str = None):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:
        user_id_payload = request.state.user_id
        user_id = user_id_payload.get("user_id")
        data = await request.json()
        response = update_phone_book(data, user_id, phone_number)
    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response


@app.delete("/delete_phone_log/")
@app.delete("/delete_phone_log/{phone_number}")
@app.delete("/delete_phone_log/{phone_number}")
@token_required
async def delete_phone_number(request: Request, phone_number: str = None):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:
        user_id_payload = request.state.user_id
        user_id = user_id_payload.get("user_id")
        response = delete_phone_log(user_id, phone_number)
    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response

