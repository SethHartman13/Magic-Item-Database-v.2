# Overview

I wanted to further my understanding and development of cloud databases as I wanted to work more with REST APIs. This is a redo of the code presented in [Magic Item Generator](https://github.com/SethHartman13/Magic-Item-Generator), this repository has a better interface and contains multithreading programming. This repository is being held seperate as the source code (not included in repository) contains content **not** covered under the Creative Commons Agreement released by Wizards of the Coast.

I have written 4 distinct programs that is run by main.py to fullfil the following HTTP requests:
- delete (Deletes JSON from DB)
- get (Retrieves JSON from DB)
- post (Adds JSON to DB)
- put (Updates JSON in DB)

All the programs are reliant on having the proper authentication to access the database, that is where google.oath2 comes into play because using Google Authentication service, I am able to ensure that I am the only one (or those who I allow) is able to access the database.

## Post

Post requires the following information from the user in order to post to the database:
1. Rarity of magic items that need to be sent to the database

The program does the rest as it sends a POST request to the database with the authentication and new JSON data


## Put

Post requires the following information from the user in order to post to the database:
1. Rarity of magic items that need to be updated

The program does the rest as it sends a PUT request to the database with the authentication and updated JSON data

## Get

Get requires the following information from the user in order to get information from the database:
1. Magic_item rarity
2. Number of magic_items desired

The program does the rest as it sends a GET request to the database with the authentication and returns the magic items with necessary details.

## Delete

Get requires the following information from the user in order to delete information from the database:
1. JSON (filename) containing magic_item data
2. file location containing magic_item data

The program does the rest as it sends a DELETE request to the database with the authentication.



I wrote this software because I was in need of a random loot generator for DnD campaigns that I run.

# Cloud Database

I am using Google Firebase's Realtime Database that uses REST APIs to perform Post, Put, Delete, and Get operations.

Realtime Database uses a JSON based data structure, allowing for the altering and creating of content in the database that primarily focuses on JSONs.

# Development Environment

Visual Studio Code is the source code editor used to write the Python programs and the JSON files.

Python

Google Authentication Libraries:
- google.auth.transport.requests
- google.oauth2

Built-in Python Libraries:
- json - JSON creation/loading library
- random - Random number generation
- time - time-related library
- webbrowser - Allows for the opening of http content (websites)
- threading - Allows for multithreading