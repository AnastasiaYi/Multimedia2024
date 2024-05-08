<?php
$uploadStatus = [];

// Check if files have been uploaded
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $totalFiles = count($_FILES['filesToUpload']['name']);

    for ($i = 0; $i < $totalFiles; $i++) {
        $targetDir = "uploads/";
        $targetFile = $targetDir . basename($_FILES["filesToUpload"]["name"][$i]);
        $uploadOk = 1;

        // Check if file already exists
        if (file_exists($targetFile)) {
            $uploadStatus[$i] = "Sorry, file already exists.";
            $uploadOk = 0;
        }

        // Check file size (e.g., 5MB limit)
        if ($_FILES["filesToUpload"]["size"][$i] > 5000000) {
            $uploadStatus[$i] = "Sorry, your file is too large.";
            $uploadOk = 0;
        }

        // Allow certain file formats
        $imageFileType = strtolower(pathinfo($targetFile, PATHINFO_EXTENSION));
        if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg") {
            $uploadStatus[$i] = "Sorry, only JPG, JPEG, PNG files are allowed.";
            $uploadOk = 0;
        }

        // Check if $uploadOk is set to 0 by an error
        if ($uploadOk == 0) {
            $uploadStatus[$i] = "Sorry, your file was not uploaded.";
        // if everything is ok, try to upload file
        } else {
            if (move_uploaded_file($_FILES["filesToUpload"]["tmp_name"][$i], $targetFile)) {
                $uploadStatus[$i] = "The file ". htmlspecialchars(basename($_FILES["filesToUpload"]["name"][$i])). " has been uploaded.";
            } else {
                $uploadStatus[$i] = "Sorry, there was an error uploading your file.";
            }
        }
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Upload Multiple Images</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .upload-container {
            background: white;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0,0,0,0.2);
            border-radius: 8px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="upload-container">
        <h1>Upload Images</h1>
        <form id="uploadForm" action="upload.php" method="post" enctype="multipart/form-data">
            <input type="file" name="filesToUpload[]" id="filesToUpload" multiple>
            <button type="submit" name="submit">Upload Files</button>
            <script>
                var btn = document.getElementById('submit');
                btn.addEventListener('click', function() {
                document.location.href = 'loading.php';
                });
            </script>
        </form>
        
        <?php
        foreach ($uploadStatus as $status) {
            echo '<p>' . $status . '</p>';
        }
        ?>
    </div>
</body>
</html>
