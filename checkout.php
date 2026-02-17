<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// Handle Preflight
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Configuration
$team_email = "hello@ellipsiscapital.co.uk"; // Notification goes here
$from_email = "team@ellipsiscapital.co.uk";
$stripe_url = "https://buy.stripe.com/00w4gy55G8tk7gV2oc7ss05"; // Launchpad Product Link
$calendly_link = "https://calendly.com/ellipsis-capital/strategy-kickoff"; // Placeholder

// Get JSON Input
$input = file_get_contents('php://input');
$data = json_decode($input, true);

if (!$data) {
    echo json_encode(['status' => 'error', 'message' => 'Invalid data']);
    exit();
}

$name = strip_tags($data['name'] ?? 'Unknown');
$email = strip_tags($data['email'] ?? '');
$phone = strip_tags($data['phone'] ?? '');
$company = strip_tags($data['company'] ?? '');
$details = strip_tags($data['details'] ?? '');

if (empty($email)) {
    echo json_encode(['status' => 'error', 'message' => 'Email is required']);
    exit();
}

// ---------------------------------------------------------
// 1. Email to Ellipsis Team (Lead Notification)
// ---------------------------------------------------------
$team_subject = "🚀 New Launchpad Lead: $name ($company)";
$team_message = "
New Founder Launchpad Application:

Name: $name
Company: $company
Email: $email
Phone: $phone

Vision/Details:
$details

---------------------------------
Status: Redirected to Stripe for payment.
Action Required: Wait for payment confirmation, then check if they booked via Calendly.
";

$team_headers = "From: $from_email\r\n";
$team_headers .= "Reply-To: $email\r\n";
$team_headers .= "X-Mailer: PHP/" . phpversion();

mail($team_email, $team_subject, $team_message, $team_headers);

// ---------------------------------------------------------
// 2. Email to User (Welcome & Booking)
// ---------------------------------------------------------
$user_subject = "Welcome to the Launchpad – Book Your Kickoff Call";
$user_message = "
Hi $name,

Welcome to the Ellipsis Founders' Launchpad. We are excited to build your brand.

We have received your details for $company.

## Next Steps

1. **Complete Payment**: If you haven't already completed your payment via Stripe, please ensure that is done so we can allocate your team.
2. **Book Your Strategy Kickoff**: This is where we align on your vision, style, and narrative.

👉 **Book your 30-min session here:**
$calendly_link

We look forward to speaking with you.

Best,

The Ellipsis Capital Team
ellipsiscapital.co.uk
";

$user_headers = "From: Ellipsis Capital <$from_email>\r\n";
$user_headers .= "Reply-To: $team_email\r\n";
$user_headers .= "X-Mailer: PHP/" . phpversion();

mail($email, $user_subject, $user_message, $user_headers);

// ---------------------------------------------------------
// 3. Return Success to Frontend
// ---------------------------------------------------------
echo json_encode([
    'status' => 'success',
    'message' => 'Emails sent',
    'redirect_url' => $stripe_url
]);
?>
