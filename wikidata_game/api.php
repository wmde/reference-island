<?PHP
// This is a POC, don't judge
function getDb() {
    $server_root = $_SERVER['DOCUMENT_ROOT'];
    $dbmycnf = parse_ini_file($server_root . "/../replica.my.cnf");
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
        if ($pid == 'P854') {
            // We skip url for references given in the game: T251262#6096951
            continue;
        }
        if ($pid == 'dateRetrieved') {
            continue;
        }
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

function getFormattedValue($type, $value, $datatype) {
    $params = [
        'action' => 'wbformatvalue',
        'generate' => 'text/html',
        'datavalue' => '',
        'datatype' => $datatype
    ];

    $params['datavalue'] = json_encode([
        'type' => $type,
        'value' => $value
    ]);

    $data = loadApi($params);

    return $data['result'];
}

function getFormattedProperty($id) {
    $propertyValue = [
        'entity-type' => 'property',
        'id' => $id,
        'numeric-id' => (int)substr($id, 1)
    ];

    return getFormattedValue('wikibase-entityid', $propertyValue, 'wikibase-property');
}

function getFormattedItem($id) {
    $itemValue = [
        'entity-type' => 'item',
        'id' => $id,
        'numeric-id' => (int)substr($id, 1)
    ];

    return getFormattedValue('wikibase-entityid', $itemValue, 'wikibase-item');
}

function formatEntityValue($id, $value){
    // A hack to fix the URLS coming from wbformatvalue endpoint.
    $full_url_link = str_replace('href="/', 'target="_blank" href="http://wikidata.org/', $value); 
    return '<span class="lead">' . $full_url_link . ' <sub class="id" style="font-size: 0.65em">[' . $id . ']</sub></span>';
}

function formatStatementValue($statement) {
    $value = $statement["value"];
    $datatype = $statement["datatype"];

    switch ($datatype){
        case 'wikibase-item':
            $formattedData = getFormattedValue('wikibase-entityid', $value, $datatype);
            return formatEntityValue($value['id'], $formattedData);
        case 'globe-coordinate':
            return getFormattedValue('globecoordinate', $value, $datatype);
        case 'time':
        case 'monolingualtext':
        case 'quantity':
            return getFormattedValue($datatype, $value, $datatype);
        default:
            return $value;
    }
}

function formatClaimHTML($data) {
    $itemId = $data['itemId'];
    $statement = $data["statement"];
    
    $html = '<div class="statement">';
    $html .= '<p class="item">Item: ' . formatEntityValue($itemId, getFormattedItem($itemId)) . '</p>';
    $html .= '<p class="property-id">Property: ' . formatEntityValue($statement ['pid'], getFormattedProperty($statement['pid'])) . '</p>';
    $html .= '<p class="value">Value: ' . formatStatementValue($statement) . '</p>';
    $html .= '</div>';

    return $html;
}

function formatSourceURL($referenceMeta){
    $url = $referenceMeta["P854"];
    $retrieved = $referenceMeta["dateRetrieved"];
    return '<a class="lead" target="_blank" href="' . $url .'">' . $url . '</a> (Retrieved: ' . $retrieved . ')';  
}

function formatExtractedData($data) {
    return is_array($data) ? json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) : $data;
}

function formatSourceDataHTML($data) {
    $sourceData = $data["reference"];
    $extractedData = $sourceData['extractedData'];
    
    $html = '<div class="extracted-data">';
    $html .= '<p class="source-url">Source URL: '. formatSourceURL($sourceData["referenceMetadata"]) .'</p>';
    $html .= '<p>Extracted Data:</p>';
    
    foreach($extractedData as $datum){
        $html .= '<pre>' . formatExtractedData($datum) . '</pre>';
    }
    
    $html .= '</div>';

    return $html;
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
        $referenceMetadata = $data['reference']['referenceMetadata'];
        if (!array_key_exists( 'P813', $referenceMetadata)) {
            $referenceMetadata['P813'] = $referenceMetadata['dateRetrieved'];
        }
        $refApi = [
            'action' => 'wbsetreference',
            'statement' => $guid,
            'tags' => 'reference-game',
            'snaks' => json_encode(getReferenceSnak($referenceMetadata)),
        ];
        $tile = [
            'id' => (int)$row['ref_id'],
            'sections' => [],
            'controls' => []
        ];
        $tile['sections'][] = [
            'type' => 'html',
            'text' => '<p class="h3">Is this source a reliable reference material <strong>and</strong> does the extracted data support the Wikidata Statement?</p>'
        ];
        $tile['sections'][] = [
            'type' => 'html',
            'title' => 'Wikidata Statement',
            'text' => formatClaimHTML($data)
        ];
        $tile['sections'][] = [
            'type' => 'html',
            'title' => 'Source Data',
            'text' => formatSourceDataHTML($data)
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
