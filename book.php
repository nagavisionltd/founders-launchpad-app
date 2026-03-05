<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Configuration
$team_email = "hello@ellipsiscapital.co.uk";
$from_email = "team@ellipsiscapital.co.uk";

// Get JSON Input
$input = file_get_contents('php://input');
$data = json_decode($input, true);

if (!$data) {
    echo json_encode(['status' => 'error', 'message' => 'Invalid data']);
    exit();
}

$name = strip_tags($data['name'] ?? 'Unknown');
$email = strip_tags($data['email'] ?? '');
$company = strip_tags($data['company'] ?? '');
$date = strip_tags($data['date'] ?? '');
$time = strip_tags($data['time'] ?? '');

if (empty($email) || empty($date) || empty($time)) {
    echo json_encode(['status' => 'error', 'message' => 'All fields are required']);
    exit();
}

// 1. Save to Local CSV (Log)
$log_entry = [date('Y-m-d H:i:s'), $name, $email, $company, $date, $time];
$fp = fopen('bookings.csv', 'a');
fputcsv($fp, $log_entry);
fclose($fp);

// 2. Email to Ellipsis Team
$team_subject = "📅 New Booking: $name ($company)";
$team_message = "
New Consultation Booked!

Founder: $name
Company: $company
Email: $email

Slot: $date @ $time

---------------------------------
System: Founders' Scheduler (In-House)
";

$team_headers = "From: $from_email\r\n";
$team_headers .= "Reply-To: $email\r\n";
$team_headers .= "X-Mailer: PHP/" . phpversion();

mail($team_email, $team_subject, $team_message, $team_headers);

// 3. Email to User
$user_subject = "Confirmed: Your Strategy Session with Ellipsis Capital";
$user_message = "
Hi $name,

Your kickoff session for $company is confirmed!

📅 Date: $date
⏰ Time: $time (London/UK)

We will meet via Google Meet. A calendar invite with the link will follow shortly.

We're excited to help you launch.

Best,

The Ellipsis Capital Team
ellipsiscapital.co.uk
";

$user_headers = "From: Ellipsis Capital <$from_email>\r\n";
$user_headers .= "Reply-To: $team_email\r\n";
$user_headers .= "X-Mailer: PHP/" . phpversion();

mail($email, $user_subject, $user_message, $user_headers);

echo json_encode(['status' => 'success', 'message' => 'Booking confirmed']);
?>
