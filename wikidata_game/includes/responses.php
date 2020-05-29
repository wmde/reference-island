<?php declare(strict_types=1);

/**
 * Responds with a csv dump of passed in matches
 *
 * @param string $filename The filename to generate
 * @param iterable $matches An iterable containing the matches to dump
 * @return void
 */
function csvDumpResponse(string $filename, iterable $matches): void {
    header('Content-Type: text/csv; charset=utf-8');
    header('Content-Disposition: attachment; filename=' . $filename .'.csv');

    // create a file pointer connected to the output stream
    $output = fopen('php://output', 'w');

    // output the column headings
    fputcsv($output, ['Item', 'Property', 'Value (JSON)', 'Source URL', 'Extracted Data (JSON)']);

    foreach ($matches as $match){
        $data = json_decode($match['ref_data'], TRUE);
        $statement = $data['statement'];
        $value = json_encode($statement['value']);
        $reference = $data['reference'];
        $extracted = json_encode($reference['extractedData']);
        $url = $reference['referenceMetadata']['P854'];

        fputcsv($output, [$data['itemId'], $statement['pid'], $value, $url, $extracted]);
    }
}