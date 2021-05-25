import global_vars

def get_n_emails(n):
    mails = []
    with open(global_vars.EMAIL_FILE_NAME, "r") as emails:
        mails = emails.readlines()
    first_n = [mail[:-1] for mail in mails[:n]]
    mails = mails[n:] + mails[:n]
    with open(global_vars.EMAIL_FILE_NAME, "w") as emails:
        emails.write("".join(mails))
    return first_n


if __name__ == '__main__':
    print(get_n_emails(2))
