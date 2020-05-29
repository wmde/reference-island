<?php declare(strict_types=1);

require_once('helpers.php');

/**
 * Initiates and returns a database connection
 *
 * @param array $db_cnf List of required configuration to create the connection
 * @return PDO The PDO database connection
 * 
 * @throws InvalidArgumentException when an invalid database configuration is passed
 */
// TODO: Unit Tests needed (Mocking Database connection)
function getDb(array $db_cnf): PDO {
    $required_keys = ['user', 'password', 'dbhost', 'dbname'];
    
    if(!array_has_keys($required_keys, $db_cnf)){
        throw new InvalidArgumentException('Database configuration is missing one of the following required keys: ' 
                                            . implode($required_keys, ', '));
    }
    
    $dbhost = $db_cnf['dbhost'];
    $dbname = $db_cnf['dbname'];
    $dbuser = $db_cnf['user'];
    $dbpass = $db_cnf['password'];

    return new PDO('mysql:host=' . $dbhost . ';dbname=' . $dbname . ';charset=utf8', $dbuser, $dbpass);
}

/**
 * Creates a closure to retrieve reference matches from a specified database connection
 *
 * @param PDO $db
 * @return Closure function to query and retrieve matches
 */
// TODO: Unit Tests needed (Mocking Database connection)
function createMatchesReader(PDO $db): Closure {
    /**
     * Queries and retrieves a list of potential matches from the game database
     *
     * @param integer $flag Match flag filter: 0 - Pending matches, 1 - Accepted matches, 2 - Rejected matches
     *                                         Default: (-1) - All matches
     * @return array A list of matches
     */
    return function(int $flag = -1) use ($db): iterable {
        $sql = $flag !== -1 ? "SELECT * FROM refs WHERE ref_flag = :flag" : "SELECT * FROM refs";
        $query = $db->prepare($sql);
        
        $query->execute(['flag' => $flag]);
        
        while($row = $query->fetch(PDO::FETCH_ASSOC)){
            yield $row;
        }
    };
}

/**
 * Creates a closure to count reference matches from a specified database connection
 *
 * @param PDO $db
 * @return Closure
 */
// TODO: Unit Tests needed (Mocking Database connection)
function createMatchesCounter(PDO $db): Closure {
    
    /**
     * Counts matches in the game database
     *
     * @param integer $flag Match flag filter: 0 - Pending matches, 1 - Accepted matches, 2 - Rejected matches
     *                                         Default: (-1) - All matches
     * @return integer A list of matches
     */
    return function(int $flag = -1) use ($db): int {
        $sql = $flag === -1 ? "SELECT COUNT(ref_flag) FROM refs" : "SELECT COUNT(ref_flag) FROM refs WHERE ref_flag = :flag";
        $query = $db->prepare($sql);
        
        $query->execute(['flag' => $flag]);
        return (int)$query->fetchColumn();
    };
}