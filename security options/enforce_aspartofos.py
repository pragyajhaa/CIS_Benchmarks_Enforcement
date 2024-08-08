import subprocess
import logging

# Set up logging
logging.basicConfig(filename='cis_benchmark_enforcement.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def apply_security_policy():
    try:
        # Define the security template content
        security_template_content = """
        [Unicode]
        Unicode=yes
        [System Access]
        [Event Audit]
        [Registry Values]
        [Privilege Rights]
        SeTcbPrivilege = 
        """
        
        # Write the security template to a temporary file
        with open("secpol.inf", "w") as file:
            file.write(security_template_content)
        
        # Apply the security template using secedit
        subprocess.run(['secedit', '/configure', '/db', 'secedit.sdb', '/cfg', 'secpol.inf', '/areas', 'USER_RIGHTS'], check=True)
        
        # Remove the temporary security template file
        os.remove("secpol.inf")
        
        logging.info("Successfully applied security policy to ensure 'Act as part of the operating system' is set to 'No One'.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error applying security policy: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == '__main__':
    apply_security_policy()
