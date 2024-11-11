# 0x01. Basic Authentication

## Back-end | Authentication

**Project Duration:**  
- **Start:** Nov 11, 2024, 6:00 AM  
- **End:** Nov 13, 2024, 6:00 AM 

## Background Context

This project covers the fundamentals of authentication and demonstrates how to implement Basic Authentication on a simple API. While industry-standard applications typically use established libraries (e.g., Flask-HTTPAuth for Python-Flask), this project will help you gain a deep understanding of the mechanism by implementing it from scratch.

## Resources
Please refer to these resources for additional information:
- [REST API Authentication Mechanisms](#)
- [Base64 in Python](#)
- [HTTP header Authorization](#)
- [Flask Documentation](#)
- [Base64 Concept](#)

## Learning Objectives

By the end of this project, you should be able to explain the following concepts without external references:

### General
- The purpose and concept of authentication
- What Base64 encoding is and its applications
- How to encode a string in Base64
- The principles of Basic Authentication
- How to send the Authorization header in HTTP requests

## Requirements

### Python Scripts
- **Interpreter:** All files must run on Ubuntu 18.04 LTS with `python3` (version 3.7)
- **File format:** All files should end with a new line
- **Shebang:** The first line of each file should be `#!/usr/bin/env python3`
- **README:** A `README.md` file at the project root is mandatory
- **Code Style:** Use `pycodestyle` (version 2.5) for styling
- **Executable Files:** All scripts must be executable
- **File Length:** Tested with `wc` command

### Documentation
- **Modules:** Each module must have a descriptive docstring (`python3 -c 'print(__import__("my_module").__doc__)'`)
- **Classes:** Each class should have documentation (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`)
- **Functions:** Both standalone and class functions should include documentation:
  - For standalone functions: `python3 -c 'print(__import__("my_module").my_function.__doc__)'`
  - For class methods: `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`
- **Documentation Quality:** Each docstring should be a clear sentence explaining the purpose of the module, class, or method, as the length of the documentation will be verified.

## Project Outline

### Part 1: Authentication Fundamentals
- Study the meaning of authentication and the Basic Authentication protocol.
- Explore encoding techniques, focusing on Base64, and understand how it applies to Basic Authentication.

### Part 2: Basic Authentication Mechanism
- Implement a Basic Authentication system that accepts and verifies user credentials.
- Encode credentials in Base64 and include them in the HTTP `Authorization` header.
  
### Part 3: API Integration
- Test the authentication mechanism on a simple Flask API.
- Verify that authorized users can access protected endpoints.

### Expected Outcomes
- A functional Basic Authentication system for a sample API, with endpoints protected by Base64-encoded credentials in the Authorization header.