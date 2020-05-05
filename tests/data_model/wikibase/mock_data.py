mock = {
    "statement": {
        "with_quantity": {
            "datatype": 'quantity',
            "value": {
                "amount": "12"
            }
        },
        "with_string": {
            "datatype": 'string',
            "value": "Test"
        },
        "with_url": {
            "datatype": 'url',
            "value": "Test"
        },
        "with_monolingualtext": {
            "datatype": 'monolingualtext',
            "value": {
                "text": "Test"
            }
        },
        "with_datetime": {
            "day_precision": {
                "datatype": 'time',
                "value": {
                    "time": '+1986-05-04T00:00:00Z',
                    "precision": '11'
                }
            },
            "month_precision": {
                "datatype": 'time',
                "value": {
                    "time": '+1986-05-04T00:00:00Z',
                    "precision": '10'
                }
            },
            "year_precision": {
                "datatype": 'time',
                "value": {
                    "time": '+1986-05-04T00:00:00Z',
                    "precision": '9'
                }
            }
        },
        "with_globe-coordinate": {
            "on_earth": {
                "datatype": 'globe-coordinate',
                "value": {
                    "latitude": 52.498469,
                    "longitude": 13.381021,
                    "globe": "http://www.wikidata.org/entity/Q2"
                }
            },
            "on_mars": {
                "datatype": 'globe-coordinate',
                "value": {
                    "latitude": 18.65,
                    "longitude": 226.2,
                    "globe": "http://www.wikidata.org/entity/Q111"
                }
            }
        },
        "without_type": {
            "datatype": 'some-other-data'
        }
    },
    "reference": {
        "with_one_quantity_match": {
            "extractedData": ["12"]
        },
        "with_one_string_match": {
            "extractedData": ["Test"]
        },
        "with_one_geo_match": {
            "extractedData": [{
                "latitude": "52.498469",
                "longitude": "13.381021",
            }]
        },
        "with_one_day_match": {
            "extractedData": ["1986-05-04"]
        },
        "with_one_year_match": {
            "extractedData": ["1986"]
        },
        "with_multiple_values_match": {
            "extractedData": ["12", "Test", "1986-05-04", {
                "latitude": "52.498469",
                "longitude": "13.381021",
            }]
        },
        "without_match": {
            "extractedData": ["Some", "Other", "Values"]
        }
    }
}
