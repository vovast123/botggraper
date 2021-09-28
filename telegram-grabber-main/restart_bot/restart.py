import subprocess


class Commands:
    def command_execution(self):
        subprocess.run(['pkill', '-f', 'bot_grabber.py'])
        subprocess.Popen(['nohup', 'python3', '-u', '../python_bot/bot_grabber.py', '&'])
        return 'Выполнен рестарт сессии.'
