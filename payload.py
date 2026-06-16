import os
import subprocess

result = subprocess.run(
    ["powershell", "-Command",
     "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8;"
     "[Environment]::GetFolderPath('Desktop')"],
    capture_output=True,
    encoding="utf-8"
)
desktop = result.stdout.strip() or os.path.expanduser("~")
txt_path = os.path.join(desktop, "pwned.txt")

with open(txt_path, "w") as f:
    f.write("You have been pwned!\n")
    f.write("This file was created by a hidden payload embedded in an image.\n")
    f.write("Technique used: LSB Steganography\n")

subprocess.Popen([
    "powershell", "-WindowStyle", "Hidden", "-Command",
    "Add-Type -AssemblyName PresentationFramework;"
    "[System.Windows.MessageBox]::Show("
    "'Payload executed successfully! A file has been created on your Desktop: pwned.txt',"
    "'System Alert')"
])
