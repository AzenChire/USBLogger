from datetime import datetime
import wmi
import time
import os
import pathlib

usb_connect_time = None
directory_folder = pathlib.Path.home() / "Documents" / "USBLogger"
html_file_path = "Logs USB.html"
css_file_path = "styles.css"

def initialize_html_file():

    # Créer le dossier "USBLogger" dans "Documents" s'il n'éxiste pas
    if not os.path.exists(directory_folder):
        os.makedirs(directory_folder)
        os.chdir(directory_folder)
    else:
        os.chdir(directory_folder)

    # Créer le fichier HTML s'il n'existe pas
    if not os.path.exists(html_file_path):
        with open(html_file_path, "w") as f:
            f.write("""<html>
<head>
<link rel="stylesheet" href="styles.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>
</head>
<body>
<div class="header">
    <h2 class="title">Logs USB</h2>
    <button onclick="toggleTheme()" id="theme-toggle">
        <i class="fas fa-sun" id="theme-icon"></i>
    </button>
</div>
<script>
function toggleTheme() {
    var body = document.body;
    var icon = document.getElementById("theme-icon");
    body.classList.toggle("dark-mode");  // Ajoute ou retire la classe "dark-mode"
    
    // Changer l'icône en fonction du mode
    if (body.classList.contains("dark-mode")) {
        icon.classList.remove("fa-sun");
        icon.classList.add("fa-moon");
    } else {
        icon.classList.remove("fa-moon");
        icon.classList.add("fa-sun");
    }
}
</script>
<table>
<tr><th>Date et heure</th><th>Événement</th><th>Nom du volume</th><th>Numéro de série</th><th>Durée de connexion (sec)</th></tr>""")

def initialize_css_file():
    # Créer le fichier HTML s'il n'existe pas
    if not os.path.exists(css_file_path):
        with open(css_file_path, "w") as f:
            f.write("""
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 100px;
    margin-bottom: 10px;
    margin-top: 20px;
}

.title {
    margin: 0;
}

body { 
    font-family: Arial, sans-serif; 
    transition: background-color 0.3s, color 0.3s; 
    background-color: #ffffff; /* Fond clair */
    color: #000000; /* Texte sombre */
}
table { 
    width: 100%; 
    border-collapse: collapse; 
}
table, th, td { 
    border: 1px solid #000000; /* Bordure noire pour le mode clair */
    padding: 8px; 
}
th { 
    background-color: #f2f2f2; /* Couleur d'en-tête pour le mode clair */
}

/* Styles pour le mode sombre */
body.dark-mode { 
    background-color: #121212; /* Fond sombre */
    color: #ffffff; /* Texte clair */
}
body.dark-mode table, 
body.dark-mode th, 
body.dark-mode td { 
    border-color: #444444; /* Bordure grise pour le mode sombre */
}
body.dark-mode th { 
    background-color: #333333; /* Couleur d'en-tête pour le mode sombre */
    color: #ffffff /* Texte clair pour les en-têtes en mode sombre */
}
body.dark-mode td {
    background-color: #1e1e1e; /* Fond des cellules pour le mode sombre */
    color: #ffffff; /* Texte clair pour les cellules en mode sombre */
}

/* Styles pour le mode clair */
body td, 
body th {
    color: #000000; /* Texte sombre pour les cellules et les en-têtes en mode clair */
}

#theme-toggle {
    background: none;
    border: none;
    font-size: 24px; /* Ajuste la taille de l'icône */
    cursor: pointer;
    margin-bottom: 10px; /* Espace en bas du bouton */
    transition: color 0.3s;
}

body.dark-mode #theme-toggle {
    color: #ffffff; /* Couleur d'icône en mode sombre */
}

body #theme-toggle {
    color: #000000; /* Couleur d'icône en mode clair */
}""")

def log_usb_event(event_type, volume_name="Inconnu", serial_number="Inconnu", duration=None):
    # Initialiser le fichier HTML si nécessaire
    initialize_html_file()
    initialize_css_file()

    # Ajouter une ligne au fichier HTML
    log_time = datetime.now().strftime("%d-%m-%Y - %H:%M:%S")
    with open(html_file_path, "a") as f:
        if duration is not None:
            f.write(f"<tr><td>{log_time}</td><td>{event_type}</td><td>{volume_name}</td><td>{serial_number}</td><td>{duration}</td></tr>\n")
        else:
            f.write(f"<tr><td>{log_time}</td><td>{event_type}</td><td>{volume_name}</td><td>{serial_number}</td><td>-</td></tr>\n")

def get_device_info(instance):
    try:
        serial_number = instance.PNPDeviceID.split("\\")[-1]  # Numéro de série

        # Utilisation de Win32_DiskDrive pour récupérer les informations du fabricant
        c = wmi.WMI()
        for drive in c.Win32_DiskDrive():
            if serial_number in drive.PNPDeviceID:
                return serial_number
        return serial_number
    except AttributeError:
        return "Inconnu"

def get_volume_name():
    c = wmi.WMI()
    for disk in c.Win32_LogicalDisk(DriveType = 2):  # DriveType 2 correspond aux clés USB
        if disk.VolumeName:
            return disk.VolumeName
    return "Inconnu"

def monitor_usb():
    global usb_connect_time
    c = wmi.WMI()

    # Surveillance des événements de connexion de périphérique USB
    watcher_in = c.watch_for(notification_type = "Creation", wmi_class="Win32_USBHub")
    # Surveillance des événements de déconnexion de périphérique USB
    watcher_out = c.watch_for(notification_type = "Deletion", wmi_class="Win32_USBHub")

    while True:
        try:
            # Vérifier les connexions USB
            usb_device_in = watcher_in()
            serial_in = get_device_info(usb_device_in)
            volume_name_in = get_volume_name()  # Récupérer le nom du volume
            usb_connect_time = datetime.now()  # Enregistrer l'heure de connexion
            log_usb_event("Connexion", volume_name_in, serial_in)
            print(f"Clé USB connectée: {volume_name_in} - {serial_in}")
            
            # Vérifier les déconnexions USB
            usb_device_out = watcher_out()
            serial_out = get_device_info(usb_device_out)
            usb_disconnect_time = datetime.now()
            connection_duration = (usb_disconnect_time - usb_connect_time).total_seconds()  # Calculer la durée
            log_usb_event("Déconnexion", volume_name_in, serial_out, duration = int(connection_duration))
            print(f"Clé USB déconnectée: {volume_name_in} - {serial_out} | Durée : {int(connection_duration)} sec")
        
        except Exception as e:
            print(f"Erreur: {e}")
            time.sleep(1)

if __name__ == "__main__":
    print("Détection des clés USB...")
    monitor_usb()