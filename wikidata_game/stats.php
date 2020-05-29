<?php declare(strict_types=1);

require_once('includes/constants.php');
require_once('includes/responses.php');
require_once('includes/setup-db.php');

if(isset($_GET['dump']) && $_GET['dump'] === 'rejected'){
    $rejected = $getMatches(FLAGS['REJECTED']);
    csvDumpResponse('rejected-matches', $rejected);
    exit();
}

$total_matches = $countMatches();
$accepted_matches = $countMatches(FLAGS['ACCEPTED']);
$rejected_matches = $countMatches(FLAGS['REJECTED']);

$total_reviewed = ($rejected_matches +  $accepted_matches);
$acceptance_rate = ($accepted_matches * 100) / $total_reviewed;

include_once('views/stats-page.php');
?>