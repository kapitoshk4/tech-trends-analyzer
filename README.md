# tech-trends-analyzer

This project is a web scraper and data analyzer for Python job vacancies on the [DOU website](https://jobs.dou.ua/). It collects job listings based on experience levels, extracts relevant data like job title, company, required technologies, and experience level, and then generates visual analyses of technology trends.
`

## Installation
   ```bash
   git clone https://github.com/yourusername/py-tech-trends-analyzer.git
   cd py-tech-trends-analyzer
   python3 -m venv venv
   source venv/scripts/activate
   pip install -r requirements.txt
   ```
## Configuration
In parse/config.py, you can customize the following:

TECHNOLOGIES: List of technologies to be identified in job listings.
EXPERIENCE_LEVELS: Mapping of experience page URLs to human-readable experience labels.

## Running the Scraper
To run the scraper and save vacancy data:
   ```bash
   python parse/parse.py
   ```
This will save the scraped job listings in data_analysis/vacancies.csv.

## Analyzing Data
After scraping, you can generate diagrams representing the distribution of technologies across vacancy listings:
   ```bash
   python data_analysis/data_analysis.py
   ```
This script will create diagrams in the data_analysis/diagrams/ folder, showing technology trends overall and for each experience level.

## Features
- **Scraping Job Listings:** Extracts Python job vacancies from DOU's job listings page for different experience levels.
- **Experience Levels:** 
  - Junior (0-1 years)
  - Middle (1-3 years)
  - Senior (3-5+ years)
- **Technology Extraction:** Identifies technologies mentioned in job descriptions based on a predefined list.
- **CSV Export:** Saves the collected data in a `vacancies.csv` file.
- **Data Analysis:** Generates bar diagrams showing the popularity of technologies in job listings overall and across different experience levels.

## Diagrams
- Overall technology frequency
![technology_frequency_overall.png](data_analysis%2Fdiagrams%2Ftechnology_frequency_overall.png)
- Junior technology frequency
![technology_frequency_junior.png](data_analysis%2Fdiagrams%2Ftechnology_frequency_junior.png)
- Middle technology frequency
![technology_frequency_middle.png](data_analysis%2Fdiagrams%2Ftechnology_frequency_middle.png)
- Senior technology frequency
![technology_frequency_senior.png](data_analysis%2Fdiagrams%2Ftechnology_frequency_senior.png)
