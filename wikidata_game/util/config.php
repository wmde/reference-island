<?php declare(strict_types=1);

/**
 * Retrieves a base path a string for the config directory
 *
 * @return string Path to config path
 */
// TODO: Unit Tests needed (Mocking Env Vars)
function getConfigDirectory(): string {
    // From environment variable
    if(getenv('CONFIG_PATH')){
        return getenv('CONFIG_PATH');
    }

    // Home path from process (CLI only)
    if(isset($_SERVER['HOME'])){
        return $_SERVER['HOME'];
    }

    // Parent directory of server's document root
    if(isset($_SERVER['DOCUMENT_ROOT'])){
        return dirname($_SERVER['DOCUMENT_ROOT']);
    }

    // Default: parent directory of current file
    return dirname(__FILE__);
}

/**
 * Reads configuration files and return a composed list of all configurations
 *
 * @param string ...$paths variable amount of paths to read configurations from
 * @return array An array of collected configurations from paths
 * 
 * @throws InvalidArgumentException when a file doesn't exists in provided path
 */
// TODO: Unit Tests needed (Mocking FileSystem)
function getConfig(string ...$paths): array {
    return array_reduce($paths, function($config, $path){
        $resolved_path = realpath($path); 
        
        if(!$resolved_path) {
            throw new InvalidArgumentException('Cannot read configuration in path: ' . $path);
        }

        $current_config = parse_ini_file($resolved_path);

        return array_merge($config, $current_config);
    }, []);
}