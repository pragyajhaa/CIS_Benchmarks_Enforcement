import subprocess
import logging
import re
import winreg

# Set up logging
logging.basicConfig(filename='system_audit_win7.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_admin_users():
    try:
        result = subprocess.run(['net', 'localgroup', 'administrators'], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            users = result.stdout.splitlines()
            start = False
            admin_users = []
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
        result = subprocess.run(['whoami', '/priv'], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            privileges = result.stdout.splitlines()
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

def get_hotfix_name(hotfix_id):
    hotfix_names = {
        'KB3033929': 'Security Update for Windows 7 (April 2015)',
        'KB4534310': 'Windows 7 Cumulative Update (January 2020)',
        'KB4598279': 'Security Monthly Quality Rollup (January 2021)',
    }
    return hotfix_names.get(hotfix_id, 'Unknown')

def get_windows_version(hotfix_id):
    hotfix_versions = {
        'KB3033929': 'Windows 7 SP1',
        'KB4534310': 'Windows 7 SP1',
        'KB4598279': 'Windows 7 SP1',
    }
    return hotfix_versions.get(hotfix_id, 'Unknown')

def get_installed_patches():
    try:
        result = subprocess.run(['wmic', 'qfe', 'list', 'brief'], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            if lines:
                header = lines[0]
                print(header)
                logging.info(header)
                hotfix_details = []
                for line in lines[1:]:
                    print(line)
                    logging.info(line)
                    match = re.search(r'KB\d+', line)
                    if match:
                        hotfix_id = match.group(0)
                        hotfix_name = get_hotfix_name(hotfix_id)
                        hotfix_version = get_windows_version(hotfix_id)
                        hotfix_details.append((hotfix_id, hotfix_name, hotfix_version))
                if hotfix_details:
                    print("\n{:<10} {:<60} {:<30}".format("HotFixID", "Name", "Windows Version"))
                    logging.info("{:<10} {:<60} {:<30}".format("HotFixID", "Name", "Windows Version"))
                    for hotfix_id, hotfix_name, hotfix_version in hotfix_details:
                        print("{:<10} {:<60} {:<30}".format(hotfix_id, hotfix_name, hotfix_version))
                        logging.info("{:<10} {:<60} {:<30}".format(hotfix_id, hotfix_name, hotfix_version))
                else:
                    print("No HotFixIDs found.")
                    logging.info("No HotFixIDs found.")
            else:
                print("No patches found.")
                logging.info("No patches found.")
        else:
            print("Error querying installed patches.")
            logging.error("Error querying installed patches.")
    except subprocess.CalledProcessError as e:
        logging.error(f'Error querying installed patches: {e}')
        print(f'Error querying installed patches: {e}')

def get_current_users():
    try:
        result = subprocess.run(['wmic', 'computersystem', 'get', 'username'], capture_output=True, text=True, check=True)
        if result.returncode == 0:
            users = result.stdout.splitlines()
            header = users[0]
            print(header)
            logging.info(header)
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
            username = user.split('\\')[-1]
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

def get_installed_software():
    try:
        software_list = []
        registry_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        for registry_path in registry_paths:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path) as key:
                    for i in range(0, winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                display_version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                                software_list.append((display_name, display_version))
                            except FileNotFoundError:
                                continue
            except Exception as e:
                logging.error(f"Error accessing registry path {registry_path}: {e}")
        print("\nInstalled Software:")
        logging.info("Installed Software:")
        for software, version in software_list:
            print(f"{software}: {version}")
            logging.info(f"{software}: {version}")
        return software_list
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")

if __name__ == '__main__':
    print("Fetching Admin Users and Privileges...")
    admin_users = get_admin_users()
    get_privileges()
    
    print("\nFetching Installed Patches...")
    get_installed_patches()
    
    print("\nFetching Current Users and Checking User Rights...")
    users = get_current_users()
    if users:
        check_user_rights(users)
    
    print("\nFetching Installed Software...")
    get_installed_software()
