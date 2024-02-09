#!/usr/bin/env python3
"""
    a function that obfuscate a log message
"""
import logging
from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating
    """
    for field in fields:
        messages = re.sub('{}=.*?{}'.format(field, separator),
                          '{}={}'.format(separator, redaction), message)

    return messages


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"
    fields = ['']

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Function to filter values in incoming log records"""

        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'ip',)


def get_logger() -> logging.Logger:
    """
        a function that returns a logger object of user data
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list((PII_FIELDS))))
    logger.addHandler(stream_handler)

    return logger
