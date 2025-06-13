# # scrape_tds_site.py
# # Scrapes TDS content from sidebar-linked pages into a structured JSON file

# import time
# import json
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By

# # --- Setup Selenium WebDriver --- #
# print("🔧 Setting up Chrome WebDriver...")
# options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# options.add_argument("--window-size=1920,1080")
# driver = webdriver.Chrome(options=options)

# BASE_URL = "https://tds.s-anand.net"
# print(f"🌐 Navigating to {BASE_URL}")
# driver.get(BASE_URL)
# time.sleep(3)  # wait for JS to load sidebar

# # --- Parse Sidebar --- #
# print("📦 Parsing sidebar for section and file links...")
# soup = BeautifulSoup(driver.page_source, 'html.parser')
# sidebar = soup.select_one(".sidebar-nav")

# content_items = []

# for section in sidebar.select("li.folder"):
#     section_title = section.select_one("a").text.strip()
#     print(f"\n📁 Section: {section_title}")
#     section_ul = section.find("ul")
#     if not section_ul:
#         print("⚠️ No sub-sections found.")
#         continue

#     for file in section_ul.select("li.file"):
#         a_tag = file.select_one("a")
#         if not a_tag:
#             continue

#         subsection_title = a_tag.text.strip()
#         href = a_tag.get("href")
#         slug = href.lstrip("#")

#         print(f"  🔗 Subsection: {subsection_title} (slug: {slug})")

#         full_url = f"{BASE_URL}/{href}" if not href.startswith("http") else href
#         try:
#             driver.get(full_url)
#             time.sleep(1)

#             page_soup = BeautifulSoup(driver.page_source, 'html.parser')

#             # Wait for the actual content to load by checking for .page
#             page_main = page_soup.select_one(".page")
#             retries = 0
#             sections = page_soup.select("section")
#             #print(sections)
#             print(sections[0].select("article"))
#             print(len(sections))

#             content_items.append({
#                 "section": section_title,
#                 "subsection": subsection_title,
#                 "slug": slug,
#                 "content": page_text
#             })

#             print("    ✅ Page scraped successfully.")
#         except Exception as e:
#             print(f"    ❌ Failed to scrape {slug}: {str(e)}")

# # --- Save to JSON --- #
# print("\n💾 Saving scraped content to tds_content.json...")
# with open("tds_content.json", "w") as f:
#     json.dump(content_items, f, indent=2)

# print("✅ Done. All data saved to tds_content.json")
# driver.quit()

# scrape_tds_site.py
# Scrapes TDS content from sidebar-linked pages into a structured JSON file

import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# --- Helper Function --- #
def extract_text_with_links(article):
    output = []
    for element in article.descendants:
        if element.name == 'a' and element.get('href'):
            text = element.get_text(strip=True)
            href = element['href']
            output.append(f"{text} ({href})")
        elif element.name is None and element.strip():
            output.append(element.strip())
    return ' '.join(output)

# --- Setup Selenium WebDriver --- #
print("🔧 Setting up Chrome WebDriver...")
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

BASE_URL = "https://tds.s-anand.net"
print(f"🌐 Navigating to {BASE_URL}")
driver.get(BASE_URL)
time.sleep(3)  # wait for JS to load sidebar

# --- Parse Sidebar --- #
print("📦 Parsing sidebar for section and file links...")
soup = BeautifulSoup(driver.page_source, 'html.parser')
sidebar = soup.select_one(".sidebar-nav")

content_items = []

for section in sidebar.select("li.folder"):
    section_title = section.select_one("a").text.strip()
    print(f"\n📁 Section: {section_title}")
    section_ul = section.find("ul")
    if not section_ul:
        print("⚠️ No sub-sections found.")
        continue

    for file in section_ul.select("li.file"):
        a_tag = file.select_one("a")
        if not a_tag:
            continue

        subsection_title = a_tag.text.strip()
        href = a_tag.get("href")
        slug = href.lstrip("#")

        print(f"  🔗 Subsection: {subsection_title} (slug: {slug})")

        full_url = f"{BASE_URL}/{href}" if not href.startswith("http") else href
        try:
            driver.get(full_url)
            time.sleep(1)

            page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            sections = page_soup.select("section")

            if not sections:
                print("    ⚠️ No <section> found.")
                continue

            articles = sections[0].select("article")
            if not articles:
                print("    ⚠️ No <article> found.")
                continue

            page_text = extract_text_with_links(articles[0])

            content_items.append({
                "section": section_title,
                "subsection": subsection_title,
                "slug": slug,
                "content": page_text
            })
    
            print("    ✅ Page scraped successfully.")
        except Exception as e:
            print(f"    ❌ Failed to scrape {slug}: {str(e)}")

# --- Save to JSON --- #
print("\n💾 Saving scraped content to tds_content.json...")
with open("tds_content.json", "w", encoding="utf-8") as f:
    json.dump(content_items, f, indent=2, ensure_ascii=False)

print("✅ Done. All data saved to tds_content.json")
driver.quit()
