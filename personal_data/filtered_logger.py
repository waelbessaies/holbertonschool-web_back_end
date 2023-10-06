#!/usr/bin/env python3
"""
Module for filtered_logger
"""
import re
import logging
import os
import mysql.connector
from typing import List


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Constructor """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming log records using `filter_datum`
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Args:
        fields:       fields to obfuscate
        redaction:    represents by what the field will be obfuscated
        message:      the log line
        separator:    string by which character is separating all fields
                      in the log line (message)
    Returns:
    -------
        Protected log message
    """
    for field in fields:
        message = re.sub(rf"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


def get_logger() -> logging.Logger:
    """
    Instantiates a logging class
    Returns:
    -------
        logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Instantiates a mysql.connector.connection class
    Returns:
    -------
        mysql.connector.connection.MySQLConnection object connector
    """
    config = {
        'user': os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        'password': os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        'host': os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        'database': os.getenv("PERSONAL_DATA_DB_NAME")
    }
    connector = mysql.connector.connect(**config)
    return connector


def main():
    """
    Connects to the database `my_db` using `get_db` function, retrieves all
    rows in the `users` table and display each row under a filtered format.
    Filtered PII fields: name, email, phone, ssn, and password.
    Format example:
        [HOLBERTON] user_data INFO 2019-11-19 18:37:59,596: name=***;
        email=***; phone=***; ssn=***; password=***;
        ip=e848:e856:4e0b:a056:54ad:1e98:8110:ce1b;
        last_login=2019-11-14T06:16:24; user_agent=Mozilla/5.0
        (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; KTXN);
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    records = []
    for row in cursor:
        msg = f"name={row[0]}; email={row[1]}; phone={row[2]}; " \
              f"ssn={row[3]}; password={row[4]}; ip={row[5]}; " \
              f"last_login={row[6]}; user_agent={row[7]};"
        records.append(msg)

    logger = get_logger()
    for record in records:
        logger.info(record)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
