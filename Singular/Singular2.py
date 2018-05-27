import email
import imaplib
import os
import sys
from Singular1 import report_parser


def save_attachment(msg, download_folder="/tmp"):
    """
    Given a message, save its attachments to the specified
    download folder (default is /tmp)

    return: file path to attachment
    """
    att_path = "No attachment found."
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        filename = part.get_filename()
        att_path = os.path.join(download_folder, filename)

        if not os.path.isfile(att_path):
            fp = open(att_path, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
    return att_path


def mail_report_parser(username, password):
    download_dir = os.getcwd()  # change download_dir if needed
    gmail_imap_url = 'imap.gmail.com'

    mail_connector = imaplib.IMAP4_SSL(gmail_imap_url)
    try:
        mail_connector.login(username+"@gmail.com", password)
    except imaplib.IMAP4.error:
        print('LOGIN FAILED!')
        sys.exit(1)

    mail_connector.select('inbox')

    searchterm_from_you = 'FROM "{}"'.format("Yonatan Komornik")
    searchterm_subject = 'SUBJECT "{}"'.format("Singular Python Exercise")
    searchterm_allterms = "{} {}".format(searchterm_from_you, searchterm_subject)

    result, data = mail_connector.uid('search', None, searchterm_allterms)
    mail_uid = (data[0].split())[0]

    result, data = mail_connector.uid('fetch', mail_uid, '(RFC822)')

    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email)

    file_path = save_attachment(email_message, download_dir)
    report_parser(file_path)


def main():
    if len(sys.argv) != 3:
        print("Command should be: 'python Singular2.py <gmail-username> <password>'")
        sys.exit(1)
    mail_report_parser(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
