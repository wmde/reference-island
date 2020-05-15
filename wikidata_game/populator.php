<?php
$dbhost = "tools.db.svc.eqiad.wmflabs";
$dbname = "s54377__wd_ref_island_p";

function getDb($dbhost, $dbname) {
    $dbmycnf = parse_ini_file("../replica.my.cnf");
    $dbuser = $dbmycnf['user'];
    $dbpass = $dbmycnf['password'];
    return new PDO('mysql:host=' . $dbhost . ';dbname=' . $dbname . ';charset=utf8', $dbuser, $dbpass);
}

function backupTable($dbhost, $dbname) {
    // Strangely writing a backup code in php is extremely complicated
    // See https://stackoverflow.com/q/18279066/2596051
    $backup_file = 'db-backup-ref-' . time() . '.sql';
    // https://wikitech.wikimedia.org/wiki/Help:Toolforge/Database#ToolsDB_Backups_and_Replication
    exec("mysqldump --defaults-file=~/replica.my.cnf --host=$dbhost $dbname --result-file=$backup_file");
}

$db = getDb($dbhost, $dbname);
$file_path = getenv('REFS_PATH');
$data = explode( "\n", file_get_contents($file_path) );
backupTable($dbhost, $dbname);
$db->query("TRUNCATE TABLE refs;")->execute();
$sql = "INSERT INTO refs (ref_data) VALUES (?)";
$db->beginTransaction();
foreach ($data as $row) {
    $stmt = $db->prepare($sql);
    // PHP PDO doesn't have an easy way to batch multiple rows in insert
    // TODO: This is okay for 300 cases but for more cases,
    //   we need to write a query builder for the inserts
    $stmt->execute([$row]);
}
$db->commit();