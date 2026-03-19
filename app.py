from flask import Flask, render_template, request
import feedparser 

app = Flask(__name__)
 
# Needed: RSS feed URLs
# Have to specify URLs of an RSS feed to parse with feedparser 
# Key note: the URLs themselves has to have some sort of rss specification. Can't just 
# put in a url and expect it to work 
# Note : Anything on 'substack' automatically has rss enabled, just tack on /feed to the
# end
RSS_FEEDS = {
     'Hackernews': 'https://news.ycombinator.com/rss',
     'DeepMind': 'https://deepmind.com/blog/feed/basic/',
     'PyTorch': 'https://pytorch.org/feed',
     'TheZvi': 'https://thezvi.substack.com/feed'
}
 
# Default route
@app.route('/')
def index():
    # Get all articles and arrange by date + display with pages
    articles = [] # Stores articles
    for source, feed in RSS_FEEDS.items(): # Iterate over feeds
        parsed_feed = feedparser.parse(feed) # Load feed using feedparser
        # Individual articles 
        # Tuple -> Want to specify where each entry in the feed is from/what feed its
        # from
        entries = [(source, entry) for entry in parsed_feed.entries] 
        # Add the entries list to articles list
        articles.extend(entries)
    
    # Lambda function to sort by date published. x[1] used since tuple structure
    # specifies date as second entry per tuple
    # published_parsed = date 
    articles = sorted(articles, key = lambda x: x[1].published_parsed, reverse = True)
    
    # Split into pages -> 10 articles per page, next and prev button
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_articles = len(articles)
    # How many artciesl per page, what's the start point?
    start = (page-1) * per_page
    end = start + per_page
    paginated_articles = articles[start: end]
    
    return render_template('index.html', articles=paginated_articles, page=page,
                           total_pages = total_articles//per_page + 1)
    
@app.route('/search')
def search():
    query = request.args.get('q')
    articles = []
    for source, feed in RSS_FEEDS.items(): 
        parsed_feed = feedparser.parse(feed) 
        entries = [(source, entry) for entry in parsed_feed.entries] 
        articles.extend(entries)
        
    results = [article for article in articles if query.lower() in article[1].title.lower()]
    return render_template('search_results.html', articles = results, query=query)

if __name__=='__main__':
    app.run(debug=True)
    
    
    
    
    
    