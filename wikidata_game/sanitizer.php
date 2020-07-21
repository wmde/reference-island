<?php
/**
 * Dumps a db backup, and removes potential references from ignored sources
 * This is throwaway code, meant to only run once as a resolution of bug T252781
 */

function getDb($dbhost, $dbname, $dbmycnf) {
    $dbuser = $dbmycnf['user'];
    $dbpass = $dbmycnf['password'];
    return new PDO('mysql:host=' . $dbhost . ';dbname=' . $dbname . ';charset=utf8', $dbuser, $dbpass);
}

function backupTable($dbhost, $dbname, $mycnf_path) {
    $root = dirname(__FILE__);
    $backup_file = 'db-backup-ref-' . date('c') . '.sql';
    exec("mysqldump --defaults-file=". $mycnf_path ." --host=$dbhost $dbname --result-file=$backup_file");
}

function getRefsToRemove($removelist){
    return function($row) use ($removelist){
        $data = json_decode($row["ref_data"], true);
        $reference_meta = $data["reference"]["referenceMetadata"];
        if($reference_meta == NULL){
            return TRUE;
        }

        foreach(array_keys($reference_meta) as $key){
            if(in_array($key, $removelist)){
                return TRUE;
            }
        }

        return FALSE;
    };
}

$dbhost = getenv('HOST');
$dbname = getenv('DB');

if(!$dbhost || ! $dbname){
    echo 'Could not find `HOST` or `DB` environment variables' . PHP_EOL;
    exit(1);
}

$root = dirname(__FILE__);
$mycnf_path = $root . '/../replica.my.cnf';
$dbmycnf = parse_ini_file($mycnf_path);

if(!$dbmycnf){
    echo 'Could not find database configuration file' . PHP_EOL;
    exit(1);
}

$removelist_path = $root . '/ignored-properties.json';
$removelist = json_decode(file_get_contents($removelist_path));

if(!$removelist){
    echo 'Could not find external id in ignored properties file' . PHP_EOL;
    exit(1);
}

backupTable($dbhost, $dbname, $mycnf_path);

$db = getDb($dbhost, $dbname, $dbmycnf);

$sql_select = "SELECT * FROM refs WHERE ref_flag = 0";
$rows = $db->query($sql_select)->fetchAll();

$bad_references = array_filter($rows, getRefsToRemove($removelist));
$delete_count = sizeof($bad_references);
$remaining_count = sizeof($rows) - $delete_count; 

$sql_delete = "DELETE FROM refs WHERE ref_id = ?";

echo 'Deleting: ' . $delete_count . PHP_EOL;

foreach($bad_references as $row){        
    $query = $db->prepare($sql_delete);
    $query->execute([$row['ref_id']]);
    echo '.';
}

echo PHP_EOL;

$sql_count = "SELECT COUNT(ref_flag) FROM refs WHERE ref_flag = 0";
$post_count = $db->query($sql_count)->fetchColumn();

if($post_count == $remaining_count){
    echo 'Successfully sanitized database.' . PHP_EOL;
} else {
    echo 'Row count mismatch: expected' . $remaining_count . ' but got ' . $post_count . 'please check sanitized database.' . PHP_EOL;
}



