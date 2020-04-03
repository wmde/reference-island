import json
from functools import reduce

def property_filter(key):
    return "schema.org" in key

def type_filter(type_url):
    return "schema.org" in type_url

def schemaorg_reducer(accumulator, rdfa_property):
    if "@type" not in rdfa_property or not any("schema.org" in type_url for type_url in rdfa_property["@type"]):
        return accumulator
    
    return accumulator + [{
        "types": list(filter(type_filter, rdfa_property["@type"])),
        "properties": list(filter(property_filter, list(rdfa_property.keys())))
    }]

def schemaorg_filter(rdfa_property):
    return "@type" in rdfa_property and any("schema.org" in typeUrl for typeUrl in rdfa_property["@type"])

def rdfa_extractor(url, prop, site_data):
    filtered_types = list(filter(schemaorg_filter, site_data["rdfa"]))
    
    return {
        "propertyId": prop,
        "url": url,
        "schemaorg": reduce(schemaorg_reducer, site_data["rdfa"], [])
    }

def rdfa_filter(site_data):
    return len(site_data["schemaorg"]) > 0

def rdfa_reducer(accumulator, prop, site_data):
    if type(site_data) is not dict:
        return accumulator
    
    mapped_site_data = list(map(lambda url: rdfa_extractor(url, prop, site_data[url]), list(site_data.keys())))
    filtered_site_data = list(filter(rdfa_filter, mapped_site_data))

    if not filtered_site_data:
        return accumulator

    return accumulator + [ filtered_site_data ]


with open('data/ext_idef_check_result_limit10.json') as f:
    data = json.load(f)
    rdfa_list = reduce(lambda acc, key: rdfa_reducer(acc, key, data[key]), data, [])

    # print(json.dumps(rdfa_list, sort_keys=True, indent=2))

    with open('data/schema_equiv_props.json') as p:
        props_list = list(map(lambda propmap: propmap["url"] ,json.load(p)))

        total_mapped = 0
        total_items = 0
        total_types = 0
        total_props = 0
        total_resources = 0

        unmapped_props = {}
        unmapped_types = {}

        for externalid_list in rdfa_list:
            total_resources += len(externalid_list)
            for site_data in externalid_list:
                total_items += len(site_data["schemaorg"])

                for schemaorg_item in site_data["schemaorg"]:
                    total_types += len(schemaorg_item["types"])
                    total_props += len(schemaorg_item["properties"])

                    for item_type in schemaorg_item["types"]:
                        if item_type in props_list:
                            total_mapped += 1
                        elif item_type not in unmapped_types:
                            unmapped_types = {
                                **unmapped_types,
                                item_type: 1
                            }
                        else:
                            unmapped_types[item_type] += 1
                    
                    for item_prop in schemaorg_item["properties"]:
                        if item_prop in props_list:
                            total_mapped += 1
                        elif item_prop not in unmapped_props:
                            unmapped_props = {
                                **unmapped_props, 
                                item_prop: 1 
                            }
                        else:
                            unmapped_props[item_prop] += 1
        
        avg_item_per_resource = 0
        avg_prop_per_item = 0

        with open('data/rdfa_stats.json', 'w') as r:
            r.write(json.dumps({
                "total_mapped": total_mapped,
                "total_resources": total_resources,
                "total_items": total_items,
                "total_types": total_types,
                "total_props": total_props,
                "avg_items_per_resource": total_items / total_resources,
                "avg_props_per_item": total_props / total_items,
                "unmapped_types": unmapped_types,
                "unmapped_props": unmapped_props
            }, indent=2))