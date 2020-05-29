<?php declare(strict_types=1);

require_once('util/config.php');

/**
 * Potential Match Flags from the Game Database
 */
const FLAGS = [
    'PENDING' => 0,
    'ACCEPTED' => 1,
    'REJECTED' => 2
];

/**
 * Base directory for configuration files (*.my.cnf)
 */
define( 'CONFIG_DIR', getConfigDirectory());

/**
 * Various useful configuration files
 */
define( 'REPLICA_CNF_PATH', CONFIG_DIR . '/replica.my.cnf');
define( 'ENV_CNF_PATH', CONFIG_DIR . '/env.my.cnf');