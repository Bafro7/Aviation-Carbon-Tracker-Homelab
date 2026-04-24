# Aviation-Carbon-Tracker-Homelab
"A real-time data pipeline and analytics dashboard hosted on a Windows Server/Active Directory environment."
Overview

This project is a live tracking system for 61+ high-profile aircrafts. It ingests data from the OpenSky Network API, processes it through a Python pipeline, and stores it in a MySQL database hosted on a Windows Server VM.
Tech Stack

    Backend: Python (Flask), MySQL

    Infrastructure: Windows Server 2022, Active Directory, VirtualBox

    Frontend: JavaScript (Leaflet.js), HTML5, CSS3

    Automation: Windows Task Scheduler

The Math

The system calculates carbon emissions in real-time based on the following formula:
Carbonlbs​=Distance (miles)×Fuel Burn (gal/mile)×21.1

Infrastructure Detail

Unlike a standard web app, this is hosted in a Bridged Networking environment within a homelab.

    Active Directory: Integrated domain services for server management.

    Networking: Configured static IPs and firewall rules to allow mobile access on the local network.
