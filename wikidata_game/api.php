<?PHP
function getDb() {
	$dbmycnf = parse_ini_file("../replica.my.cnf");
	$dbuser = $dbmycnf['user'];
	$dbpass = $dbmycnf['password'];
	$dbhost = "tools.db.svc.eqiad.wmflabs";
	$dbname = "s52709__kian_p";
	return new PDO('mysql:host=' . $dbhost . ';dbname='.$dbname . ';charset=utf8', $dbuser, $dbpass);
}
function getDesc() {
	$title = "Reference hunt!" ;
	return [
		"label" => [ "en" => $title ] ,
		"description" => [ "en" => "[https://www.wikidata.org/wiki/Wikidata:Automated_finding_references_input Reference hunt] suggestions to add references in items based on structued data in the web. Source code can be found in [https://github.com/wmde/reference-island here]"],
		"icon" => 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/ArtificialFictionBrain.png/120px-ArtificialFictionBrain.png' ,
	];
}

function getGuid( $statement ) {
	return 'Q76$D4FDE516-F20C-4154-ADCE-7C5B609DFDFF';
}
function getReferenceSnak( $reference ) {
	return ["P212" => [ ["snaktype"=>"value","property" => "P212","datavalue"=>["type"=>"string","value"=>"foo"]]]];
}
function getTextForUsers( $data ) {
	return 'Very useful text';
}

function getTiles() {
	$db = getDb();
	$num = $_REQUEST['num'];
	$sql = "SELECT * FROM references WHERE ref_flag = 0 ORDER by RAND() DESC LIMIT " . $num;
	$result = $db->query( $sql );
	$result = $result->fetchAll();
	$output = [];
	foreach ( $result as $row ) {
		$data = json_decode( $row['ref_data'], true );
		$refApi = [
			'action' => 'wbsetreference',
			'statement' => getGuid( $data['statement'] ),
			'snaks' => getReferenceSnak( $data['reference'] ),
		];
		$tile = [
			'id' => (int)$row['ref_id'],
			'sections' => [],
			'controls' => []
		];
		$tile['sections'][] = ['type' => 'item' , 'q' => $data['itemId']] ;
		$tile['sections'][] = [
			'type' => 'text' ,
			'title' => 'Possible reference' ,
			'text' => getTextForUsers( $data ),
			'url'=> $data['reference']['referenceMetadata']['referenceUrl']
		];
		$tile['controls'][] = [
			'type' => 'buttons' ,
			'entries' => [
				[ 'type' => 'green' , 'decision' => 'accept' , 'label' => 'Accept' , 'api_action' => $refApi ],
				[ 'type' => 'white' , 'decision' => 'skip' , 'label' => 'Skip' ],
				[ 'type' => 'blue' , 'decision' => 'reject' , 'label' => 'Reject' ]
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
	$sql = '' ;
	if ( $decision == 'accept' ) {
		$sql = "UPDATE references SET ref_flag=1 WHERE ref_id=$ref_id" ;
	} else if ( $decision == 'reject' ) {
		$sql = "UPDATE references SET ref_flag=2 WHERE ref_id=$ref_id" ;
	}

	if ( $sql != '' ) {
		$result = $db->exec($sql);
		if ( !$result ) {
			return [ 'error' => 'There was an error running the query [' . $db->error . ']' ];
		}
	}
	return [];
}

function dispatchRequest( $action ) {
	if ( $action === 'desc' ) {
		return getDesc();
	}

	if ( $action === 'tiles' ) {
		return getTiles();
	}

	if ( $action === 'log_action' ) {
		return recordLog();
	}

	return [ 'error' => "No valid action!" ];
}


$callback = $_REQUEST['callback'];
$output = dispatchRequest( $_REQUEST['action'] );
if ( $callback ) {
	header('Content-type: application/json');
	print $callback . '(' ;
	print json_encode( $output );
	print ")\n" ;
} else {
	header('Content-type: text/javascript');
	print json_encode( $output );
}
?>
