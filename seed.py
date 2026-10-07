from app import create_app
from database import db, User, Scenario, Option, Badge, Skill

def seed_database():
    app = create_app()
    with app.app_context():
        # Drop all tables and recreate them to ensure a clean slate
        db.drop_all()
        db.create_all()

        print("Creating users...")
        admin = User(name='Admin User', email='admin@cyberarena.local', role='admin')
        admin.set_password('admin123')
        
        student = User(name='Test Student', email='student@cyberarena.local', role='student')
        student.set_password('student123')
        student.xp = 1500
        student.level = 4
        student.total_score = 1500
        student.streak = 3
        
        db.session.add(admin)
        db.session.add(student)

        print("Creating badges...")
        badges = [
            Badge(name='Phishing Hunter', description='Identify 5 phishing scenarios correctly.', icon='fas fa-fish', requirement='5_phishing'),
            Badge(name='Scam Detector', description='Identify 5 digital payment scams correctly.', icon='fas fa-money-bill-wave', requirement='5_scam'),
            Badge(name='Password Guardian', description='Complete password security challenges.', icon='fas fa-key', requirement='password_challenges'),
            Badge(name='Social Engineering Expert', description='Successfully complete 5 social engineering challenges.', icon='fas fa-users', requirement='5_se'),
            Badge(name='Cyber Defender', description='Reach an overall score of 80%.', icon='fas fa-shield-alt', requirement='80_score'),
            Badge(name='Security Streak', description='Maintain a 7-day streak.', icon='fas fa-fire', requirement='7_streak')
        ]
        db.session.add_all(badges)

        print("Creating skills...")
        skill_names = ['Phishing', 'Password Security', 'Privacy', 'Social Engineering', 'Malware Awareness', 'Web Safety', 'Digital Payment', 'Incident Response']
        for name in skill_names:
            db.session.add(Skill(name=name))

        print("Creating scenarios...")
        # ==========================================
        # PHISHING (4)
        # ==========================================
        s1 = Scenario(
            title="Suspicious College Email",
            category="Phishing",
            difficulty="Easy",
            description="You receive an urgent email from 'college-verifiy.com'.",
            scenario_text="<p><strong>From:</strong> IT Support (it-support@college-verifiy.com)</p><p><strong>Subject:</strong> URGENT: Your College Account Will Be Disabled</p><p>Your account will be suspended within 24 hours due to inactivity. Click the verification link below to keep your account active.</p>",
            threat_type="Credential Harvesting Phishing",
            explanation="The email uses urgency and a misspelled domain (college-verifiy.com instead of a legitimate .edu domain) to trick you into clicking a malicious link.",
            security_tip="Never enter credentials through links received in unexpected messages. Verify the sender using an official channel."
        )
        s1_opts = [
            Option(option_text="Click the link immediately to prevent suspension.", is_correct=False, explanation="Clicking the link will likely take you to a fake login page designed to steal your credentials."),
            Option(option_text="Reply to the email asking for more time.", is_correct=False, explanation="Replying confirms your email address is active to the attacker."),
            Option(option_text="Report the email as suspicious and do not click the link.", is_correct=True, explanation="Correct! Reporting the phishing attempt helps the organization block the attacker."),
            Option(option_text="Forward it to a friend to see if they got it too.", is_correct=False, explanation="Forwarding spreads the potential threat to others.")
        ]
        
        s2 = Scenario(
            title="Fake Scholarship Offer",
            category="Phishing",
            difficulty="Medium",
            description="An email promises a $10,000 scholarship if you pay a processing fee.",
            scenario_text="<p><strong>Subject:</strong> Congratulations! You've been selected!</p><p>You have been awarded a $10,000 National Merit Scholarship. To process your funds, please click the link to pay a small $50 administrative fee.</p>",
            threat_type="Advance Fee Fraud",
            explanation="Legitimate scholarships do not require an upfront fee. The sense of a massive reward is used to cloud judgment.",
            security_tip="If it sounds too good to be true, it probably is. Never pay to receive a scholarship."
        )
        s2_opts = [
            Option(option_text="Pay the $50 fee using a credit card.", is_correct=False, explanation="You will lose the $50 and your credit card details will be stolen."),
            Option(option_text="Search for the scholarship online independently.", is_correct=True, explanation="Correct! Always verify offers independently through a search engine rather than clicking email links."),
            Option(option_text="Click the link but only provide fake information.", is_correct=False, explanation="Clicking the link could still expose you to malware."),
            Option(option_text="Email them back asking for proof.", is_correct=False, explanation="Scammers will provide fake proof. Engaging is dangerous.")
        ]

        s3 = Scenario(
            title="HR Policy Update",
            category="Phishing",
            difficulty="Hard",
            description="An email appearing to be from your company's HR department with an attached PDF.",
            scenario_text="<p><strong>From:</strong> hr-update@yourcompany.com</p><p>Please review the attached updated employee handbook immediately. You must sign the acknowledgment on the last page by EOD.</p>",
            threat_type="Malicious Attachment",
            explanation="The email spoofs the internal HR address and uses urgency. The PDF likely contains a macro or exploit.",
            security_tip="Always verify unexpected internal requests with the sender via phone or Slack before opening attachments."
        )
        s3_opts = [
            Option(option_text="Open the PDF since it's an internal email.", is_correct=False, explanation="Sender addresses can be easily spoofed."),
            Option(option_text="Forward it to your personal email to read on your phone.", is_correct=False, explanation="This bypasses corporate security and puts your personal device at risk."),
            Option(option_text="Contact HR via an internal messaging tool to verify the email.", is_correct=True, explanation="Correct! Verifying through a secondary channel is the safest approach."),
            Option(option_text="Delete it and ignore it.", is_correct=False, explanation="While safe for you, reporting it protects the rest of the company.")
        ]
        
        s4 = Scenario(
            title="Streaming Service Billing Error",
            category="Phishing",
            difficulty="Medium",
            description="An SMS claims your Netflix account is on hold.",
            scenario_text="<p>NETFLIX: Your last payment was declined. Your account is on hold. Update payment info here: http://netfIix-billing-update.com/login</p>",
            threat_type="Smishing (SMS Phishing)",
            explanation="The text uses urgency and a lookalike domain (capital 'I' instead of 'l') to steal credit card details.",
            security_tip="Never click links in unexpected text messages. Go directly to the official app or website to check your account status."
        )
        s4_opts = [
            Option(option_text="Click the link to fix the payment issue.", is_correct=False, explanation="The link goes to a fake site that will steal your credit card data."),
            Option(option_text="Call the number the text came from.", is_correct=False, explanation="The number is likely spoofed or belongs to the scammer."),
            Option(option_text="Open the Netflix app directly to check your account status.", is_correct=True, explanation="Correct! Always navigate to the service independently to verify account issues."),
            Option(option_text="Reply STOP to unsubscribe.", is_correct=False, explanation="Replying confirms to the scammer that your number is active.")
        ]

        # ==========================================
        # SOCIAL ENGINEERING (4)
        # ==========================================
        s5 = Scenario(
            title="Fake IT Support Call",
            category="Social Engineering",
            difficulty="Medium",
            description="You receive a phone call from someone claiming to be from IT.",
            scenario_text="<p>The caller says: 'Hi, this is Mike from IT. We are seeing unusual activity on your account. I need you to read me the 6-digit code we just texted you so I can secure your account.'</p>",
            threat_type="Pretexting / MFA Bypass",
            explanation="The attacker is trying to log into your account and needs the Multi-Factor Authentication (MFA) code sent to your phone.",
            security_tip="IT will NEVER ask for your password or your MFA security codes."
        )
        s5_opts = [
            Option(option_text="Read them the code to secure the account.", is_correct=False, explanation="Providing the code gives the attacker full access to your account."),
            Option(option_text="Ask them for their employee ID before giving the code.", is_correct=False, explanation="They can easily make up a fake ID."),
            Option(option_text="Hang up and call the official IT support desk number.", is_correct=True, explanation="Correct! Hanging up and using an official, known channel verifies their identity."),
            Option(option_text="Read the code backwards to trick them.", is_correct=False, explanation="Engaging with scammers is risky and unnecessary.")
        ]

        s6 = Scenario(
            title="Tailgating at the Office",
            category="Social Engineering",
            difficulty="Easy",
            description="You are entering your secure office building.",
            scenario_text="<p>As you swipe your badge to open the secure door, a person carrying two large boxes of coffee and donuts rushes up behind you. They ask, 'Hey, can you hold the door? My hands are completely full!'</p>",
            threat_type="Tailgating / Physical Breach",
            explanation="Attackers often use props (like boxes) or act in a hurry to exploit social norms of politeness and bypass physical security.",
            security_tip="Security over politeness. Everyone must badge in, no matter what."
        )
        s6_opts = [
            Option(option_text="Hold the door open for them, it's the polite thing to do.", is_correct=False, explanation="You just allowed an unauthorized person into a secure area."),
            Option(option_text="Ask them who they are visiting before holding the door.", is_correct=False, explanation="They can lie. You are not a security guard."),
            Option(option_text="Apologize, close the door, and tell them they must use their own badge.", is_correct=True, explanation="Correct! It might feel rude, but enforcing physical security is everyone's job."),
            Option(option_text="Take one of the boxes so they can use their badge.", is_correct=False, explanation="While helpful, this still creates a chaotic situation where they might slip in.")
        ]
        
        s7 = Scenario(
            title="The Urgent CEO Request",
            category="Social Engineering",
            difficulty="Hard",
            description="You get an urgent direct message from the CEO on Slack/Teams.",
            scenario_text="<p><strong>CEO:</strong> 'I am in a confidential meeting with a client and my corporate card was declined. Buy $500 in Apple gift cards immediately for client gifts and send me the codes. I will reimburse you later today.'</p>",
            threat_type="CEO Fraud / Business Email Compromise",
            explanation="The attacker has compromised the CEO's account (or spoofed it) and is using authority and urgency to bypass standard procedures.",
            security_tip="Gift cards are almost never a legitimate business expense. Always verify unusual requests from executives out of band (e.g., a phone call)."
        )
        s7_opts = [
            Option(option_text="Buy the gift cards immediately to impress the CEO.", is_correct=False, explanation="You will lose $500 and the company will not reimburse you for falling for a scam."),
            Option(option_text="Ask the CEO for a purchase order number in the chat.", is_correct=False, explanation="The attacker is in the chat and will just make one up."),
            Option(option_text="Call the CEO or their assistant on a known phone number to verify.", is_correct=True, explanation="Correct! Out-of-band verification breaks the attacker's control over the communication channel."),
            Option(option_text="Tell the CEO you don't have $500.", is_correct=False, explanation="The attacker will just try to get a smaller amount from you.")
        ]
        
        s8 = Scenario(
            title="The Helpful Flash Drive",
            category="Social Engineering",
            difficulty="Easy",
            description="You find something interesting in the company parking lot.",
            scenario_text="<p>While walking to your car, you find a USB flash drive on the ground with a label reading: '2025 Executive Bonus Payouts - CONFIDENTIAL'.</p>",
            threat_type="Baiting / USB Drop",
            explanation="Attackers drop infected USB drives hoping someone's curiosity will lead them to plug it into a corporate network.",
            security_tip="Never plug untrusted devices into your computer. Curiosity can compromise an entire network."
        )
        s8_opts = [
            Option(option_text="Plug it into your work computer to see who gets a bonus.", is_correct=False, explanation="The drive likely contains malware that will immediately infect the network."),
            Option(option_text="Plug it into an old personal laptop instead.", is_correct=False, explanation="You are still risking a personal device infection."),
            Option(option_text="Hand it over to your IT or Security department.", is_correct=True, explanation="Correct! IT has isolated environments to safely investigate suspicious devices."),
            Option(option_text="Throw it in the trash.", is_correct=False, explanation="Someone else might find it and plug it in.")
        ]

        # ==========================================
        # DIGITAL PAYMENT (3)
        # ==========================================
        s9 = Scenario(
            title="QR Reward Scam",
            category="Digital Payment",
            difficulty="Medium",
            description="You receive a WhatsApp message offering a cashback reward.",
            scenario_text="<p>Message: 'Congratulations! You've won ₹500 cashback on your last purchase. Scan this QR code using your UPI app to receive the money instantly into your bank account.'</p>",
            threat_type="QR Code Fraud",
            explanation="Scanning a QR code on UPI apps is for SENDING money, not receiving it. The scammer is trying to make you authorize a payment to them.",
            security_tip="You NEVER need to enter a PIN or scan a QR code to receive money in your bank account."
        )
        s9_opts = [
            Option(option_text="Scan the code to claim the cashback.", is_correct=False, explanation="You will authorize a payment and lose money."),
            Option(option_text="Ask them to send the money via bank transfer instead.", is_correct=False, explanation="Engaging with scammers is a waste of time and risky."),
            Option(option_text="Block the sender and report the message.", is_correct=True, explanation="Correct! Never scan a QR code to receive money."),
            Option(option_text="Scan the code but enter a wrong PIN.", is_correct=False, explanation="Never scan suspicious codes in the first place.")
        ]

        s10 = Scenario(
            title="Fake UPI Refund",
            category="Digital Payment",
            difficulty="Medium",
            description="You get a call about a failed transaction refund.",
            scenario_text="<p>The caller says: 'Your recent Amazon order failed, and we need to refund ₹1500. Please open your GPay app, you will see a request for ₹1500. Enter your PIN to approve the refund to your account.'</p>",
            threat_type="Payment Request Scam",
            explanation="The scammer has initiated a 'Collect' request. Entering your PIN authorizes money to leave your account, not enter it.",
            security_tip="A UPI PIN is only used to deduct money from your account."
        )
        s10_opts = [
            Option(option_text="Open the app and enter your PIN to get the refund.", is_correct=False, explanation="Entering your PIN will transfer money TO the scammer."),
            Option(option_text="Decline the collect request in your app and hang up.", is_correct=True, explanation="Correct! You recognized that Collect requests take your money."),
            Option(option_text="Tell the caller you will call Amazon customer care.", is_correct=False, explanation="While safer, it's best to actively decline the fraudulent request in your app."),
            Option(option_text="Give them your bank account number instead.", is_correct=False, explanation="Never share banking details with unverified callers.")
        ]
        
        s11 = Scenario(
            title="Customer Support Search",
            category="Digital Payment",
            difficulty="Hard",
            description="You have an issue with a recent digital payment.",
            scenario_text="<p>A transaction is stuck. You Google 'PhonePe Customer Care Number' and call the first number that appears in a sponsored ad. The person answers and asks you to download 'AnyDesk' to help resolve the issue.</p>",
            threat_type="Search Engine Poisoning & Remote Access Scam",
            explanation="Scammers place fake ads with fake customer care numbers. Apps like AnyDesk give them remote control over your phone to steal your money.",
            security_tip="Only find support numbers inside the official app. Never download remote access software on the instruction of customer support."
        )
        s11_opts = [
            Option(option_text="Download the app so they can fix the issue quickly.", is_correct=False, explanation="They will take control of your screen, open your banking app, and steal your money."),
            Option(option_text="Refuse to download the app but read them your card details.", is_correct=False, explanation="Never read card details over the phone to unverified support."),
            Option(option_text="Hang up immediately and use the 'Help' section inside the official payment app.", is_correct=True, explanation="Correct! Official support is always best accessed through the secure app environment."),
            Option(option_text="Search Google again for a different number.", is_correct=False, explanation="The search results are likely still compromised.")
        ]

        # ==========================================
        # PASSWORD SECURITY (3)
        # ==========================================
        s12 = Scenario(
            title="Choosing a New Password",
            category="Password Security",
            difficulty="Easy",
            description="You are setting up a new banking account.",
            scenario_text="<p>The system requires a new password. You want something you can remember but that is also secure.</p>",
            threat_type="Weak Password Creation",
            explanation="Short passwords, dictionary words, and personal information are easily cracked by automated tools.",
            security_tip="Length beats complexity. A 16-character passphrase of random words is stronger than a 8-character complex password."
        )
        s12_opts = [
            Option(option_text="Password123!", is_correct=False, explanation="This is one of the most common passwords in the world."),
            Option(option_text="Your dog's name and birth year (e.g., Buster2015)", is_correct=False, explanation="Personal info is easily found on social media."),
            Option(option_text="BlueHorseStaplerBattery!42", is_correct=True, explanation="Correct! A long passphrase of random words is highly secure and easier to remember."),
            Option(option_text="The same password you use for your email.", is_correct=False, explanation="Password reuse means if one account is breached, they all are.")
        ]

        s13 = Scenario(
            title="The Shared Account",
            category="Password Security",
            difficulty="Medium",
            description="A colleague asks for a favor while they are out of the office.",
            scenario_text="<p>'Hey, I forgot to submit the quarterly report! Can I give you my password so you can log in as me and click submit? It will only take a second.'</p>",
            threat_type="Credential Sharing",
            explanation="Sharing passwords violates security policies and removes accountability (non-repudiation) from systems.",
            security_tip="Never share your password, even with colleagues or IT. Use proper delegation features if a system supports them."
        )
        s13_opts = [
            Option(option_text="Log in and help them out; it's a team effort.", is_correct=False, explanation="You are violating security policy and taking responsibility for actions under their account."),
            Option(option_text="Ask them to email the password so there is a record.", is_correct=False, explanation="Emailing passwords in plain text is a severe security risk."),
            Option(option_text="Politely refuse and suggest they contact IT for remote access.", is_correct=True, explanation="Correct! You protected both yourself and your colleague by maintaining security protocols."),
            Option(option_text="Change their password for them after you log in.", is_correct=False, explanation="This does not solve the root issue of credential sharing.")
        ]
        
        s14 = Scenario(
            title="Data Breach Notification",
            category="Password Security",
            difficulty="Hard",
            description="You read the news.",
            scenario_text="<p>You see a news article stating that 'FitnessApp', a service you use, has suffered a massive data breach. Millions of passwords have been leaked online.</p>",
            threat_type="Credential Stuffing Risk",
            explanation="When a site is breached, attackers use the stolen username/password pairs to try and log into banking, email, and corporate accounts.",
            security_tip="Always use unique passwords for every service so a breach at one company doesn't compromise your entire digital life."
        )
        s14_opts = [
            Option(option_text="Do nothing, you don't care if someone sees your workout data.", is_correct=False, explanation="If you reused that password anywhere else, those accounts are now compromised."),
            Option(option_text="Change your FitnessApp password immediately, and change any other accounts that used the same password.", is_correct=True, explanation="Correct! Mitigating the risk of credential stuffing is the priority."),
            Option(option_text="Delete the FitnessApp app from your phone.", is_correct=False, explanation="Deleting the app does not delete your compromised data from their servers."),
            Option(option_text="Wait for FitnessApp to email you instructions.", is_correct=False, explanation="Companies can take weeks to notify users; you must act immediately.")
        ]

        # ==========================================
        # MALWARE AWARENESS (3)
        # ==========================================
        s15 = Scenario(
            title="Suspicious Software Update",
            category="Malware Awareness",
            difficulty="Easy",
            description="You are browsing a sports website.",
            scenario_text="<p>A popup suddenly appears: 'WARNING: Your Flash Player is out of date. Click here to update now to view this video.' The download starts automatically.</p>",
            threat_type="Drive-by Download / Malvertising",
            explanation="Fake updates are a common way to distribute malware. (Also, Flash Player is discontinued).",
            security_tip="Only download software updates directly from the official developer's website or app store."
        )
        s15_opts = [
            Option(option_text="Run the downloaded file to update your system.", is_correct=False, explanation="The file is malware and will infect your computer."),
            Option(option_text="Cancel the download and close the popup/tab.", is_correct=True, explanation="Correct! Recognizing fake updates prevents malware infections."),
            Option(option_text="Click the popup to see where it leads.", is_correct=False, explanation="Clicking malicious popups can trigger further unwanted downloads."),
            Option(option_text="Turn off your antivirus so the update installs faster.", is_correct=False, explanation="Never disable your security controls for an unexpected download.")
        ]
        
        s16 = Scenario(
            title="The Free Software License",
            category="Malware Awareness",
            difficulty="Medium",
            description="You need expensive video editing software for a project.",
            scenario_text="<p>You find a YouTube video offering a 'Free Crack + Keygen' for the software. The link points to a file hosting site. The video has many comments saying 'It works, thanks!'</p>",
            threat_type="Trojan / Pirated Software",
            explanation="Pirated software and keygens almost always contain hidden malware (Trojans, ransomware, or cryptominers). The comments are usually fake.",
            security_tip="Never use cracked or pirated software. The cost of a malware infection is far higher than the software license."
        )
        s16_opts = [
            Option(option_text="Download it, but scan it with antivirus first.", is_correct=False, explanation="Antivirus doesn't catch everything; custom malware in cracks easily bypasses it."),
            Option(option_text="Download it but only run it once to get the key.", is_correct=False, explanation="Running it once is all it takes to infect your system."),
            Option(option_text="Avoid the download and look for a free, open-source alternative.", is_correct=True, explanation="Correct! Using legitimate open-source software is the safest alternative."),
            Option(option_text="Ask a friend to download it and send it to you.", is_correct=False, explanation="You are just transferring the risk to a friend.")
        ]
        
        s17 = Scenario(
            title="Macro Warning",
            category="Malware Awareness",
            difficulty="Hard",
            description="You receive an Excel file from a vendor.",
            scenario_text="<p>When you open 'Invoice_Q3.xlsm', Excel shows a yellow ribbon saying: 'SECURITY WARNING: Macros have been disabled.' The document itself has an image saying 'Please click Enable Content to view the secure invoice.'</p>",
            threat_type="Macro Malware",
            explanation="Macros are powerful scripts in Office documents. Attackers use social engineering to trick you into enabling them, which executes the malware.",
            security_tip="Never enable macros on a document from an external source unless you explicitly expected it and verified it."
        )
        s17_opts = [
            Option(option_text="Click 'Enable Content' since it's from a vendor.", is_correct=False, explanation="The vendor's email might be compromised, and the macro will execute malware."),
            Option(option_text="Leave macros disabled and contact the vendor to ask for a standard PDF invoice.", is_correct=True, explanation="Correct! A secure invoice does not require macros. Requesting a safe format is the right move."),
            Option(option_text="Forward it to the finance department to handle.", is_correct=False, explanation="You are putting another department at risk."),
            Option(option_text="Enable macros but disconnect from the internet first.", is_correct=False, explanation="The malware might still encrypt your local files (ransomware).")
        ]

        # ==========================================
        # PRIVACY & WEB SAFETY (3)
        # ==========================================
        s18 = Scenario(
            title="Airport Wi-Fi",
            category="Privacy",
            difficulty="Medium",
            description="You are waiting at an airport gate.",
            scenario_text="<p>You want to check your bank balance. You see an open, free Wi-Fi network called 'Free_Airport_WiFi_Fast'.</p>",
            threat_type="Man-in-the-Middle (MitM) / Rogue Hotspot",
            explanation="Open, public Wi-Fi networks are unencrypted, and attackers can easily intercept your traffic or set up fake hotspots (Evil Twin).",
            security_tip="Avoid accessing sensitive information on public Wi-Fi. If you must, use a trusted VPN."
        )
        s18_opts = [
            Option(option_text="Connect and quickly check your bank balance.", is_correct=False, explanation="An attacker on the network could intercept your banking credentials."),
            Option(option_text="Turn off Wi-Fi and use your cellular data instead to check your bank.", is_correct=True, explanation="Correct! Cellular data is encrypted and much safer for sensitive transactions."),
            Option(option_text="Connect, but only use your web browser's incognito mode.", is_correct=False, explanation="Incognito mode only hides history locally; it does not encrypt your network traffic."),
            Option(option_text="Connect to a different open network that has a password.", is_correct=False, explanation="If the password is public (like in a cafe), the network is still effectively open to interception.")
        ]
        
        s19 = Scenario(
            title="The Oversharing Colleague",
            category="Privacy",
            difficulty="Easy",
            description="You are scrolling through LinkedIn.",
            scenario_text="<p>Your coworker posts a photo of their desk with the caption 'First day at the new office! So excited!' In the background, their monitor clearly shows an open email with a client list, and their employee badge is visible on the desk.</p>",
            threat_type="Information Disclosure",
            explanation="Social media oversharing is a massive source of open-source intelligence (OSINT) for attackers.",
            security_tip="Always review photos for sensitive information in the background before posting online."
        )
        s19_opts = [
            Option(option_text="Like the post and comment congratulations.", is_correct=False, explanation="You are ignoring a security incident."),
            Option(option_text="Report the post to LinkedIn.", is_correct=False, explanation="LinkedIn likely won't take it down as it doesn't violate their TOS, only your company's."),
            Option(option_text="Privately message the coworker to immediately take the photo down.", is_correct=True, explanation="Correct! Promptly addressing the spill limits the exposure of the data."),
            Option(option_text="Download the photo to show others how not to take pictures.", is_correct=False, explanation="You are creating another copy of sensitive data.")
        ]

        s20 = Scenario(
            title="The Incredible Deal",
            category="Web Safety",
            difficulty="Medium",
            description="You are shopping online for a new laptop.",
            scenario_text="<p>You find an Instagram ad for a brand new MacBook Pro for $300 (usually $1500). The website is 'applestore-discount-deals.shop'. The site looks professional and has a checkout page.</p>",
            threat_type="Fake E-commerce Site",
            explanation="Scammers create realistic-looking fake shops with impossible prices to steal credit card information.",
            security_tip="Check the URL carefully. Legitimate companies do not use domains like 'discount-deals.shop'."
        )
        s20_opts = [
            Option(option_text="Buy it immediately before it sells out.", is_correct=False, explanation="You will lose $300, get nothing, and your card will be compromised."),
            Option(option_text="Check if the website URL matches the official brand and look for reviews on third-party sites.", is_correct=True, explanation="Correct! Verifying the domain and checking external reviews prevents shopping scams."),
            Option(option_text="Use a debit card instead of a credit card to be safe.", is_correct=False, explanation="Debit cards offer LESS fraud protection than credit cards."),
            Option(option_text="Add it to your cart to see if the price changes.", is_correct=False, explanation="Providing any information to a fake site is risky.")
        ]

        scenarios = [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20]
        
        # Link options and add to session
        for s in scenarios:
            if s == s1: s.options = s1_opts
            if s == s2: s.options = s2_opts
            if s == s3: s.options = s3_opts
            if s == s4: s.options = s4_opts
            if s == s5: s.options = s5_opts
            if s == s6: s.options = s6_opts
            if s == s7: s.options = s7_opts
            if s == s8: s.options = s8_opts
            if s == s9: s.options = s9_opts
            if s == s10: s.options = s10_opts
            if s == s11: s.options = s11_opts
            if s == s12: s.options = s12_opts
            if s == s13: s.options = s13_opts
            if s == s14: s.options = s14_opts
            if s == s15: s.options = s15_opts
            if s == s16: s.options = s16_opts
            if s == s17: s.options = s17_opts
            if s == s18: s.options = s18_opts
            if s == s19: s.options = s19_opts
            if s == s20: s.options = s20_opts
            
            db.session.add(s)

        db.session.commit()
        print("Database seeded successfully with 20 scenarios, users, skills, and badges!")

if __name__ == '__main__':
    seed_database()
