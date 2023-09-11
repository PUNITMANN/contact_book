import mysql.connector
import logging
import traceback
class DatabaseUtility:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="root@12345",
            database="contact_book",
        )
        self.cursor = self.connection.cursor()

    def execute_query(self, query):
        try:
            result = self.cursor.execute(query)
            self.connection.commit()
            status_code = 200
            return result, status_code
        except Exception as e:
            error_message = e.__str__()
            logging.error(error_message)
            traceback.print_exc()
            self.connection.rollback()

            result = "Some Internal Error Occurred"
            status_code = 500
            return result, status_code

    def read(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            status_code = 200
            return result, status_code
        except Exception as e:
            result = "Some Internal Error Occurred"
            status_code = 500
            return result, status_code

    def close_connection(self):
        self.cursor.close()
        self.connection.close()


def my_sql_execute_query(query):
    db_utility = DatabaseUtility()
    try:
        if query.lower().startswith("select"):
            try:
                response = db_utility.read(query)
            except Exception as e:
                error_message = e.__str__()
                logging.error(error_message)
                traceback.print_exc()
                response = {"status": "error", "message": "Some Internal Error Occurred", "status_code": 500}
        else:
            try:
                response = db_utility.execute_query(query)
            except Exception as e:
                error_message = e.__str__()
                logging.error(error_message)
                traceback.print_exc()
                response = {"status": "error", "message": "Some Internal Error Occurred", "status_code": 500}
    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
        response = {"status": "error", "message": "Some Internal Error Occurred", "status_code": 500}
    finally:
        db_utility.close_connection()
    return response
