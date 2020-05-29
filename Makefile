# Putting the top one first so "make" without argument picks up the last result
data/references.jsonl: \
	data/matched_references.jsonl \
	data/matched_item_references.jsonl
	cat $^ > $@

data/whitelisted_ext_idefs.json:
	python3 wikidatarefisland/run.py --step ss1 --output "whitelisted_ext_idefs.json"
data/extracted_unreferenced_statements.jsonl: \
	data/whitelisted_ext_idefs.json
	python3 wikidatarefisland/run.py --step extract_items --side-service-input "whitelisted_ext_idefs.json" --dump-path "${DUMP_PATH}" --output "extracted_unreferenced_statements.jsonl"
data/schema_org_context.jsonld:
	python3 wikidatarefisland/run.py --step fetch_schema_ctx --output "schema_org_context.jsonld"
data/scraped_data.jsonl: \
	data/extracted_unreferenced_statements.jsonl \
	data/schema_org_context.jsonld
	python3 wikidatarefisland/run.py --step scrape  --side-service-input "schema_org_context.jsonld" --input "extracted_unreferenced_statements.jsonl" --output "scraped_data.jsonl"
data/matched_references.jsonl: \
	data/scraped_data.jsonl
	python3 wikidatarefisland/run.py --step match --input "scraped_data.jsonl" --output "matched_references.jsonl"
data/matched_item_references.jsonl: \
	data/scraped_data.jsonl
	python3 wikidatarefisland/run.py --step item_analysis --input "scraped_data.jsonl" --side-service-input "whitelisted_ext_idefs.json" --output "matched_item_references.jsonl"

