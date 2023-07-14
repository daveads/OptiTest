import smtplib
from email.mime.text import MIMEText

smtp_ssl_host = 'smtp.gmail.com'
smtp_ssl_port = 465

async def send_email(html_content, sever_company_email, sever_company_password, manager_email):
    msg = MIMEText(html_content, 'html')
    
    msg['Subject'] = 'Daily Employee Activities'
    msg['From'] = sever_company_email
    msg['To'] = ', '.join(manager_email)

    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    server.login(sever_company_email, sever_company_password)
    server.sendmail(sever_company_email, manager_email, msg.as_string())
    server.quit()