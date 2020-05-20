<?php
function detectRequestBody() {
    // Reads raw request data. See: https://stackoverflow.com/questions/8945879/how-to-get-body-of-a-post-in-php
    $rawInput = fopen('php://input', 'r');
    $tempStream = fopen('php://temp', 'r+');
    stream_copy_to_stream($rawInput, $tempStream);
    rewind($tempStream);

    return $tempStream;
}

function verifySignature($token, $payload){
    if(!isset($_SERVER['HTTP_X_HUB_SIGNATURE'])) {
        return false;
    }

    $signature = 'sha1=' . hash_hmac('sha1', $payload, $token);
    return hash_equals($signature, $_SERVER['HTTP_X_HUB_SIGNATURE']);
}
?>