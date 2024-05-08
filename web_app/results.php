<?php
session_start();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Upload Results</title>
</head>
<body>
    <h1>Upload Results</h1>
    <?php
    if (isset($_SESSION['uploadStatus'])) {
        foreach ($_SESSION['uploadStatus'] as $status) {
            echo '<p>' . $status . '</p>';
        }
    } else {
        echo '<p>No upload results to display.</p>';
    }
    ?>
</body>
</html>