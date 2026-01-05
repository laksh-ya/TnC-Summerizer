# TnC-Summarizer

Made by Lakshya & Harsh as a Kaggle Capstone Project

**[Live Demo](https://lakshyaharshtnc.streamlit.app/)** | **[Colab Notebook](https://colab.research.google.com/drive/1EcEwBKEbZXV5GU7yHPlnluknfCxsNVKc)** | **[Video Demo](https://youtu.be/Q9QKhzHEMFE)** | **[Documentation](https://medium.com/@thebeasts9876/building-a-terms-conditions-summarizer-with-google-gemini-ai-d528ba245d33)**

## Overview

An AI-powered tool that automatically summarizes Terms & Conditions documents using Google's Gemini 2.0 Flash model. The tool extracts critical points, identifies potential risks, and provides actionable recommendations without requiring users to read through pages of legal text.

## The Problem

Studies show over 90% of users accept terms without reading them, potentially agreeing to concerning clauses about data usage, privacy, and legal rights. This tool addresses that gap by making T&Cs digestible and highlighting what actually matters.

## How It Works

The summarizer processes T&C documents and outputs structured information in three sections:

1. **Critical Watchpoints**: Two key risk points hidden in the document
2. **Recommended Action**: One actionable piece of advice based on identified risks
3. **Summary**: Ten key points covering the entire document

Uses few-shot learning to train the model on recognizing patterns like data sharing concerns, termination policies, liability limitations, and arbitration clauses.

## Tech Stack

- Google Generative AI (Gemini 2.0 Flash)
- PyPDF2 for PDF handling
- Python Requests library
- Streamlit for web deployment
- Google Colab for development

## Key Features

- Condenses lengthy legal text into essential points
- Highlights potentially problematic clauses
- Translates legal jargon into plain language
- Identifies patterns across various document types

## Installation

```bash
pip install --upgrade google-generativeai
pip install PyPDF2
pip install requests
pip install streamlit
```

## Usage

1. Configure your Google Gemini API key
2. Input your T&C document (text or PDF)
3. Get instant structured summary with risk analysis

## Sample Output Format

```
📋 T&C Summary
- [10 clear, concise points about the terms]

⚠️ Critical Watchpoints
- [2 major risk points with explanations]

💡 Recommended Action
- [1 actionable advice based on the analysis]
```




## Contributors

- Lakshya
- Harsh Tripathi
