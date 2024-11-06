# 0x00. Personal Data

## Overview
This project is focused on implementing personal data protection mechanisms in a back-end system. You’ll gain practical skills in handling Personally Identifiable Information (PII), including logging sensitive information securely, encrypting passwords, and authenticating to databases using environment variables.

**Project Weight:** 1  
**Start Date:** November 6, 2024, 6:00 AM  
**Deadline:** November 8, 2024, 6:00 AM  
**Checker Release:** November 6, 2024, 6:00 PM  

After completing the project, request a **Manual QA review**. An automatic review will be conducted at the deadline.

---

## Learning Objectives
By the end of this project, you should be able to:

1. **Identify PII Examples**  
   Recognize examples of Personally Identifiable Information (PII) and understand how to handle them responsibly.

2. **Implement Log Filters for Obfuscation**  
   Develop a log filter that masks PII fields to protect sensitive data in logs.

3. **Encrypt and Validate Passwords**  
   Use the `bcrypt` library to securely encrypt passwords and check the validity of input passwords.

4. **Database Authentication Using Environment Variables**  
   Authenticate securely to a database by using environment variables to manage sensitive credentials.

---

## Resources
Make sure to review the following resources:

- [What Is PII, non-PII, and Personal Data?](https://example.com)
- [Python logging documentation](https://docs.python.org/3/library/logging.html)
- [bcrypt package documentation](https://pypi.org/project/bcrypt/)
- [Logging to Files, Setting Levels, and Formatting](https://realpython.com/python-logging/)

---

## Requirements
- **Environment:** Ubuntu 18.04 LTS
- **Python Version:** Python 3.7
- **Style Guide:** Follow the `pycodestyle` style (version 2.5)
- **File Specifications:**
  - Each file must end with a new line.
  - First line of each file: `#!/usr/bin/env python3`
  - Files must be executable.
  - File length will be tested with `wc`.
- **Documentation Requirements:**
  - All modules, classes, and functions should have clear, descriptive documentation.
  - Each function should be type annotated.

---

## Project Structure
Your project should include:

1. **Logging Configuration**  
   Implement a logging setup that obfuscates PII data fields (e.g., names, email addresses, phone numbers) to ensure logs do not contain sensitive information in plain text.

2. **Password Encryption and Verification**  
   Use the `bcrypt` package to hash passwords securely and create functions to verify that user inputs match stored hashes.

3. **Environment-Based Database Authentication**  
   Authenticate to your database by securely retrieving credentials from environment variables, rather than hardcoding them.

---

## Setup Instructions
1. Install dependencies:
   ```bash
   pip install bcrypt
