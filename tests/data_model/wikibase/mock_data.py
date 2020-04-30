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
        "with_multiple_values_match": {
            "extractedData": ["12", "Test"]
        },
        "without_match": {
            "extractedData": ["Some", "Other", "Values"]
        }
    }
}
