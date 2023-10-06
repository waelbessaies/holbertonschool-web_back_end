#!/usr/bin/env python3

import re
import logging
import os
import mysql.connector
from typing import List

# Define Personally Identifiable Information (PII) fields to redact in log messages
PII_FIELDS = ("name", "email", "phone", "ssn", "password")

# Custom Formatter class for redacting PII in log messages


class RedactingFormatter(logging.Formatter):
    """ Custom log formatter to redact sensitive information """

    # Redacted text to replace PII
    REDACTION = "***"

    # Log message format
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"

    # Separator between fields in log message
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

# Function to redact PII in a log message


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Redacts specified fields in a log message.

    Args:
        fields: List of PII fields to obfuscate
        redaction: Represents the text by which the field will be obfuscated
        message: The log message to redact
        separator: String used to separate fields in the log message

    Returns:
        Protected log message with redacted PII
    """
    for field in fields:
        message = re.sub(rf"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message

# Function to create and configure the logger


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger for the user_data module.

    Returns:
        logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger

# Function to establish a database connection


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes a connection to the database.

    Returns:
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

# Main function to retrieve and log user data while redacting PII


def main():
    """
    Main function to connect to the database, retrieve user records,
    and log them with redacted PII.
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
