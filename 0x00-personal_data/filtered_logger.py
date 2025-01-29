#!/usr/bin/env python3
"""
Defines a function and classes for redacting PII in log messages.
"""
from typing import List
import re
import logging
import os
import mysql.connector


# Fields with personally identifiable information (PII)
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates fields in a log message with a redaction string.

    Args:
        fields (list): Fields to obfuscate.
        redaction (str): String used to replace sensitive data.
        message (str): The log message to redact.
        separator (str): Separator between fields in the message.

    Returns:
        str: The redacted message.
    """
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Formatter class to redact PII in log messages. """

    REDACTION = "***"  # Redaction string
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"  # Separator for fields

    def __init__(self, fields: List[str]):
        """
        Initializes RedactingFormatter with fields to redact.

        Args:
            fields (list): Fields to redact in the logs.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats and redacts the log message.

        Args:
            record (logging.LogRecord): LogRecord instance.

        Returns:
            str: The formatted log message with redacted fields.
        """
        message = super(RedactingFormatter, self).format(record)
        redacted = filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)
        return redacted


def get_logger() -> logging.Logger:
    """
    Returns a configured logger with redacting formatter.

    Returns:
        logging.Logger: The configured logger.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes a connection to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection: The database connection.
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    conn = mysql.connector.connect(user=user, password=passwd,
                                   host=host, database=db_name)
    return conn


def main():
    """
    Main function to fetch and log user data with redaction.
    """
    db = get_db()
    logger = get_logger()

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = cursor.column_names

    for row in cursor:
        message = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        logger.info(message.strip())

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()  # Run the main function
