import subprocess
import logging

# Set up logging to capture the activity and any errors that occur
logging.basicConfig(filename='current_users_rights.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_current_users():
    try:
        # Use 'wmic' to get the list of logged-in users
        result = subprocess.run(['wmic', 'computersystem', 'get', 'username'], capture_output=True, text=True, check=True)
        
        if result.returncode == 0:
            users = result.stdout.splitlines()
            
            # Print and log the header
            header = users[0]
            print(header)
            logging.info(header)
            
            # Extract and log user details
            logged_in_users = []
            for user in users[1:]:
                user = user.strip()
                if user:
                    print(user)
                    logging.info(user)
                    logged_in_users.append(user)
            
            return logged_in_users
        else:
            print("Error querying current users.")
            logging.error("Error querying current users.")
            return []

    except subprocess.CalledProcessError as e:
        logging.error(f'Error querying current users: {e}')
        print(f'Error querying current users: {e}')
        return []

def check_user_rights(users):
    try:
        for user in users:
            username = user.split('\\')[-1]  # Extract the username
            
            # Check if the user is an admin
            result = subprocess.run(['net', 'user', username], capture_output=True, text=True, check=True)
            
            if result.returncode == 0:
                user_details = result.stdout.splitlines()
                is_admin = any('Administrators' in line for line in user_details)
                
                print(f"\nUser: {username}")
                logging.info(f"\nUser: {username}")
                
                for detail in user_details:
                    print(detail)
                    logging.info(detail)
                
                if is_admin:
                    print(f"Rights: Admin")
                    logging.info(f"Rights: Admin")
                else:
                    print(f"Rights: User")
                    logging.info(f"Rights: User")
            else:
                print(f"Error retrieving details for user: {username}")
                logging.error(f"Error retrieving details for user: {username}")
    
    except subprocess.CalledProcessError as e:
        logging.error(f'Error checking user rights: {e}')
        print(f'Error checking user rights: {e}')

if __name__ == '__main__':
    users = get_current_users()
    if users:
        check_user_rights(users)
