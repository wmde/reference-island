<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reference Treasure Hunt - Game Stats</title>
</head>
<body>
    <h1>Reference Treasure Hunt - Game Stats</h1>
    <h2>Total Matches</h2>
    <ul>
        <li>
            <strong>Number of Total Matches </strong>: <?php echo $total_matches ?>
        </li>
        <li>
            <strong>Total Matches Reviewed</strong>: <?php echo $total_reviewed ?>
        </li>
        <li>
            <strong>Total Accepted Matches</strong>: <?php echo $accepted_matches ?>
        </li>
        <li>
            <strong>Total Rejected Matches</strong>: <?php echo $rejected_matches ?>
        </li>
        <li>
            <strong>Acceptance Rate</strong>: <?php echo $acceptance_rate ?>%
        </li>
    </ul>
    <p><a href="?dump=rejected" download>Download Rejected Matches (CSV)</a></p>
</body>
</html>