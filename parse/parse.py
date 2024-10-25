import csv
import os
import re
import time
from urllib.parse import urljoin
from dataclasses import dataclass, fields

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import TECHNOLOGIES, EXPERIENCE_LEVELS

BASE_URL = "https://jobs.dou.ua/vacancies/"
PAGES = {
    "0-1": urljoin(BASE_URL, "?category=Python&exp=0-1"),
    "1-3": urljoin(BASE_URL, "?category=Python&exp=1-3"),
    "3-5": urljoin(BASE_URL, "?category=Python&exp=3-5"),
    "5plus": urljoin(BASE_URL, "?category=Python&exp=5plus"),
}


@dataclass
class Vacancy:
    title: str
    company: str
    technologies: str
    experience: str


VACANCY_FIELDS = [field.name for field in fields(Vacancy)]


class Scraper:
    def __init__(self, headless: bool = True) -> None:
        options = Options()
        options.headless = headless
        self.driver = webdriver.Edge(options=options)

    def click_load_more(self) -> None:
        try:
            while True:
                button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.more-btn a"))
                )
                if button and button.is_displayed():
                    button.click()
                    time.sleep(0.5)
                else:
                    break
        except Exception as e:
            print(f"Error while clicking 'Load more': {e}")

    def get_vacancy(self, vacancy_soup: BeautifulSoup, exp_level: str) -> Vacancy:
        vacancy_link = vacancy_soup.select_one("a.vt")["href"]
        self.driver.get(vacancy_link)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        title = soup.select_one(".l-vacancy > h1").text
        company = soup.select_one(".l-n a").text
        description = " ".join(element.text.strip() for element in soup.select(".l-vacancy *"))

        technologies = [
            tech for tech in TECHNOLOGIES if tech.lower() in description.lower()
        ]

        experience = self.extract_experience_level(title, exp_level)

        return Vacancy(
            title=title,
            company=company,
            technologies=", ".join(technologies),
            experience=experience,
        )

    def extract_experience_level(self, title: str, exp_level: str) -> str:
        for level in EXPERIENCE_LEVELS.values():
            if re.search(rf"\b{level}\b", title, re.IGNORECASE):
                return level.capitalize()
        return EXPERIENCE_LEVELS.get(exp_level)

    def get_page(self, page_url: str, exp_level: str) -> [Vacancy]:
        self.driver.get(page_url)
        self.click_load_more()
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        vacancies = soup.select("li.l-vacancy")

        return [self.get_vacancy(vacancy, exp_level) for vacancy in vacancies]

    @staticmethod
    def write_vacancies_to_csv(output_csv_path: str, vacancies: [Vacancy]) -> None:
        with open(output_csv_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(VACANCY_FIELDS)
            for vacancy in vacancies:
                writer.writerow([vacancy.title, vacancy.company, vacancy.technologies, vacancy.experience])

    def close(self) -> None:
        self.driver.quit()


def scrape_all_vacancies() -> None:
    scraper = Scraper()
    all_vacancies = []
    for exp_level, page_url in PAGES.items():
        print(f"Scraping {exp_level} experience level...")
        vacancies = scraper.get_page(page_url, exp_level)
        all_vacancies.extend(vacancies)
        print(f"Found {len(vacancies)} vacancies for {exp_level}.")

    base_dir = os.path.dirname(os.path.dirname(__file__))
    csv_directory = os.path.join(base_dir, "data_analysis")
    os.makedirs(csv_directory, exist_ok=True)
    csv_filename = os.path.join(csv_directory, "vacancies.csv")
    scraper.write_vacancies_to_csv(csv_filename, all_vacancies)
    print(f"Saved {len(all_vacancies)} vacancies to {csv_filename}.")

    scraper.close()


if __name__ == "__main__":
    scrape_all_vacancies()
