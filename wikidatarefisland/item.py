class Item(object):
    def __init__(self, id_, serialization):
        self.id_ = id_
        self.serialization = serialization
        self.claims = {}
        self.fully_cached = False

    def getPropertyClaims(self, pid):
        if self.claims.get(pid):
            return self.claims[pid]
        claims = []
        for claim in self.serialization['claims'].get(pid, []):
            claims.append(Claim(claim['id'], claim))
        self.claims[pid] = claims
        return claims

    def hasPropertyItemValue(self, pid, qids):
        # Returns true if it has any of the given Q-ids
        for claim in self.getPropertyClaims(pid):
            if claim.getItemValue() in qids:
                return True
        return False

    def getProperties(self):
        return set(self.serialization['claims'].keys())

    def getClaims(self):
        if not self.fully_cached:
            for pid in self.getProperties():
                self.getPropertyClaims(pid)
            self.fully_cached = True

        return self.claims


class Claim(object):
    def __init__(self, uuid, serialization):
        self.uuid = uuid
        self.serialization = serialization

    def getValue(self):
        try:
            return self.serialization['mainsnak']['datavalue']['value']
        except:
            return None

    def getItemValue(self):
        if not self.getValue():
            return None
        return self.getValue().get('id')

    def getReferences(self):
        references = []
        for reference in self.serialization.get('references', []):
            references.append(reference['snaks'])
        return references

    def hasValidReference(self):
        if not self.getReferences():
            return False
        isAllRefsBS = True
        for ref in self.getReferences():
            if 'P143' in ref or 'P4656' in ref:
                continue
            isAllRefsBS = False
        return not isAllRefsBS
