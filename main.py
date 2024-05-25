import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import tkinter as tk
from tkinter import simpledialog, messagebox

class AmazonReviewScraper:
    def __init__(self, master):
        self.master = master
        self.master.title("Amazon Review Scraper")

        self.scrape_btn = tk.Button(master, text="Scrape Reviews", command=self.scrape_reviews)
        self.scrape_btn.pack(pady=10)

    def scrape_reviews(self):
        url = simpledialog.askstring("URL", "Enter Amazon product URL:")
        if not url:
            return

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        reviews = []
        for review in soup.find_all('div', {'data-hook': 'review'}):
            review_text = review.find('span', {'data-hook': 'review-body'}).get_text().strip()
            reviews.append(review_text)

        if not reviews:
            messagebox.showerror("Error", "No reviews found or invalid URL")
            return

        sentiment_scores = [TextBlob(review).sentiment.polarity for review in reviews]
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)

        sentiment_message = f"Scraped {len(reviews)} reviews.\n\nAverage Sentiment Polarity: {avg_sentiment:.2f}\n"
        sentiment_message += "Positive" if avg_sentiment > 0 else "Negative" if avg_sentiment < 0 else "Neutral"
        
        messagebox.showinfo("Sentiment Analysis", sentiment_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = AmazonReviewScraper(root)
    root.mainloop()
