import subprocess
import os
import logging

# set up logging
# to capture the activity and any errors that occur
# writes the necessary configuration to a temporary .inf file.
logging.basicConfig(filename='enforce_maximum_password_age.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def enforce_maximum_password_age(setting_value):
    try:
        # create a temporary inf file with the required setting
        with open('password_policy.inf', 'w') as file:
            file.write(f'''
[Unicode]
Unicode=yes
[System Access]
MaximumPasswordAge = {setting_value}
[Version]
signature="$CHICAGO$"
Revision=1
''')

        # use secedit to apply the security policy settings from the inf file
        # /configure option to apply the settings from the .inf file
        # /db option specifies the security database file
        # /overwrite option ensures that existing settings in the database are overwritten
        subprocess.run(['secedit', '/configure', '/db', 'secedit.sdb', '/cfg', 'password_policy.inf', '/overwrite'], check=True)

        # verify the changes
        result = subprocess.run(['secedit', '/export', '/cfg', 'exported_policy.inf', '/areas', 'SECURITYPOLICY'], capture_output=True, text=True, check=True)

       # print the changes to the console
        with open('exported_policy.inf', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if 'MaximumPasswordAge' in line:
                    print(f'Updated Setting: {line.strip()}')
                    logging.info(f'Updated Setting: {line.strip()}')
                    
        # Clean up the temporary files
        os.remove('password_policy.inf')
        os.remove('exported_policy.inf')

        logging.info(f'Successfully enforced maximum password age to {setting_value} days.')
        print(f'Successfully enforced maximum password age to {setting_value} days.')
        #print(result)

    # if error during execution of secedit command, logged and printed to console 
    except subprocess.CalledProcessError as e:
        logging.error(f'Error applying maximum password age setting: {e}')
        print(f'Error applying maximum password age setting: {e}')

if __name__ == '__main__':
    # Set the maximum password age to 365 days
    enforce_maximum_password_age(100)
