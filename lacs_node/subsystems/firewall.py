import subprocess
import syslog

class UFWManager:
    def __init__(self):
        pass

    def add_ip_to_ufw(self, ip_addr, hours_until_removal):
        try:
            result = subprocess.run(f"ufw allow from {ip_addr}", shell=True, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            syslog.syslog(syslog.LOG_ALERT, f"UFW allow command failed with: {e.output}")
            return
        
        syslog.syslog(syslog.LOG_INFO, "ADDED firewall rule to allow from " + ip_addr)

        try:
            subprocess.run(f'echo "ufw delete allow from {ip_addr}" | at now +{hours_until_removal} hours', shell=True, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            syslog.syslog(syslog.LOG_ALERT, f"Scheduling the UFW rule removal using 'at' failed: {e.output}")