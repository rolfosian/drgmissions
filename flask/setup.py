from pwd import getpwnam
from grp import getgrnam
import os
import subprocess
import shutil
import json
import random
import string
import re

def get_linux_distribution():
    try:
        result = subprocess.run(['lsb_release', '-is'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        distribution_id = result.stdout.decode('utf-8').strip()
        return distribution_id
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    
def check_root_privileges():
    if os.geteuid() == 0:
        return
    else:
        print("Please run this script with root privileges.")
        quit()

def wrap_with_color(string, color=37):
    return f"\033[1;{color}m{string}\033[0m"

def wrapped_print(func):
    def wrapper(*args, **kwargs):
        include_color = kwargs.pop('include_color', True)
        if include_color:
            args = [wrap_with_color(str(arg)) for arg in args]
        return func(*args, **kwargs)
    return wrapper
print = wrapped_print(print)

def wrapped_input(func):
    def wrapper(arg, **kwargs):
        include_color = kwargs.pop('include_color', True)
        if include_color:
            arg = wrap_with_color(str(arg))
        return func(arg, **kwargs)
    return wrapper
input = wrapped_input(input)

def generate_random_string(length=30):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def yes_or_no(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response == 'y':
            return True
        elif response == 'n':
            return False
        else:
            print("Please enter 'Y' or 'N'.")

def confirm_user_input(prompt):
    while True:
        user_input = input(f'{prompt}: ')
        if yes_or_no(f'Confirm {user_input}? Y/N: '):
            break
        else:
            continue
    return user_input

def user_exists(username):
    try:
        getpwnam(username)
        return True
    except:
        return False

def create_group(group_name):
    subprocess.run(['groupadd', group_name])

def add_user_to_group(user_name, group_name):
    subprocess.run(['usermod', '-aG', group_name, user_name])

def change_ownership_recursively(directory_path, user_name, group_name ):
    try:
        uid = getpwnam(user_name).pw_uid
        gid = getgrnam(group_name).gr_gid
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                os.chown(file_path, uid, gid)
                
            for directory in dirs:
                dir_path = os.path.join(root, directory)
                os.chown(dir_path, uid, gid)
    except OSError as e:
        print(f"Failed to change ownership recursively for directory '{directory_path}': {e}")


def create_venv(proj_cwd):
    result = subprocess.run(["python3", "-m", "venv", f"{proj_cwd}/venv"], capture_output=True, text=True)
    error = result.returncode
    if error != 0:
        cmd = result.stdout.splitlines()[4].strip().split(' ')
        cmd.insert(2, '-y')
        subprocess.run(cmd)
        return create_venv(proj_cwd)

def activate_venv(proj_cwd):
    activate_path = os.path.join(f'{proj_cwd}/venv', "bin", "activate")
    subprocess.run(["bash", "-c", f"source {activate_path}"])

def deactivate_venv(proj_cwd):
    activate_path = os.path.join(f'{proj_cwd}/venv', "bin", "activate")
    subprocess.run(["bash", "-c", f"source {activate_path}"])

def install_packages(proj_cwd):
    subprocess.run([os.path.join(proj_cwd, 'venv', "bin", "pip"), "install", "-r", "requirements.txt"])

def match_item(item, ignore_list):
    for pattern in ignore_list: 
        if re.match(pattern, item):
            return True
    return False

def copy_directory(source, target, ignore_list):
    os.mkdir(target+'/flask')

    for item in os.listdir(source):
        if match_item(item, ignore_list):
            continue

        source_item = os.path.join(source, item)
        target_item = os.path.join(target+'/flask', item)

        if os.path.isdir(source_item):
            shutil.copytree(source_item, target_item, ignore=shutil.ignore_patterns(*ignore_list), dirs_exist_ok=True)
        else:
            shutil.copy2(source_item, target_item)

def create_systemd_service(service_name, service_user, proj_cwd):
    with open(f"/etc/systemd/system/{service_name}.service", "w") as f:
        f.write(f"""[Unit]
Description=Gunicorn instance to serve {service_name}
After=network.target

[Service]
User={service_user}
Group=www-data
WorkingDirectory={proj_cwd}/flask
Environment="PATH={proj_cwd}/venv/bin"
ExecStart={proj_cwd}/venv/bin/gunicorn --config {proj_cwd}/flask/gunicorn.conf.py main:app

[Install]
WantedBy=multi-user.target
""")
        f.close()

def set_nginx_reverse_proxy(domain_name, service_bind, max_body_size, auth_token):
    subprocess.run(['apt', 'install', '-y', 'nginx'])

    sites_available_dir = "/etc/nginx/sites-available/"
    max_body_size = str(max_body_size)

    with open(f"{sites_available_dir}/{domain_name}", 'w') as f:
        f.write("""server {{
    listen 80;
    listen [::]:80;
    server_name {domain_name};
    client_max_body_size {max_body_size};

    location / {{
        proxy_pass http://{service_bind};
        include proxy_params;
    }}
    
}}
""".format(service_bind=service_bind, domain_name=domain_name, max_body_size=max_body_size))
        f.close()
    
    subprocess.run(['ln', '-s', f'{sites_available_dir}/{domain_name}', '/etc/nginx/sites-enabled/'])
    subprocess.run(['nginx', '-t'])
    subprocess.run(['systemctl', 'restart', 'nginx'])
    
    if not domain_name[0].isdigit():
        if yes_or_no('Run certbot for site? Y/N: '):
            while True:
                try:
                    subprocess.run(['apt', 'install', '-y', 'certbot', 'python3-certbot-nginx'], check=True)
                    
                    if yes_or_no('Run certbot with --register-unsafely-without-email option? Y/N: '):
                        subprocess.run(['certbot', '--register-unsafely-without-email'])
                    
                    subprocess.run(['certbot', '--nginx', '-d', domain_name], check=True)
                    break
                except Exception as e:
                    print('Error:', e, 'Try Again.')
                    continue

            set_cfg(domain_name, service_bind, auth_token, max_body_size, use_https=True)

def set_cfg(domain_name, service_bind, auth_token, max_body_size, use_https=False):
    cfg = json.dumps({
    "domain_name" : domain_name,
    "max_body_size" : max_body_size,
    "service_bind" : service_bind,
    "auth_token" : auth_token,
    "use_https" : use_https
    }, indent=1)
    
    with open('cfg.json', 'w') as f:
        f.write(cfg)
        f.close()
    print("\x1b[4;37m!!!!MAKE SURE TO COPY THIS TO YOUR scraper_cfg.json IN THE DEEP ROCK GALACTIC\BINARIES\WIN64 FOLDER!!!!\x1b[0m", include_color=False)
    print(cfg)
    print('------------------------------------------------------------------------------------------------------')
    return cfg

def set_gconf_bind(service_bind):
    gconf = ""
    with open('gunicorn.conf.py', 'r') as f:
        gconf_ = f.readlines()
        for line in gconf_:
            if line.startswith('bind'):
                line = f"bind = '{service_bind}'"
            gconf += f"{line}\n"
        f.close()
        
    with open('gunicorn.conf.py', 'w') as f:
        f.write(gconf)
        f.close()
        
def initialize_service(service_name):
    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "start", service_name])
    subprocess.run(["systemctl", "enable", service_name])

def main():
    cwd = os.path.abspath(__file__)
    cwd = '/'.join(cwd.split('/')[:-1])
    
    print('Welcome to the drgmissions service setup. Follow the prompts and make sure to copy down the cfg.json when it is generated.')
    print('------------------------------------------------------------------------------------------------------------------------')
    service_name = confirm_user_input('Enter service name')
    service_bind = confirm_user_input('Enter service bind (eg 127.0.0.1:5000 ')
    set_gconf_bind(service_bind)
    
    print('Generating auth token...')
    auth_token = generate_random_string()
    cfg = set_cfg("", service_bind, auth_token, 200000000)
    
    while True:
        service_user = confirm_user_input('Enter service user')
        if user_exists(service_user):
            break
        print('Please enter an existing valid username.')
    
    proj_cwd = f'/home/{service_user}/{service_name}'
    
    print('Creating venv...')
    create_venv(proj_cwd)
    print('Activating venv...')
    activate_venv(proj_cwd)
    print('Installing packages...')
    install_packages(proj_cwd)
    
    if yes_or_no('Set up nginx reverse proxy site? Y/N: '):
        domain_name = confirm_user_input('Enter domain name for site eg \x1b[1;37mexample.com\x1b[0m, or enter a lan address eg \x1b[1;37m192.168.1.69\x1b[0m')
        while True:
            try:
                max_body_size = int(confirm_user_input('Enter max_body_size byte integer value for uploads (leave blank for default 200M, minimum 1M)'))
                if max_body_size < 1000000:
                    print('Please enter a max size equal to or greater than 1,000,000')
                    continue
                if yes_or_no(f'max_body_size set to {max_body_size}. Proceed? Y/N: '):
                    break
            except:
                max_body_size = 200000000
                if yes_or_no(f'max_body_size set to {max_body_size}. Proceed? Y/N: '):
                    break
                
        set_cfg(domain_name, service_bind, auth_token, max_body_size)
        set_nginx_reverse_proxy(domain_name, service_bind, max_body_size, auth_token)
    
    print('Copying files...')
    copy_directory(cwd, proj_cwd, ignore_list=['requirements.txt', 'setup.py', 'test.py', 'split_timestamps.py', 'test.js', 'imgest.js', '\..*'])
    print('Creating systemd service...')
    create_systemd_service(service_name, service_user, proj_cwd)
    
    create_group(service_name)
    add_user_to_group(service_user, service_name)
    print(f'Changing directory owner to {service_user}')
    change_ownership_recursively(proj_cwd, service_user, service_name)
    
    print('Initializing service...')
    initialize_service(service_name)
    print(f"{service_name} service enabled and running.")
    deactivate_venv(proj_cwd)
    
    print('Cleaning up...')
    if os.getcwd() == cwd:
        os.chdir('..')
    shutil.rmtree(cwd)

if __name__ == "__main__":
    distribution_name = get_linux_distribution()
    if distribution_name:
        distribution_name = distribution_name.lower().strip()
        if distribution_name == 'debian' or distribution_name == 'ubuntu':
            check_root_privileges()
            main()
        else:
            print("This setup script is made for Debian or Ubuntu. If you're using something else then edit it to bring it in line with whatever you're using, or emulate it manually however you feel like.")
    else:
        print("This setup script is made for Debian or Ubuntu. If you're using something else then edit it to bring it in line with whatever you're using, or emulate it manually however you feel like.")