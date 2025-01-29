#!/usr/bin/env python3
"""
This script defines a function and classes for redacting personal information 
from log messages before they are logged. It helps ensure that sensitive 
data such as names, emails, and phone numbers are not exposed in log files.
"""
from typing import List
import re
import logging
import os
import mysql.connector


# Fields containing personally identifiable information (PII)
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates specified fields in the provided log message with a redaction string.

    Args:
        fields (list): A list of strings indicating the field names that contain PII to obfuscate.
        redaction (str): The string to replace the sensitive field values with.
        message (str): The log message to process and redact.
        separator (str): The character that separates the fields in the log message.

    Returns:
        str: The obfuscated log message with sensitive fields replaced by the redaction string.
    """
    for field in fields:
        # Use regex to find and replace field=value pairs with redacted values
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Custom logging formatter that redacts sensitive information in log messages. """

    REDACTION = "***"  # String used for redacting sensitive fields
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"  # Log message format
    SEPARATOR = ";"  # Separator between fields in the log message

    def __init__(self, fields: List[str]):
        """
        Initializes the RedactingFormatter with a list of fields to redact.

        Args:
            fields (list): List of field names to redact in the log messages.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log message and applies redaction to specified fields.

        Args:
            record (logging.LogRecord): The log record containing the message to format.

        Returns:
            str: The formatted log message with sensitive fields redacted.
        """
        # Format the message using the parent class formatter
        message = super(RedactingFormatter, self).format(record)
        # Apply redaction to the formatted message
        redacted = filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)
        return redacted


def get_logger() -> logging.Logger:
    """
    Creates and configures a logger that uses the RedactingFormatter to filter sensitive information.

    Returns:
        logging.Logger: A configured logger object.
    """
    logger = logging.getLogger("user_data")  # Logger name set to 'user_data'
    logger.setLevel(logging.INFO)  # Set the log level to INFO
    logger.propagate = False  # Prevent the log messages from being propagated to other loggers

    # Create a stream handler for logging to the console
    handler = logging.StreamHandler()

    # Use the custom RedactingFormatter to redact PII fields in the log messages
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)  # Set the formatter for the handler
    logger.addHandler(handler)  # Add the handler to the logger

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishes a connection to the MySQL database.

    Returns:
        mysql.connector.connection.MySQLConnection: A MySQL database connection object.
    """
    # Retrieve database connection details from environment variables or use defaults
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or "root"
    passwd = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ""
    host = os.getenv('PERSONAL_DATA_DB_HOST') or "localhost"
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    # Establish the connection to the database
    conn = mysql.connector.connect(user=user,
                                   password=passwd,
                                   host=host,
                                   database=db_name)
    return conn


def main():
    """
    Main entry point for the script. Retrieves user data from the database and logs it.

    This function fetches data from the 'users' table in the database, formats it 
    as a log message, and logs it using the configured logger with redaction applied.
    """
    # Get the database connection and logger
    db = get_db()
    logger = get_logger()

    cursor = db.cursor()  # Create a cursor to interact with the database
    cursor.execute("SELECT * FROM users;")  # Execute the query to fetch all user data
    fields = cursor.column_names  # Get the column names (field names)

    # Iterate over the rows of the result set and log each user data entry
    for row in cursor:
        # Format each row into a log message (field=value pairs)
        message = "".join("{}={}; ".format(k, v) for k, v in zip(fields, row))
        logger.info(message.strip())  # Log the message with redaction applied

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection


if __name__ == "__main__":
    main()  # Execute the main function when the script is run
