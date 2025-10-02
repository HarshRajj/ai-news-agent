# AI News Agent

An intelligent news search and summarization system that combines multiple AI services to provide natural language news discovery and analysis.

## Features

- 🤖 **Natural Language Processing**: Ask for news in plain English
- 📰 **Real-time News Search**: Access to 80,000+ news sources via NewsAPI.org
- 📅 **Date-specific Queries**: Search news by specific dates, ranges, or relative terms
- 🔍 **Progressive Search**: Automatic fallback to broader date ranges when no recent articles found
- 📄 **Full Article Extraction**: Scrape complete article content using Firecrawl
- 💬 **Conversational Interface**: Chat-like interaction with memory of previous queries
- 📊 **Smart Formatting**: Clean, readable article summaries and detailed views

## Architecture

The system follows a modular architecture with clear separation of concerns:

```
src/
├── main.py                 # Main entry point
├── config.py              # Configuration management
├── agent/
│   └── chat_session.py    # Conversation memory management
├── clients/               # External API wrappers
│   ├── llm_client.py      # Cerebras LLM integration
│   ├── news_client.py     # NewsAPI.org wrapper
│   └── scraper_client.py  # Firecrawl integration
├── parsers/               # Input processing
│   ├── date_parser.py     # Date parsing from queries
│   └── query_cleaner.py   # Query optimization
├── services/              # Business logic
│   ├── llm_service.py     # AI response generation
│   ├── news_service.py    # News search orchestration
│   ├── scraper_service.py # Web scraping coordination
│   └── response_formatter.py # Output formatting
├── models/                # Data structures
│   └── article.py         # Article data model
└── utils/                 # Helper functions
    └── text_helpers.py    # Text processing utilities
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd search-news
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   NEWSAPIORG_KEY=your_newsapi_key_here
   FIRECRAWL_API_KEY=your_firecrawl_key_here
   CEREBRAS_API_KEY=your_cerebras_key_here
   ```

## API Keys Setup

### NewsAPI.org
1. Visit [NewsAPI.org](https://newsapi.org/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add to `.env` file as `NEWSAPIORG_KEY`

### Firecrawl
1. Visit [Firecrawl](https://firecrawl.dev/)
2. Create an account
3. Get your API key
4. Add to `.env` file as `FIRECRAWL_API_KEY`

### Cerebras Cloud
1. Visit [Cerebras Cloud](https://cloud.cerebras.ai/)
2. Sign up for an account
3. Get your API key
4. Add to `.env` file as `CEREBRAS_API_KEY`

## Usage

1. **Start the application**:
   ```bash
   cd src
   python main.py
   ```

2. **Example interactions**:

   ```
   You: What's happening in AI today?
   Bot: Searching for 'AI today'...
   
   🔍 Here are the latest headlines:
   ==================================================
   
   📰 1. OpenAI Announces GPT-5 Development
      🔗 Source: TechCrunch | 📅 2025-10-02 at 14:30 UTC
      📋 OpenAI reveals plans for next-generation language model...
   
   📰 2. Google's New AI Chip Breakthrough
      🔗 Source: Wired | 📅 2025-10-02 at 12:15 UTC
      📋 Revolutionary tensor processing unit shows 40% improvement...
   
   💡 Type 'details [number]' to read the full article content.
   
   You: details 1
   Bot: Fetching full article details...
   
   📰 OpenAI Announces GPT-5 Development
   
   🔗 Source: TechCrunch
   ✍️ Author: Sarah Chen
   📅 Published: 2025-10-02 at 14:30 UTC
   🌐 URL: https://techcrunch.com/...
   
   ============================================================
   📄 FULL ARTICLE CONTENT
   ============================================================
   
   [Full scraped article content appears here...]
   ```

3. **Supported query types**:
   - **General topics**: "technology news", "climate change updates"
   - **Date-specific**: "news from yesterday", "this week's sports"
   - **Relative dates**: "3 days ago", "last month"
   - **Follow-up**: "details 2", "tell me more about the first one"

## Features in Detail

### Smart Date Parsing
- **Today/Yesterday**: "Show me today's tech news"
- **Relative dates**: "What happened 3 days ago?"
- **Week/Month ranges**: "This week's business news"
- **Specific dates**: "News from 2025-10-01"

### Progressive Search Fallback
When no recent articles are found:
1. Searches the past week automatically
2. Falls back to past month if needed
3. Notifies user about the fallback

### Intelligent Response Generation
- Natural language understanding via Cerebras LLM
- Context-aware responses
- Command generation for news searches
- Conversational memory

### Article Processing
- Full content extraction via Firecrawl
- Fallback to article summaries when scraping fails
- Content truncation to avoid token limits
- Clean markdown formatting

## Configuration

### LLM Settings
The system uses Cerebras Cloud's Llama-4 model with:
- Temperature: 0.7 (balanced creativity/accuracy)
- Max tokens: 1000
- Context window: Maintains last 6 conversation turns

### News Search Parameters
- Default limit: 5 articles per search
- Language: English
- Sort order: Most recent first
- Source coverage: 80,000+ news outlets

## Error Handling

The system includes robust error handling for:
- API rate limits and failures
- Network connectivity issues
- Invalid date formats
- Article scraping failures
- Malformed user inputs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Dependencies

### Core Services
- `cerebras_cloud_sdk`: LLM interactions
- `newsapi-python`: News data retrieval
- `firecrawl`: Web scraping
- `python-dotenv`: Environment management

### Supporting Libraries
- `pydantic`: Data validation
- `aiohttp`/`httpx`: HTTP clients
- `requests`: HTTP requests
- `datetime`: Date processing

See [`requirements.txt`](requirements.txt) for complete dependency list.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. **Import Errors**:
   - Ensure you're running from the `src/` directory
   - Check that all dependencies are installed

2. **API Key Errors**:
   - Verify `.env` file exists and contains valid keys
   - Check API key permissions and quotas

3. **No Articles Found**:
   - Try broader search terms
   - Check internet connection
   - Verify NewsAPI quota hasn't been exceeded

4. **Scraping Failures**:
   - System automatically falls back to article summaries
   - Check Firecrawl API quota and status

### Debug Mode

Enable debug output by setting in `.env`:
```env
DEBUG=true
```

This will show detailed API request/response information.

## Future Enhancements

- [ ] Support for multiple languages
- [ ] Article sentiment analysis
- [ ] News trend visualization
- [ ] Export functionality (PDF, HTML)
- [ ] Custom news source filtering
- [ ] Advanced search operators
- [ ] Real-time news alerts