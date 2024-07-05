import subprocess
import os
import logging

# set up logging
logging.basicConfig(filename='enforce_password_history.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def enforce_password_history():
    try:
        # create a temporary inf file with the required setting
        with open('password_history_policy.inf', 'w') as file:
            file.write('''
[Unicode]
Unicode=yes
[Version]
signature="$CHICAGO$"
Revision=1
[System Access]
PasswordHistorySize = 24
''')

        # use secedit to apply the security policy settings from the inf file
        subprocess.run(['secedit', '/configure', '/db', 'secedit.sdb', '/cfg', 'password_history_policy.inf', '/overwrite'], check=True)

        # clean up the temporary inf file
        os.remove('password_history_policy.inf')

        logging.info('Successfully enforced password history requirements.')
        print('Successfully enforced password history requirements.')

    except subprocess.CalledProcessError as e:
        logging.error(f'Error applying password history setting: {e}')
        print(f'Error applying password history setting: {e}')

if __name__ == '__main__':
    # enforce password history requirements
    enforce_password_history()
