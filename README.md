# ChatGPT Log Analysis Project

## Overview

This project leverages ChatGPT to analyze logs stored in Elasticsearch, providing summaries and actionable advice based on the insights gained. By querying Elasticsearch, we can retrieve relevant log data and use ChatGPT to analyze patterns, summarize information, and provide valuable advice to users or administrators.

### Features

- **Summarization**: Uses ChatGPT to summarize log data and extract key insights.
- **Advice Generation**: Generates actionable advice based on the analyzed log data.
- **Natural Language Interaction**: Allows users to interact with the system in natural language.

## Requirements

- local elk stack (refer : https://github.com/birkanatici/ELK-stack)
- chatgpt api key
- python 3.7+

## Libraries

- elasticsearch
- openai
- flask
- json
- logging
- request
- jsonify
  
## Installation

1. Clone the repository:
   
   ```bash
   git clone https://github.com/chandu245/chatgpt-log-analyzer.git

2. Navigate to the project directory:

   ```bash
   cd chatgpt-log-analyzer

3. Start the app:

   ```bash
   py chatgpt-log-analyzer.py

## Contributions

Contributions are welcome! If you have any suggestions, ideas, or encounter any issues, please feel free to open an issue or submit a pull request.

## References

- https://github.com/elastic/chatgpt-log-analysis

## Acknowledgments

I would like to thank the developers of Elasticsearch, OpenAI's ChatGPT API, and other open-source libraries used in this project.

## Output

![](https://github.com/chandu245/chatgpt-log-analyzer/blob/main/output.png)
