data/whitelisted_ext_idefs.json: 
	python3 wikidatarefisland/run.py --step ss1 --output "whitelisted_ext_idefs.json"

data/scraped_data.jsonl:
	python3 wikidatarefisland/run.py --step scrape --input "pipe1.jsonl" --output "scraped_data.jsonl"

data/matched_references.jsonl: \
	data/scraped_data.jsonl
	python3 wikidatarefisland/run.py --step match --input "scraped_data.jsonl" --output "matched_references.jsonl"
