import random
import subprocess
import sys

def generate_account_details(inisial):
    """Generate a random username and fixed password."""
    random_digits = random.randint(10000, 99999)
    username = f"{inisial}{random_digits}"
    password = "123"  # Fixed password
    return username, password

def create_vpn_account(command, inisial):
    """Create a VPN account by running the specified script with generated details."""
    username, password = generate_account_details(inisial)
    quota = 8  # Define quota in GB
    duration = 30  # Define expiry duration in days

    print(f"Generating account with script: {script}")
    
    try:
        # Split the command into a list for subprocess.run
        command_list = command.split()
        # Run the script with generated details as arguments
        subprocess.run(command_list + [username, str(quota), str(duration)], check=True)
        print(f"Account successfully created:\n Username: {username}\n Password: {password}")
    except FileNotFoundError:
        print(f"Error: The file '{script}' was not found. Check the path.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating account: {e}")

def main(script, inisial):
    """Main function to create VPN accounts based on the script path and initial."""
    print("\n════════════════════════════════════════════════")
    print("      Creating VPN Account")
    print("════════════════════════════════════════════════\n")
    
    create_vpn_account(script, inisial)

    print("\n════════════════════════════════════════════════")
    print("       VPN Account Creation Complete")
    print("════════════════════════════════════════════════")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 v2ray.py <script_path> <inisial>")
        sys.exit(1)

    script = sys.argv[1]  # Get script path from command line argument
    inisial = sys.argv[2]  # Get inisial from command line argument
    main(script, inisial)
