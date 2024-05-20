import json
import os
import os.path

from random import randint

from fastapi import FastAPI, Query

description = """
Quotes API for when you need a little inspiration.
"""

app = FastAPI(title="QuotesAPI", description=description)

data_dir = os.environ.get('DATA_PATH', os.path.dirname(__file__) + '/../data')
quotes = json.load(open(data_dir + '/quotes.json'))
max_id = len(quotes)

@app.get("/quote/")
async def get_quote(quote_id: int = Query(-1, description="The ID of the quote you want to retrieve. Leave blank to get a random quote.")):
    if quote_id == -1:
        quote_id = randint(1, max_id+1)
    return quotes[quote_id-1]

