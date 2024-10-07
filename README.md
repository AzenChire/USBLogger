# USBLogger

**USBLogger** is a Python-based tool that monitors USB device connections and disconnections, logging details such as event time, device name, serial number, and connection duration in a formatted HTML file. It features a dark mode toggle for easy readability of the logs.

## Features

- **USB Connection/Disconnection Detection**: Logs both insertion and removal events for USB devices.
- **HTML Log Generation**: Automatically creates an HTML file with the following details:
  - **Date and Time** of the event
  - **Event Type** (Connection/Disconnection)
  - **Volume Name** (USB drive label)
  - **Serial Number** of the device
  - **Connection Duration** (in seconds) for disconnection events
- **Dark Mode**: The HTML log includes a toggle to switch between light and dark themes for better readability.

## Installation

1. **Download the `.exe` file**: USBLogger has been converted to an executable, so there is no need to install Python or other dependencies on the target machine.
2. **Run the `.exe`**: Once executed, the tool will automatically start monitoring USB connections in the background.

### Requirements

- Windows 10 or higher.
- Administrator privileges may be required for USB detection.
- The executable file creates a folder in the user's `Documents` directory where logs are stored.

## How It Works

1. **USB Monitoring**: 
   - The tool continuously monitors USB ports for device connections and disconnections using WMI (Windows Management Instrumentation).
   - Each time a USB device is connected or removed, the tool logs the event with its timestamp, volume name, serial number, and connection duration (for removals).

2. **Log Output**:
   - The HTML log file (`Logs USB.html`) is generated in the `Documents/USBLogger` folder.
   - The file is automatically updated each time a new event is detected.
   - The log file also includes a button to toggle between light and dark modes.
