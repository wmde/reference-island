<?php

    
    if(!isset($_SERVER['HTTP_X_GITHUB_EVENT'])){
        exit;
    }

    if($_SERVER['HTTP_X_GITHUB_EVENT'] != 'pull_request'){
        exit;
    }

    require_once('secure-hooks.php');

    $payload = stream_get_contents(detectRequestBody());
    $tokens = parse_ini_file('../tokens.my.cnf');

    if(!verifySignature($tokens['publish'], $payload)){
        exit;
    }

    $logfile_path = '../logs/deployment.log';
    $datetime_string = date('c');

    $payload = json_decode($_POST["payload"]);

    // Check if current branch is a game branch
    $is_game_branch = substr($payload->pull_request->head->ref, 0, 5) === 'game-';

    // If it is not a merge to master from game branch, exit
    if($payload->action != 'closed'
        || !$is_game_branch 
        || !$payload->pull_request->merged 
        || $payload->pull_request->base->ref != 'master'){
        exit;
    }

    $script_path = '../reference-island/wikidata_game/deploy.sh';

    $output = shell_exec($script_path);

    $message = 'Attempting to deploy ' . $payload->pull_request->head->sha . ' of ' . $payload->pull_request->head->ref . PHP_EOL;
    $message .= $output ? $output : 'An error occurred while trying to deploy. Please see ~/error.log for more information.';
    
    file_put_contents($logfile_path, $datetime_string . ' ' . $message . PHP_EOL, FILE_APPEND);
?>
