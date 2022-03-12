import urllib.request,json
from .models import Quote

def get_quotes():
    get_quotes_url = "http://quotes.stormconsultancy.co.uk/random.json"
    get_quotes_data= urllib.request.urlopen(get_quotes_url)
    get_quotes_response = json.loads(get_quotes_data.read())
       
    author = get_quotes_response.get("author")
    quote = get_quotes_response.get("quote")
        
    new_quote = Quote(author,quote)
    return new_quote