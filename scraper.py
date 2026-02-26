from playwright.sync_api import sync_playwright

def run_scraper():
    total_sum = 0
    
    with sync_playwright() as p:
        # Launch headless Chromium
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Loop through the specific seeds provided in the task
        for seed in range(75, 85):
            url = f"https://sanand0.github.io/tdsdata/js_table/?seed={seed}"
            print(f"Scraping: {url}")
            page.goto(url)
            
            # CRITICAL: Wait for the dynamic table cells to render
            page.wait_for_selector("table td")
            
            # Extract all text from table cells using JavaScript evaluation for speed
            cell_texts = page.evaluate("""() => {
                const tds = document.querySelectorAll('table td');
                return Array.from(tds).map(td => td.innerText.trim());
            }""")
            
            # Sum the numbers safely
            for text in cell_texts:
                try:
                    total_sum += int(text)
                except ValueError:
                    pass # Skip any headers or non-numeric text
                    
        browser.close()
        
        # Print the final total so it appears in GitHub Actions logs
        print("\n" + "="*30)
        print(f"GRAND TOTAL: {total_sum}")
        print("="*30)

if __name__ == "__main__":
    run_scraper()
