#!/usr/bin/env python3
"""
a function called filter_datum that returns the log message obfuscated:
Arguments:
fields: a list of strings representing all fields to obfuscate
redaction: a string representing by what the field will be obfuscated
message: a string representing the log line
separator: a string representing by which character is separating all fields in the log line (message)
The function should use a regex to replace occurrences of certain field values.
filter_datum should be less than 5 lines long and use re.sub to perform the substitution with a single regex.
"""
import logging
import csv


def filter_datum(fields, redaction, message, separator):
    return filter_datum

import logging

class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class."""
    
    REDACTION = "***"

    def __init__(self, fields=None):
        """Initialize the formatter with a list of fields to redact."""
        self.fields = fields if fields else []
        super().__init__()

    def filter_datum(self, datum):
        """Helper method to redact specified fields."""
        for field in self.fields:
            if field in datum:
                datum = datum.replace(field, self.REDACTION)
        return datum

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record and redact specified fields."""
        log_message = super().format(record)
        return self.filter_datum(log_message)

def get_logger():
    """Create and return a configured logger."""
    # Create a logger named 'user_data'
    logger = logging.getLogger('user_data')

    # Set the log level to INFO
    logger.setLevel(logging.INFO)

    # Ensure it does not propagate messages to other loggers
    logger.propagate = False

    # Create a stream handler (console output)
    console_handler = logging.StreamHandler()

    # Create the RedactingFormatter with PII_FIELDS
    formatter = RedactingFormatter(fields=PII_FIELDS)

    # Apply the formatter to the handler
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    return logger
