<?php 
function download($url, $path) {
    $dir = dirname($path);
    if (!is_dir($dir)) {
        mkdir($dir, 0755, true);
    }
    $ch = curl_init($url);
    $fp = fopen($path, 'wb');
    curl_setopt($ch, CURLOPT_FILE, $fp);
    curl_setopt($ch, CURLOPT_HEADER, 0);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_exec($ch);
    curl_close($ch);
    fclose($fp);
}

// Download assets from GitHub
$baseUrl = 'https://raw.githubusercontent.com/nagavisionltd/founders-launchpad-app/main/';
download($baseUrl . 'index.html', 'index.html');
download($baseUrl . 'assets/pitch_deck/slide1_high_res.png', 'assets/pitch_deck/slide1_high_res.png');
download($baseUrl . 'assets/logos/logo_brand_guidelines.jpg', 'assets/logos/logo_brand_guidelines.jpg');
download($baseUrl . 'assets/websites/site_hero_high_res.jpg', 'assets/websites/site_hero_high_res.jpg');

echo 'Update Complete';
?>