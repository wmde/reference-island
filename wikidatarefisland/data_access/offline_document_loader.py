class OfflineDocumentLoader:
    def __init__(self, schema_context):
        self.schema_context = schema_context

    def get_loader(self, url):
        if url != 'http://schema.org':
            return {
                'contextUrl': None,
                'documentUrl': url,
                'document': {}
            }
        return {
            'contextUrl': None,
            'documentUrl': url,
            'document': self.schema_context
        }
