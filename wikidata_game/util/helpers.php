<?php declare(strict_types=1);

/**
 * Check an array against a list of minimum required key names
 *
 * @param array $keys Key names to check against
 * @param array $arr Array to check
 * @return boolean True if all keys exists, False if any key doesn't exists
 */
function array_has_keys(array $keys, array $arr): bool {
    foreach($keys as $key){
        if(!array_key_exists($key, $arr)){
            return FALSE;
        }
    }

   return TRUE; 
}