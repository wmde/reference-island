<?PHP
// This is a POC, don't judge
function getDb() {
    $dbmycnf = parse_ini_file("../replica.my.cnf");
    $dbuser = $dbmycnf['user'];
    $dbpass = $dbmycnf['password'];
    $dbhost = "tools.db.svc.eqiad.wmflabs";
    $dbname = "s54377__wd_ref_island_p";
    return new PDO('mysql:host=' . $dbhost . ';dbname=' . $dbname . ';charset=utf8', $dbuser, $dbpass);
}

function getDesc() {
    $title = "Reference hunt!";
    return [
        "label" => ["en" => $title],
        "description" => ["en" => "[https://www.wikidata.org/wiki/Wikidata:Automated_finding_references_input Reference hunt] suggestions to add references in items based on structued data in the web. Source code can be found in [https://github.com/wmde/reference-island here]"],
        "icon" => 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Treasure_map.png/120px-Treasure_map.png',
    ];
}

function loadApi($params) {
    $params['format'] = 'json';
    $baseUrl = 'https://www.wikidata.org/w/api.php';
    $result = file_get_contents($baseUrl . '?' . http_build_query($params));
    return json_decode($result, true);
}

function getGuid($statement, $itemId) {
    $data = loadApi([
        'action' => 'wbgetclaims',
        'entity' => $itemId,
        'property' => $statement['pid']
    ]);
    foreach ($data['claims'][$statement['pid']] as $claim) {
        if (
            isset($claim['mainsnak']['datavalue']['value']) &&
            $claim['mainsnak']['datavalue']['value'] == $statement['value']
        ) {
            return $claim['id'];
        }
    }
    return false;
}

function getReferenceSnak($reference) {
    $result = [];
    foreach ($reference as $pid => $value) {
        if ($pid == 'P813') {
            // Time data type
            $dataValue = [
                "value" => [
                    "time" => '+0000000' . explode(' ', $value)[0] . 'T00:00:00Z',
                    "timezone" => 0,
                    "before" => 0,
                    "after" => 0,
                    "precision" => 11,
                    "calendarmodel" => "http://www.wikidata.org/entity/Q1985727"
                ],
                "type" => "time"
            ];
        } elseif ($pid == 'P248') {
            // Item data type
            $dataValue = [
                "value" => [
                    "entity-type" => "item",
                    "numeric-id" => (int)ltrim($value, 'Q'),
                    "id" => $reference[$pid]
                ],
                "type" => "wikibase-entityid"
            ];
        } else {
            // String data type
            $dataValue = ["type" => "string", "value" => $value];
        }

        $result[$pid] = [[
            'snaktype' => 'value',
            'property' => $pid,
            'datavalue' => $dataValue
        ]];
    }
    return $result;
}

function getTextForUsers($data) {
    return "Is the value for this claim and the value given in the reference the same?\nProperty: " . $data["statement"]["pid"] .
        "\nValue of the statement: " . json_encode($data["statement"]["value"]) .
        "\nURL reference: " . $data["reference"]["referenceMetadata"]["P854"] .
        "\nValue given in the reference: " . json_encode($data["reference"]["extractedData"]);
}

function getTiles() {
    $db = getDb();
    $num = $_REQUEST['num'];
    $sql = "SELECT * FROM refs WHERE ref_flag = 0 ORDER by RAND() DESC LIMIT " . $num;
    $result = $db->query($sql);
    $result = $result->fetchAll();
    $output = [];
    foreach ($result as $row) {
        $data = json_decode($row['ref_data'], true);
        $guid = getGuid($data['statement'], $data['itemId']);
        if (!$guid) {
            continue;
        }
        $refApi = [
            'action' => 'wbsetreference',
            'statement' => $guid,
            'snaks' => getReferenceSnak($data['reference']['referenceMetadata']),
        ];
        $tile = [
            'id' => (int)$row['ref_id'],
            'sections' => [],
            'controls' => []
        ];
        $tile['sections'][] = ['type' => 'item', 'q' => $data['itemId']];
        $tile['sections'][] = [
            'type' => 'text',
            'title' => 'Possible reference',
            'text' => getTextForUsers($data),
            'url' => $data['reference']['referenceMetadata']['referenceUrl']
        ];
        $tile['controls'][] = [
            'type' => 'buttons',
            'entries' => [
                ['type' => 'green', 'decision' => 'accept', 'label' => 'Accept', 'api_action' => $refApi],
                ['type' => 'white', 'decision' => 'skip', 'label' => 'Skip'],
                ['type' => 'blue', 'decision' => 'reject', 'label' => 'Reject']
            ]
        ];

        $output[] = $tile;
    }

    return $output;
}

function recordLog() {
    $db = getDb();
    $ref_id = (int)$_REQUEST['tile'];
    $decision = $_REQUEST['decision'];
    $sql = '';
    if ($decision == 'accept') {
        $sql = "UPDATE refs SET ref_flag=1 WHERE ref_id=$ref_id";
    } else if ($decision == 'reject') {
        $sql = "UPDATE refs SET ref_flag=2 WHERE ref_id=$ref_id";
    }

    if ($sql != '') {
        $result = $db->exec($sql);
        if (!$result) {
            return ['error' => 'There was an error running the query [' . $db->error . ']'];
        }
    }
    return [];
}

function dispatchRequest($action) {
    if ($action === 'desc') {
        return getDesc();
    }

    if ($action === 'tiles') {
        return getTiles();
    }

    if ($action === 'log_action') {
        return recordLog();
    }

    return ['error' => "No valid action!"];
}


$output = dispatchRequest($_REQUEST['action']);
if (isset($_REQUEST['callback'])) {
    header('Content-type: text/javascript');
    print $_REQUEST['callback'] . '(';
    print json_encode($output);
    print ")\n";
} else {
    header('Content-type: application/json');
    print json_encode($output);
}
?>
