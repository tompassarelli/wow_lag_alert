# WOW Lag Alert Installation Instructions
## Demo

[![Watch the video](https://img.youtube.com/vi/OUwaCl__e88/0.jpg)](https://www.youtube.com/watch?v=OUwaCl__e88)

## To install:

1. **Download the latest version of Python**
   - Visit [Python.org](https://www.python.org/downloads/) and download the latest version of Python.

2. **Download this project**
   - Navigate to the GitHub repository.
   - Click on the "Code" tab and then select "Download ZIP" (the last option).

3. **Install the project dependencies**
   - Extract the ZIP file to your desired directory.
   - Open the folder, right-click in the folder while holding the `Shift` key, and select "Open PowerShell window here" or "Open command window here".
   - In the terminal, input the following command and hit enter:
     ```
     py -m pip install -r requirements.txt
     ```

4. **Run the application**
   - After the dependencies are installed, you can run the application using:
     ```
     py wow_lag_alert.py
     ```
   - You will be prompted to configure the application settings:
     - **Threshold**: `250` is a conservative threshold value.
     - **Server Selection**: Choose "Defias Pillager" for US Central or "Skull Rock" for US West.
     - If you need to change your configuration later, you can directly edit the "config" file

Enjoy monitoring your WOW server latency with ease!
