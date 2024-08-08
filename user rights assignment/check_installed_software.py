import winreg
import logging

# Set up logging to capture the activity and any errors that occur
logging.basicConfig(filename='installed_software.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_installed_software():
    try:
        software_list = []
        
        # Registry path for installed software
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
                                # If the value doesn't exist, skip this entry
                                continue
            except Exception as e:
                logging.error(f"Error accessing registry path {registry_path}: {e}")

        # Print and log the software list
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
    get_installed_software()
