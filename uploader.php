<?php
$target_dir = ".";
if (isset($_POST['dir'])) {
    $target_dir = $_POST['dir'];
    if (!file_exists($target_dir)) {
        mkdir($target_dir, 0755, true);
    }
}

$target_file = $target_dir . "/" . basename($_FILES["file"]["name"]);

if (move_uploaded_file($_FILES["file"]["tmp_name"], $target_file)) {
    echo "Success: " . $target_file;
} else {
    echo "Error uploading to " . $target_file;
}
?>