from agent.chat_session import ChatSession
from src.agent.llm_service import LLMService
from src.agent.news_service import NewsService
from src.agent.scraper_service import ScraperService

def main():
    session = ChatSession()
    llm = LLMService()
    news = NewsService()
    scraper = ScraperService()
    
    print("=" * 50)
    print("         AI News Agent")
    print("=" * 50)
    print("Type 'exit' to quit\n")
    
    # Initial greeting
    greeting = "I am your AI News Agent. What are you looking for today?"
    print(f"Bot: {greeting}\n")
    session.add_message("assistant", greeting)
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["exit", "quit"]:
            print("Bot: Goodbye!")
            break
        
        if not user_input:
            continue
        
        session.add_message("user", user_input)
        
        print("Bot: Thinking...", end="\r")
        response = llm.get_response(session.get_messages())
        
        # Handle SEARCH command
        if response.startswith("SEARCH:"):
            query = response.replace("SEARCH:", "").strip()
            print(" " * 30, end="\r")
            print(f"Bot: Searching for '{query}'...\n")
            
            articles = news.fetch_headlines(query)
            session.store_articles(articles)
            
            display = news.format_articles(articles, query)
            print(f"Bot: {display}\n")
            session.add_message("assistant", display)
        
        # Handle DETAIL command
        elif response.startswith("DETAIL:"):
            try:
                index = int(response.replace("DETAIL:", "").strip()) - 1
                article = session.get_article(index)
                
                if article:
                    print(" " * 30, end="\r")
                    print("Bot: Fetching full article details...\n")
                    
                    # Scrape the article using Firecrawl with fallback
                    url = article.get('url')
                    scraped_content = scraper.scrape_article(url, fallback_article=article)
                    
                    # Format with scraped content
                    detail = news.format_article_detail(article, scraped_content)
                    print(f"Bot: {detail}\n")
                    session.add_message("assistant", detail)
                else:
                    msg = "Sorry, I couldn't find that article. Please specify a valid number."
                    print(" " * 30, end="\r")
                    print(f"Bot: {msg}\n")
                    session.add_message("assistant", msg)
            except Exception as e:
                msg = f"Error fetching article details: {str(e)}"
                print(" " * 30, end="\r")
                print(f"Bot: {msg}\n")
                session.add_message("assistant", msg)
        
        # Handle normal response
        else:
            print(" " * 30, end="\r")
            print(f"Bot: {response}\n")
            session.add_message("assistant", response)

if __name__ == "__main__":
    main()