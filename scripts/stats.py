import os

from wikidatarefisland.storage import Storage

storage = Storage.newFromScript(os.path.realpath(__file__))


def main():
    data = storage.get('ext_idef_check_result.json')
    print('Total: ', len(data))
    goods = []
    schemas = []
    for i in data:
        if data[i][1] > 5:
            goods.append(i)
        if data[i][2] > 5:
            schemas.append(i)
    print('Good: ', len(goods))
    print('Schemas: ', len(schemas))

    storage.store('whitelisted_ext_idefs.json', schemas)


if __name__ == '__main__':
    main()
