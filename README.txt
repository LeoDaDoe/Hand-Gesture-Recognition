Scripts:
 • detectionWorker.py - Contains the class that's resposible for performing object detections
 • microcontrollerInterface.py - Contains the class that's responsible for communicating with the microcontroller
 • modelLoader.py - Contains the class that's responsible for loading the model
 • startApp.py - Contains the logic for the UI elements
 • test_UART.py - Script for testing the communication port
 • util.py - Containts the method for displaying messages

Folders:
 • UI - Contains the design files for the UI
 • Resources - Contains images and GIF files
 • hand_detection_model - Contains the exported hand detection model
 • dist/Hand_Detection_Interface - Contains the compiled application
 • confusionMatrix/dataset - Contains the dataset which was used to test the accuracy of the model

Steps to launch the application:
 1. Install GIT LFS
 2. Execute the command "git lfc clone https://github.com/LeoDaDoe/Hand-Gesture-Recognition" in the repository where you'd store the project
 3. Navigate to the folder "dist/Hand_Detection_Interface"
 4. Run the "Hand_Detection_Interface.exe" executable

Notes:
The model sometimes has issues with lighting;
To install the required libraries to run the source code you need to run the command "pip install -r requirements.txt"
