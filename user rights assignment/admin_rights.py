import subprocess
import logging

# Set up logging to capture the activity and any errors that occur
logging.basicConfig(filename='admin_rights_privileges.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_admin_users():
    try:
        # Use 'net localgroup administrators' to get the list of admin users
        result = subprocess.run(['net', 'localgroup', 'administrators'], capture_output=True, text=True, check=True)
        
        if result.returncode == 0:
            users = result.stdout.splitlines()
            start = False
            admin_users = []
            
            # Extract and log admin users
            for line in users:
                if line.startswith("-----"):
                    start = not start
                    continue
                if start:
                    user = line.strip()
                    if user:
                        admin_users.append(user)
                        print(f"Admin User: {user}")
                        logging.info(f"Admin User: {user}")
            
            return admin_users
        else:
            print("Error querying admin users.")
            logging.error("Error querying admin users.")
            return []

    except subprocess.CalledProcessError as e:
        logging.error(f'Error querying admin users: {e}')
        print(f'Error querying admin users: {e}')
        return []

def get_privileges():
    try:
        # Use 'whoami /priv' to get the list of privileges for the current user
        result = subprocess.run(['whoami', '/priv'], capture_output=True, text=True, check=True)
        
        if result.returncode == 0:
            privileges = result.stdout.splitlines()
            
            # Log and print the privileges
            print("\nPrivileges:")
            logging.info("Privileges:")
            for privilege in privileges:
                print(privilege)
                logging.info(privilege)
        else:
            print("Error querying privileges.")
            logging.error("Error querying privileges.")
    
    except subprocess.CalledProcessError as e:
        logging.error(f'Error querying privileges: {e}')
        print(f'Error querying privileges: {e}')

if __name__ == '__main__':
    admin_users = get_admin_users()
    get_privileges()
