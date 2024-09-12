# TLDR Science: A Personal Project

I was going down the rabbit hole of autoimmunity research, reading every article I could find. But the more I read, the more overwhelmed I became. I needed a way to parse through the noise and get to the good stuff.

That's when I turned to AI and programming to help me out. I built TLDR Science to automate the summarization of research papers, so I could focus on the big picture.


## Overview

TLDR Science is a personal project that aims to automate the summarization of scientific research papers into concise, easy-to-understand summaries. This project showcases my skills in:

* **Natural Language Processing (NLP)**: Text analysis and summarization techniques.
* **Software Development**: Designing and implementing a solution to automate summarization.
* **Critical Thinking**: Distilling complex research into key points and simple language.

# Building TLDR Science
====================================

## Step 1: Building the Basic Chrome Extension
------------------------------------

* Created a new directory for the project and created the basic files for a Chrome extension (manifest.json, popup.html, popup.js)
* Added the necessary permissions to the manifest.json file to allow the extension to access web pages and extract text
* Created a basic popup HTML file with a button to trigger the text extraction

## Step 2: Adding the Extension to Chrome as a Developer
-----------------------------------------------

* Went to the Chrome extensions page (chrome://extensions/) and enabled developer mode
* Clicked "Load unpacked" and selected the project directory to load the extension into Chrome
* Tested the extension to ensure it was loading correctly and displaying the popup

## Step 3: Creating the Button to Extract Text
-----------------------------------------

* Added a button to the popup HTML file to trigger the text extraction
* Used JavaScript to listen for the button click event and extract the text from the current web page
* Used the Chrome extension API to access the current tab and extract the text

## Step 4: Python Retrieves the Text
--------------------------------

* Set up a Python backend to receive the extracted text from the Chrome extension
* Used a library such as Flask to create a simple web server to receive the text
* Used a library such as requests to send the text from the Chrome extension to the Python backend

## Step 5: Technical Specificities to Make it Happen
----------------------------------------------

* Used the Chrome extension API to communicate between the Chrome extension and the Python backend
* Used a library such as PyChrome to handle the communication between the Chrome extension and the Python backend
* Set up a database (such as SQLite) to store the extracted text and summaries

## Step 6: Analyzing the Text using OpenAI GPT-4
--------------------------------------------

* Chose OpenAI GPT-4 for its large context window and ability to analyze long pieces of text
* Used the OpenAI API to send the extracted text to GPT-4 for analysis
* Received the analyzed text and summary from GPT-4 and stored it in the database

## Step 7: Output to PDF and Saved to Directory
---------------------------------------------

* Used a library such as ReportLab to generate a PDF from the summary
* Saved the PDF to a directory on the local machine

## Features and Functionality

* **Summarization Algorithm**: A custom-built algorithm to extract key points and generate summaries.
* **Web Interface**: A simple web interface to input research papers and view summaries.
* **Chrome Button**: A custom Chrome button to trigger summarization with a single click.

## Technologies Used

* **Programming Languages**: Python, JavaScript
* **Libraries and Frameworks**: NLTK, spaCy, Flask
* **Tools**: Chrome Extension API

## Benefits

* **Improved Understanding**: Simplify complex research into easy-to-understand summaries.
* **Time-Saving**: Quickly grasp the essence of scientific studies.
* **Enhanced Productivity**: Focus on key points and insights.

## Conclusion

TLDR Science demonstrates my ability to design and implement a solution to a complex problem using NLP and software development skills. I'm excited to apply these skills to future projects and collaborations.
