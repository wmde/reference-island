DUMP_PATH?='/mnt/data/xmldatadumps/public/wikidatawiki/entities/latest-all.json.gz'

data/usable_ext_idefs.jsonl: \
	data/external_idefs.json \
	data/whitelisted_ext_idefs.json
	python3 scripts/extract_from_dump.py ${DUMP_PATH}

data/extracted_stats: \
	data/external_idefs.json \
	data/whitelisted_ext_idefs.json
	python3 scripts/extract_stats.py ${DUMP_PATH}

data/external_idefs.json:
	python3 scripts/generate_list_of_all_ext_idefs.py

data/whitelisted_ext_idefs.json: \
	data/external_idefs.json
	python3 scripts/examine_ext_idefs.py

data/ext_idef_check_result_limit10.json: \
	data/whitelisted_ext_idefs.json
	python3 scripts/sample_scrape.py

data/schema_equiv_props.json:
	python3 scripts/generate_list_of_schema_equivalent_properties.py

data/rdfa_stats.json: \
	data/ext_idef_check_result_limit10.json \
	data/schema_equiv_props.json
	python3 scripts/get_rdfa.py

.PHONY: clean
clean:
	rm data/*.json
	rm data/*.jsonl
