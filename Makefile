data/whitelisted_ext_idefs.json: 
	python3 wikidatarefisland/run.py --step ss1 --output "whitelisted_ext_idefs.json"
data/scraped_data.json:
	python3 wikidatarefisland/run.py --step scrape --input "pipe1.jsonl" --output "scraped_data.jsonl"
