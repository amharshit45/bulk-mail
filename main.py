import os
import smtplib
import time
from email.message import EmailMessage

subject = "Application for FTE opportunities – Harshit Goyal"

plain_text = """
    Hi, 
    I am Harshit Goyal, a final-year B.Tech [CSE] student at IIIT Bhagalpur. 
    I am currently interning at DevRev as an MTS. 
    I am also an Expert at CodeForces with a strong foundation in Data Structures & Algorithms, computer fundamentals, and system development.
    Given my background in competitive programming and hands-on development experience, I am confident in my ability to add value to your engineering team.
    PFA my resume for your kind consideration. I would appreciate the opportunity to discuss how I can contribute to your team.
    Regards, 
    Harshit Goyal
    7888531179
    amharshit45@gmail.com
"""

html_text = """
    <html>
      <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <p>
            Hi, 
        </p>
        <p> 
            I am <strong>Harshit Goyal</strong>, a final-year <strong> B.Tech [CSE] </strong> student at <strong> IIIT Bhagalpur </strong>.
            I am currently interning at <strong> DevRev </strong> as an MTS. 
            I am also an <strong> Expert </strong> at CodeForces with a strong foundation 
            in Data Structures & Algorithms, Computer Fundamentals, and System Development. 
        </p>
        <p> 
            Given my background in competitive programming and hands-on development experience, 
            I am confident in my ability to add value to your engineering team. 
        </p>
        <p> 
            PFA my resume for your kind consideration. 
            I would appreciate the opportunity to discuss how I can contribute to your team.
        </p>
        
        <p> 
            Regards, <br>
            <strong> Harshit Goyal </strong> <br>
            📞 7888531179 <br>
            📧 <a href="mailto:amharshit45@gmail.com"> amharshit45@gmail.com </a> <br>
            <a href="https://codeforces.com/profile/amharshit45">CodeForces</a> | 
            <a href="https://leetcode.com/u/amharshit45/">LeetCode</a> | 
            <a href="https://github.com/amharshit45">GitHub</a>
        </p>
      </body>
    </html>
"""

def load_env_file(path=".env"):
    if not os.path.isfile(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, val = line.partition("=")
                key, val = key.strip(), val.strip()
                if len(val) >= 2 and val[0] in "\"'" and val[0] == val[-1]:
                    val = val[1:-1]
                os.environ[key] = val


def send_email(to_email, sender_email, sender_password, resume_path):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email
    msg.set_content(plain_text)
    msg.add_alternative(html_text, subtype='html')

    # Attach Resume
    with open(resume_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(resume_path)
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

    # Send
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)


def send_bulk_emails(email_list_file, sender_email, sender_password, resume_path):
    print(f"🔍 Checking if email list exists: {email_list_file}")
    print("✅ Found file!" if os.path.exists(email_list_file) else "❌ File not found!")

    with open(email_list_file, 'r') as f:
        emails = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    print(f"\n📬 Sending email to {len(emails)} recipients...\n")

    for idx, email in enumerate(emails, 1):
        try:
            print(f"✉ [{idx}/{len(emails)}] Sending to: {email}")
            send_email(email, sender_email, sender_password, resume_path)
            time.sleep(5)
        except Exception as e:
            print(f"⚠ Failed to send to {email}: {e}")

    print("\n✅ All emails processed!")


if __name__ == "__main__":
    load_env_file(".env")

    email_list_file_name = "list"
    email_list_file = email_list_file = os.path.abspath(email_list_file_name + ".txt")

    resume_name = "harshit_res"
    resume_path = os.path.abspath(resume_name + ".pdf")

    sender_email = os.environ.get("SENDER_EMAIL", "").strip()
    sender_password = os.environ.get("SENDER_PASSWORD", "").strip()
    if not sender_email or not sender_password:
        raise SystemExit("SENDER_EMAIL and SENDER_PASSWORD must be set (use a .env file or export them)")

    send_bulk_emails(email_list_file, sender_email, sender_password, resume_path)