import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd

# URL of the website to scrape
BASE_URL = 'http://quotes.toscrape.com'

def get_limited_quotes(base_url, limit=20):
    page = 1
    all_quotes = []
    
    while len(all_quotes) < limit:
        url = f'{base_url}/page/{page}'
        response = requests.get(url)
        if response.status_code != 200:
            break
        
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')
        if not quotes:
            break
        
        for quote in quotes:
            text = quote.find('span', class_='text').get_text()
            author = quote.find('small', class_='author').get_text()
            tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
            all_quotes.append({
                'text': text,
                'author': author,
                'tags': tags
            })
            
            if len(all_quotes) >= limit:
                break
        
        page += 1

    return all_quotes

def main():
    st.title('Quote Scraper')
    st.write("Click the button below to scrape a limited number of quotes from the website.")

    if st.button('Scrape Quotes'):
        st.write("Scraping in progress...")
        quotes = get_limited_quotes(BASE_URL, limit=20)
        st.write(f'Successfully scraped {len(quotes)} quotes.')
        
        # Display quotes
        for quote in quotes:
            st.write(f"**Quote:** {quote['text']}")
            st.write(f"**Author:** {quote['author']}")
            st.write(f"**Tags:** {', '.join(quote['tags'])}")
            st.write("---")
        
        # Convert quotes to DataFrame and offer download as CSV
        df = pd.DataFrame(quotes)
        st.write("Download the scraped quotes as a CSV file:")
        st.download_button(
            label="Download CSV",
            data=df.to_csv(index=False),
            file_name='quotes.csv',
            mime='text/csv'
        )

if __name__ == '__main__':
    main()
