<?php declare(strict_types=1);

require_once('util/database.php');
require_once('util/config.php');

require_once('constants.php');

// Setup connection
$db_config = getConfig(REPLICA_CNF_PATH, ENV_CNF_PATH);
$db = getDb($db_config);

// Create query abstractions
$countMatches = createMatchesCounter($db);
$getMatches = createMatchesReader($db);