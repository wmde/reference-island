<?php 
    $branch = $_GET['branch'];
    $root = $_SERVER['DOCUMENT_ROOT'];
    $file_path = $branch . '-api.php';

    if(!file_exists($root . 'stage/' . $file_path)){
        header("HTTP/1.0 404 Not Found");
        echo '404 Not Found';
        exit;
    }

    $api_url = 'https://tools.wmflabs.org/wd-ref-island/stage/' . $file_path;

    header('Location: https://tools.wmflabs.org/wikidata-game/distributed/#mode=test_game&url=' . $api_url);

?>