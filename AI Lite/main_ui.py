from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QFont,QColor
from PyQt5.QtCore import Qt, QTimer
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QLabel, QWidget
import sys
import requests
import cv2
import mediapipe as mp
import time
import math
import socket
import asyncio
from threading import Thread
import easyocr
import win32gui
import win32con



                

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi(r"AI_Lite_Updated.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.statusBar().hide()
        self.tabWidget.tabBar().hide()

        #Charge Indicators
        self.full_charge.hide()
        self.half_charge.hide()
        self.low_charge.hide()
        
        
        self.magic_hand_button.setEnabled(False)
        self.traffic_signs_button.setEnabled(False)
        self.commander_button.setEnabled(False)

        #Start timer to check connection status every 2 seconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_connections)
        self.timer.start(1000)  # 1000 milliseconds = 1 second
        self.gesture_bot_status.setText("<span style='color: #ffffff; font-weight: bold; font-size: 14px;'>Please wait a moment...</span>")
        self.gesture_botcam_status.setText("<span style='color: #ffffff; font-weight: bold; font-size: 14px;'>Please wait a moment...</span>")

        self.windows_button.hide()
        self.windows_button.clicked.connect(self.goto_welcome)
    
        
        self.select_bot.currentIndexChanged.connect(self.disableSelectOption)
        self.select_bot.currentIndexChanged.connect(self.updateHosts)
        self.select_bot.currentIndexChanged.connect(self.battery_indicator)

        #Welcome-----------
        self.bot_connect_red.hide()
        self.bot_connect_green.hide()

        self.welcome_display.setAlignment(Qt.AlignCenter)
        self.welcome_display.setText("<span style='color: #ff0000; font-weight: bold; font-size: 16px;'>Please Connect with a bot </span>")
        
        

        # self.start_cam.setEnabled(False)
        self.close_button.clicked.connect(self.close_window)
        # self.close_button_2.clicked.connect(self.close_textwindow)
        # self.close_button_4.clicked.connect(self.close_commanderwindow)
        # self.close_button_3.clicked.connect(self.close_welcomewindow)

        
    
        # # Connect button clicks to their respective functions
        # self.magic_hand_button.clicked.connect(self.enable_tab1)
        # self.traffic_signs_button.clicked.connect(self.enable_tab2)
        # self.commander_button.clicked.connect(self.enable_tab3)
        # self.magic_hand_label.setEnabled(True)  

    
        self.tabWidget.setCurrentIndex(4)
        self.tabWidget.setTabEnabled(4, True)
        self.tabWidget.setTabEnabled(2, False)
        self.tabWidget.setTabEnabled(3, False)


        
        self.close_cam.setEnabled(False)
        self.close_botcam.setEnabled(False)

        self.cam_label.setEnabled(False)
        self.botcam_label.setEnabled(False)

        self.stop_label.setEnabled(False)
        self.run_label.setEnabled(False)
        self.left_label.setEnabled(False)
        self.right_label.setEnabled(False)

        self.stop_label_icon.setEnabled(False)
        self.run_label_icon.setEnabled(False)
        self.left_label_icon.setEnabled(False)
        self.right_label_icon.setEnabled(False)

        self.stop_led_label.setEnabled(False)
        self.run_led_label.setEnabled(False)
        self.left_led_label.setEnabled(False)
        self.right_led_label.setEnabled(False)
        
        self.stop_led_label_1.setEnabled(False)
        self.run_led_label_1.setEnabled(False)
        self.left_led_label_1.setEnabled(False)
        self.right_led_label_1.setEnabled(False)


        self.start_cam.setEnabled(False)
        self.start_cam.clicked.connect(self.gesture_detection)
        #self.stop_led_label.setStyleSheet("QLabel { background-color: #00ff00; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.close_cam.clicked.connect(self.terminate_cam)
        self.close_botcam.clicked.connect(self.terminate_botcam)

        self.gesture_bot_status.setEnabled(True)
        self.gesture_botcam_status.setEnabled(True)

        self.gesture_bot_status.setAlignment(Qt.AlignCenter)
        self.gesture_botcam_status.setAlignment(Qt.AlignCenter)

        

        #--------------------------------------------------------------------------------------------------------------------------------------------
        #Traffic signs
        self.close_cam_2.setEnabled(False)
        self.close_botcam_2.setEnabled(False)

        self.cam_label_2.setEnabled(False)
        self.botcam_label_2.setEnabled(False)


        self.stop_label_icon_2.setEnabled(False)
        self.go_label_icon.setEnabled(False)
        self.left_label_icon_2.setEnabled(False)
        self.right_label_icon_2.setEnabled(False)

        
        self.start_cam_2.setEnabled(False)
        self.start_cam_2.clicked.connect(self.text_detection)
        self.close_cam_2.clicked.connect(self.terminate_cam)
        self.close_botcam_2.clicked.connect(self.terminate_botcam)
         
        self.readngo_bot_status.setEnabled(True)
        self.readngo_botcam_status.setEnabled(True)

        self.readngo_bot_status.setAlignment(Qt.AlignCenter)
        self.readngo_botcam_status.setAlignment(Qt.AlignCenter)

        # Define instance variables for camera captures
        self.cap = None
        self.cap_1 = None
        self.text_cap = None
        self.text_cap_1 = None
        # self.host_bot = "192.168.30.5"
        # self.host_cam = "192.168.30.10"
        self.host_bot = ""
        self.host_cam = ""

        

    def close_window(self):
        sys.exit(app.exec_())


    
    # def close_textwindow(self):
    #     sys.exit(app.exec_())

    # def close_welcomewindow(self):
    #     sys.exit(app.exec_())
    
    # def close_commanderwindow(self):
    #     sys.exit(app.exec_())
    
    def disableSelectOption(self, index):
        if index != 0:  # Check if an item other than "--Select--" is selected
            self.select_bot.model().item(0).setEnabled(False)
            self.select_bot.model().item(0).setForeground(QColor('gray'))


    def updateHosts(self, index):
        
        if index == 1:
            self.host_bot = "192.168.30.5"
            self.host_cam = "192.168.30.10"
        elif index == 2:
            self.host_bot = "192.168.40.4"
            self.host_cam = "192.168.40.8"
        elif index == 3:
            self.host_bot = "192.168.80.4"
            self.host_cam = "192.168.80.8"
    
    
    def goto_welcome(self):

        self.tabWidget.setCurrentWidget(self.tab_4)
        self.windows_button.hide()
        self.magic_hand_button.setStyleSheet("font: 12pt Railway;background-color:#582c74;color: rgb(255, 255, 255);border-radius: 7px;")
        self.traffic_signs_button.setStyleSheet("font: 12pt Railway;background-color:#582c74;color: rgb(255, 255, 255);border-radius: 7px;")
        self.commander_button.setStyleSheet("font: 12pt Railway;background-color:#582c74;color: rgb(255, 255, 255);border-radius: 7px;")

    def check_connections(self):
        
            bot_connected = self.check_connection(self.host_bot)
            botcam_connected = self.check_connection(self.host_cam)
            # print(self.host_bot)
            # print(self.host_cam)

            

            # bot_status = f"<span style='color: {'green' if bot_connected else 'red'}; font-weight: bold;'>Connected</span>" if bot_connected else "<span style='color: red; font-weight: bold;'>Connection Failed</span>"
            # botcam_status = f"<span style='color: {'green' if botcam_connected else 'red'}; font-weight: bold;'>Connected</span>" if botcam_connected else "<span style='color: red; font-weight: bold;'>Connection Failed</span>"

            # self.display.setText(f"<span style='color: black; font-weight: bold;'>Bot:</span> {bot_status} | <span style='color: black; font-weight: bold;'>Bot Cam:</span> {botcam_status}")

            bot_status = f"<span style='color: {'#00ff00' if bot_connected else 'red'}; font-weight: bold; font-size: 14px;'>Connected</span>" if bot_connected else "<span style='color: red; font-weight: bold; font-size: 14px;'>Connection Failed</span>"
            botcam_status = f"<span style='color: {'#00ff00' if botcam_connected else 'red'}; font-weight: bold; font-size: 14px;'>Connected</span>" if botcam_connected else "<span style='color: red; font-weight: bold; font-size: 14px;'>Connection Failed</span>"

            self.gesture_bot_status.setText(f"<span style='color: #ffffff; font-weight: bold; font-size: 14px;'>Bot:</span> {bot_status}")
            self.gesture_botcam_status.setText(f"<span style='color: #ffffff; font-weight: bold; font-size: 14px;'>Bot Cam:</span> {botcam_status}")
            
            self.readngo_bot_status.setText(f"<span style='color: #ffffff; font-weight: bold; font-size: 14px;'>Bot:</span> {bot_status}")
            self.readngo_botcam_status.setText(f"<span style='color: #ffffff; font-weight: bold; font-size: 14px;'>Bot Cam:</span> {botcam_status}")
            

            if bot_connected and botcam_connected:
                self.start_cam.setEnabled(True)
                self.start_cam_2.setEnabled(True)

                self.bot_connect_green.show()
                self.bot_connect_red.hide()


                self.magic_hand_button.setEnabled(True)
                self.traffic_signs_button.setEnabled(True)
                self.commander_button.setEnabled(True)
                # Connect button clicks to their respective functions
                self.magic_hand_button.clicked.connect(self.enable_tab1)
                self.traffic_signs_button.clicked.connect(self.enable_tab2)
                self.commander_button.clicked.connect(self.enable_tab3)
                self.welcome_display.setText(f"<span style='color: #00cb00; font-weight: bold; font-size: 16px;'>Connected to {self.select_bot.currentText()} </span>")
                
                print("Connected")
            else:
                self.start_cam.setEnabled(False)
                self.start_cam_2.setEnabled(False)

                self.bot_connect_red.show()
                self.bot_connect_green.hide()

                #self.welcome_display.setText("<span style='color: #ff0000; font-weight: bold; font-size: 16px;'>Please Connect with a bot </span>")
                if not self.select_bot.currentIndex()==0:
                    self.welcome_display.setText(f"<span style='color: #ff0000; font-weight: bold; font-size: 16px;'>{self.select_bot.currentText()} is Not Connected </span>")
                    self.magic_hand_button.setEnabled(False)
                    self.traffic_signs_button.setEnabled(False)
                    self.commander_button.setEnabled(False)

                self.magic_hand_button.setEnabled(False)
                self.traffic_signs_button.setEnabled(False)
                self.commander_button.setEnabled(False)

                self.windows_button.setEnabled(True)
                self.terminate_cam()
                self.terminate_botcam()
                print("Not Connected")
            
            # self.terminate_cam()


    def check_connection(self, host):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((host, 80))
                
                return True
        except socket.error as e:
            return False


    def enable_tab1(self):
        self.magic_hand_button.setStyleSheet("font: 12pt Railway;background-color:#ee088c;color: rgb(255, 255, 255);border-radius: 7px;")
        self.traffic_signs_button.setStyleSheet("font: 12pt Railway;background-color:#582c74;color: rgb(255, 255, 255);border-radius: 7px;")
        self.commander_button.setStyleSheet("font: 75 12pt Railway;background-color:#582c74;color: rgb(255, 255, 255);border-radius: 7px;")
        self.windows_button.show()
        self.windows_button.setEnabled(True)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget.setTabEnabled(1, True)
        self.tabWidget.setTabEnabled(2, False)
        self.tabWidget.setTabEnabled(3, False)
 
    def enable_tab2(self):
        self.magic_hand_button.setStyleSheet("font: 12pt Railway;background-color:#582c74;color: rgb(255, 255, 255);border-radius: 7px;")
        self.traffic_signs_button.setStyleSheet("font: 12pt Railway;background-color:#ee088c;color: rgb(255, 255, 255);border-radius: 7px;")
        self.commander_button.setStyleSheet("font: 75 12pt Railway;background-color:#582c74;color: rgb(255, 255, 255);border-radius: 7px;")
        self.windows_button.show()
        self.tabWidget.setCurrentIndex(2)
        self.tabWidget.setTabEnabled(1, False)
        self.tabWidget.setTabEnabled(2, True)
        self.tabWidget.setTabEnabled(3, False)
 
    def enable_tab3(self):
        self.magic_hand_button.setStyleSheet("font: 12pt Railway;background-color:#582c74;color: rgb(255, 255, 255);border-radius: 7px;")
        self.traffic_signs_button.setStyleSheet("font: 12pt Railway;background-color:#582c74;color: rgb(255, 255, 255);border-radius: 7px;")
        self.commander_button.setStyleSheet("font: 75 12pt Railway;background-color:#ee088c;color: rgb(255, 255, 255);border-radius: 7px;")
        self.windows_button.show()
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget.setTabEnabled(1, False)
        self.tabWidget.setTabEnabled(2, False)
        self.tabWidget.setTabEnabled(3, True)
    
    def battery_indicator(self):
        voltage_response = requests.get(f"http://{self.host_bot}/?cmd=V")
        print(voltage_response.text)
        voltage_text = voltage_response.text.strip()  # Remove leading/trailing spaces

        # Extracting the last part which contains the float value
        voltage_value = float(voltage_text.split()[-1])
        print(voltage_value)
            
        if voltage_value <= 3.2:
            self.low_charge.show()
            self.full_charge.hide()
            self.half_charge.hide()
        elif 3.2 <= voltage_value <= 3.6:
            self.half_charge.show()
            self.full_charge.hide()
            self.low_charge.hide()
        elif 3.6 <= voltage_value <= 4.2:
            self.full_charge.show()  # Corrected: Should be show() not call the method
            self.half_charge.hide()
            self.low_charge.hide()
        else:
            self.full_charge.hide()
            self.half_charge.hide()
            self.low_charge.hide()


    def gesture_detection(self):

        self.start_cam.setEnabled(False)

        #welcome----
        self.magic_hand_button.setEnabled(False)
        self.traffic_signs_button.setEnabled(False)
        self.commander_button.setEnabled(False)
        self.windows_button.setEnabled(False)
        

        self.tabWidget.setTabEnabled(1, True)
        self.tabWidget.setTabEnabled(2, False)
        self.tabWidget.setTabEnabled(3, False)
        self.tabWidget.setTabEnabled(4, False)


        # self.start_cam.setEnabled(True)
        self.close_cam.setEnabled(True)
        self.close_botcam.setEnabled(True)

        self.stop_label.setEnabled(True)
        self.run_label.setEnabled(True)
        self.left_label.setEnabled(True)
        self.right_label.setEnabled(True)

        self.stop_label_icon.setEnabled(True)
        self.run_label_icon.setEnabled(True)
        self.left_label_icon.setEnabled(True)
        self.right_label_icon.setEnabled(True)

        self.stop_led_label.setEnabled(True)
        self.run_led_label.setEnabled(True)
        self.left_led_label.setEnabled(True)
        self.right_led_label.setEnabled(True)
        
        self.stop_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.run_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.left_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.right_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance


        def send_string_to_ip(data_to_send):
            # Define the endpoint URL
            endpoint_url = f"http://{self.host_bot}/?cmd={data_to_send}"

            # Send a GET request with the command
            response = requests.get(endpoint_url)
            print(response)

                

        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands()
        mp_draw = mp.solutions.drawing_utils
        # global cap
        self.cap = cv2.VideoCapture(0)
        # global cap_1
        self.cap_1 = cv2.VideoCapture(f"http://{self.host_cam}:81/stream")  # Second camera stream

        hwnd=cv2.namedWindow("Hand Sign Detection",cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
        cv2.moveWindow("Hand Sign Detection",584,340)
        cv2.resizeWindow("Hand Sign Detection",500,360)
        # cv2.setMouseCallback("Hand Sign Detection", prevent_minimizing)
        cv2.setWindowProperty("Hand Sign Detection", cv2.WND_PROP_TOPMOST, 1)  # Bring window to front

        hwnd = win32gui.FindWindow(None, "Hand Sign Detection")
        

        # # Set window styles to prevent moving or minimizing
       # Get the current window styles
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        # Remove title bar and borders
        style &= ~(win32con.WS_CAPTION | win32con.WS_THICKFRAME)
        # Apply changes
        win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
        

        bwnd = cv2.namedWindow("Bot Camera Stream",cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
        cv2.moveWindow("Bot Camera Stream",1235,340)
        cv2.resizeWindow("Bot Camera Stream",500,360)
        # cv2.setMouseCallback("Bot Camera Stream", prevent_minimizing_1)
        cv2.setWindowProperty("Bot Camera Stream", cv2.WND_PROP_TOPMOST, 1)  # Bring window to front

        bwnd = win32gui.FindWindow(None, "Bot Camera Stream")

        # # Set window styles to prevent moving or minimizing
       # Get the current window styles
        style_1 = win32gui.GetWindowLong(bwnd, win32con.GWL_STYLE)
        # Remove title bar and borders
        style_1 &= ~(win32con.WS_CAPTION | win32con.WS_THICKFRAME)
        # Apply changes
        win32gui.SetWindowLong(bwnd, win32con.GWL_STYLE, style)

        finger_tips = [8, 12, 16, 20]
        thumb_tip = 4
        
        cooldown_time = 0  # Set the cooldown time in seconds
        last_detection_time = time.time()

        while True:

            self.start_cam.setEnabled(False)

            #welcome----
            self.magic_hand_button.setEnabled(False)
            self.traffic_signs_button.setEnabled(False)
            self.commander_button.setEnabled(False)

            self.tabWidget.setTabEnabled(1, True)
            self.tabWidget.setTabEnabled(2, False)
            self.tabWidget.setTabEnabled(3, False)
            self.tabWidget.setTabEnabled(4, False)

            ret, img = self.cap.read()
            if not ret:
                break
            
            img = cv2.flip(img, 1)    
            h, w, c = img.shape
            results = hands.process(img)
            ret_1, img_1 = self.cap_1.read()  # Read from the second camera stream
            

            if not ret_1:
                break
            
        
            if not results.multi_hand_landmarks:

                requests.get(f"http://{self.host_bot}/?cmd=s")
                # asyncio.run(send_command_async('s'))
                self.stop_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.left_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.run_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.right_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                
                print("STOPPED")
        
            elif results.multi_hand_landmarks:
                current_time = time.time()
                elapsed_time_since_last_detection = current_time - last_detection_time
        
                if elapsed_time_since_last_detection > cooldown_time:
                    for hand_idx, hand_landmark in enumerate(results.multi_hand_landmarks):
                        lm_list = [lm for lm in hand_landmark.landmark]
                        finger_fold_status = [lm_list[tip].y < lm_list[tip - 2].y for tip in finger_tips]
                        print(finger_fold_status)
        
        
                        if not any(finger_fold_status):  # All fingers closed
                            # "RUN" Gesture
                            cv2.putText(img, "RUN", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                            self.run_led_label.setStyleSheet("QLabel { background-color: #00ff00; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                            self.stop_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                            self.left_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                            self.right_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
            
                            
                            print("RUN")
                            
                            send_string_to_ip("f")
                            # asyncio.run(send_command_async('f'))
                            last_detection_time = time.time()  # Update the last detection time
                            #continue  # Skip other gesture checks
        
                        if all(finger_fold_status):  # All fingers open
                            # "STOP" Gesture
                            cv2.putText(img, "STOP", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                            self.stop_led_label.setStyleSheet("QLabel { background-color: #00ff00; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                            # self.left_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                            # self.run_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                            # self.right_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                            
                            print("STOP")
                            send_string_to_ip("s")
                            #asyncio.run(send_command_async('s'))
                            
                            
                            last_detection_time = time.time()  # Update the last detection time
                            # continue  # Skip other gesture checks
        
        
                        if results.multi_hand_landmarks:
                            for hand_landmarks in results.multi_hand_landmarks:
                                # Get thumb tip and base of palm positions
                                thumb_tip = hand_landmarks.landmark[4]
                                palm_base = hand_landmarks.landmark[0]
        
                                # Calculate thumb direction vector
                                thumb_direction_vector = (thumb_tip.x - palm_base.x, thumb_tip.y - palm_base.y)
        
                                # Calculate thumb direction angle (degrees)
                                thumb_direction_angle_degrees = math.degrees(math.atan2(thumb_direction_vector[1], thumb_direction_vector[0]))
                                print(thumb_direction_angle_degrees)
        
                                # Decision logic for direction detection
                                if finger_fold_status[0]:  # Thumb extended to Right, other fingers closed
                                    if not any(finger_fold_status[1:]) and -56 <= thumb_direction_angle_degrees <= 0:
                                        cv2.putText(img, "LEFT", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                                        print("LEFT")
                                        self.left_led_label.setStyleSheet("QLabel { background-color: #00ff00; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                                        self.stop_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                                        self.run_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                                        self.right_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                                        
                                        send_string_to_ip("l")
                                        #asyncio.run(send_command_async('l'))
                                        last_detection_time = time.time()
                                    
                                    if any(finger_fold_status[1:]):
                                        data = 's'
                                        requests.get(f"http://{self.host_bot}/?cmd={data}")
                                        # self.stop_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                                        self.run_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                                        self.left_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                                        self.right_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                                        
                                        #asyncio.run(send_command_async('s'))
                                        last_detection_time = time.time()

                                        
                                    if not any(finger_fold_status[1:]) and -180 <= thumb_direction_angle_degrees <= -120:
                                        cv2.putText(img, "RIGHT", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
                                        print("RIGHT")
                                        self.right_led_label.setStyleSheet("QLabel { background-color: #00ff00; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                                        self.stop_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                                        self.left_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                                        self.run_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                                        
                                        send_string_to_ip("r")
                                        #asyncio.run(send_command_async('r'))
                                        last_detection_time = time.time()
                                        
                                # elif any(finger_fold_status):
                                #     data = 's'
                                #     requests.get(f"http://192.168.30.5/?cmd={data}")
                    
                                else:
                                    print("Thumb Direction: Undefined")
                        
                        # If none of the defined gestures are detected, print "STOP"
                        if any(finger_fold_status) and not all(finger_fold_status) and not finger_fold_status[0]:
                            
                            send_string_to_ip("s")
                            #asyncio.run(send_command_async('s'))
                            self.stop_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                            self.left_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                            self.run_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                            self.right_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                            
                            last_detection_time = time.time()
                        
                            
        
                        # Optional visualization: draw arrow based on direction
                        cv2.arrowedLine(img, (int(palm_base.x * img.shape[1]), int(palm_base.y * img.shape[0])),
                                    (int(thumb_tip.x * img.shape[1]), int(thumb_tip.y * img.shape[0])),
                                    (0, 255, 0) if 0 <= thumb_direction_angle_degrees <= -56 else
                                    (255, 0, 0) if -180 <= thumb_direction_angle_degrees <= -120 else
                                    (0, 0, 255), 2)
                                        
                                        
                        mp_draw.draw_landmarks(img, hand_landmark,
                                            mp_hands.HAND_CONNECTIONS,
                                            mp_draw.DrawingSpec((0, 0, 255), 6, 3),
                                            mp_draw.DrawingSpec((0, 255, 0), 4, 2)
                                            )
            
             # Display the second camera stream
            cv2.imshow("Bot Camera Stream", img_1)
            cv2.imshow("Hand Sign Detection", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                send_string_to_ip("s")
                #asyncio.run(send_command_async('s'))
                break
        
        self.terminate_cam()
        self.terminate_botcam()
    
    #----------------------------
        
    
    def text_detection(self):

        # self.host_bot = "192.168.30.5"
        # self.host_cam = "192.168.30.10"

        self.start_cam_2.setEnabled(False)

        self.close_cam_2.setEnabled(True)
        self.close_botcam_2.setEnabled(True)

        self.cam_label_2.setEnabled(True)
        self.botcam_label_2.setEnabled(True)

        #welcome----
        self.magic_hand_button.setEnabled(False)
        self.traffic_signs_button.setEnabled(False)
        self.commander_button.setEnabled(False)
        self.windows_button.setEnabled(False)
        

        self.tabWidget.setTabEnabled(1, False)
        self.tabWidget.setTabEnabled(2, True)
        self.tabWidget.setTabEnabled(3, False)
        self.tabWidget.setTabEnabled(4, False)


        self.stop_label_icon_2.setEnabled(True)
        self.go_label_icon.setEnabled(True)
        self.left_label_icon_2.setEnabled(True)
        self.right_label_icon_2.setEnabled(True)
        
        self.stop_led_label_1.setEnabled(True)
        self.run_led_label_1.setEnabled(True)
        self.left_led_label_1.setEnabled(True)
        self.right_led_label_1.setEnabled(True)
        
        self.stop_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.run_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.left_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.right_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance

        
        # Initialize the OCR reader
        reader = easyocr.Reader(['en'], gpu=False)


        # Function to send a string to the specified IP
        def send_string_to_ip(data_to_send):
            # Check if the data to send is "stop" or "go"
            if data_to_send.lower() == "stop" or all(char in data_to_send.lower() for char in ["s", "t", "o", "p"]):
                # If it is "stop", set the command to "S"
                requests.get(f"http://{self.host_bot}/?cmd=s")
                self.left_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.stop_led_label_1.setStyleSheet("QLabel { background-color: #00ff00; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.run_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.right_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                


            elif data_to_send.lower() == "go" or all(char in data_to_send.lower() for char in ["g", "o"]):
                # If it is "go", set the command to "F"
                requests.get(f"http://{self.host_bot}/?cmd=f")
                self.left_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.stop_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.run_led_label_1.setStyleSheet("QLabel { background-color: #00ff00; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.right_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance



            elif data_to_send.lower() == "turn right" or data_to_send.lower() == "right" or all(char in data_to_send.lower() for char in ["r", "i", "g", "h", "t"]):
                # If it is "go", set the command to "F"
                requests.get(f"http://{self.host_bot}/?cmd=r(600)")
                self.left_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.stop_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.run_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.right_led_label_1.setStyleSheet("QLabel { background-color: #00ff00; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                


            elif data_to_send.lower() == "turn left" or data_to_send.lower() == "left" or all(char in data_to_send.lower() for char in ["l", "e", "f", "t"]):
                # If it is "go", set the command to "F"
                requests.get(f"http://{self.host_bot}/?cmd=l(600)")
                self.left_led_label_1.setStyleSheet("QLabel { background-color: #00ff00; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.stop_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.run_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.right_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                
                # time.sleep(0.6)
                # requests.get(f"http://{host_bot}/?cmd=s")

            else:
                # Otherwise, use the provided data_to_send as the command
                requests.get(f"http://{self.host_bot}/?cmd=s")
                self.stop_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.left_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.run_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
                self.right_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance



        # Function to send a string to the specified IP
        # async def send_command_async(data_to_send):
        #     try:
        #         # Define the endpoint URL
        #         # endpoint_url = f"http://192.168.30.5/?cmd={data_to_send}"
        #         response = await asyncio.to_thread(requests.get(f"http://192.168.30.5/?cmd={data_to_send}"))

        #         if response.status_code == 200:
        #             print(f"Command '{data_to_send}' sent to AI-Lite server.")
        #         else:
        #             print(f"Failed to send command. HTTP Status Code: {response.status_code}")
        #     except requests.RequestException as e:
        #         print(f"command sent to server")
                


        # Open the BOT cam
        self.text_cap = cv2.VideoCapture(0)
        self.text_cap_1 = cv2.VideoCapture(f"http://{self.host_cam}:81/stream")

        ownd = cv2.namedWindow("OCR",cv2.WINDOW_NORMAL)
        cv2.moveWindow("OCR",584,342)
        cv2.resizeWindow("OCR",500,360)
        # cv2.setMouseCallback("Hand Sign Detection", prevent_minimizing)
        cv2.setWindowProperty("OCR", cv2.WND_PROP_TOPMOST, 1)  # Bring window to front

        ownd = win32gui.FindWindow(None, "OCR")

        # # Set window styles to prevent moving or minimizing
       # Get the current window styles
        style = win32gui.GetWindowLong(ownd, win32con.GWL_STYLE)
        # Remove title bar and borders
        style &= ~(win32con.WS_CAPTION | win32con.WS_THICKFRAME)
        # Apply changes
        win32gui.SetWindowLong(ownd, win32con.GWL_STYLE, style)


        ob_wnd = cv2.namedWindow("OCR Bot Camera Stream",cv2.WINDOW_NORMAL)
        cv2.moveWindow("OCR Bot Camera Stream",1235,342)
        cv2.resizeWindow("OCR Bot Camera Stream",500,360)
        # cv2.setMouseCallback("Bot Camera Stream", prevent_minimizing_1)
        cv2.setWindowProperty("OCR Bot Camera Stream", cv2.WND_PROP_TOPMOST, 1)  # Bring window to front

        ob_wnd = win32gui.FindWindow(None, "OCR Bot Camera Stream")

        # # Set window styles to prevent moving or minimizing
       # Get the current window styles
        style = win32gui.GetWindowLong(ob_wnd, win32con.GWL_STYLE)
        # Remove title bar and borders
        style &= ~(win32con.WS_CAPTION | win32con.WS_THICKFRAME)
        # Apply changes
        win32gui.SetWindowLong(ob_wnd, win32con.GWL_STYLE, style)
        

        while True:

            self.start_cam_2.setEnabled(False)
            #welcome----
            self.magic_hand_button.setEnabled(False)
            self.traffic_signs_button.setEnabled(False)
            self.commander_button.setEnabled(False)

            self.tabWidget.setTabEnabled(1, False)
            self.tabWidget.setTabEnabled(2, True)
            self.tabWidget.setTabEnabled(3, False)
            self.tabWidget.setTabEnabled(4, False)


            # Capture frame-by-frame
            ret, frame = self.text_cap.read()
            if not ret:
                break

            # Perform OCR on the frame
            result = reader.readtext(frame)

            ret_1, frame_1 = self.text_cap_1.read()
            if not ret_1:
                break

            # Extract the recognized text
            if result:
                text = result[0][1]
            else:
                text = "No text detected"

            send_string_to_ip(text)
            

            # Display the recognized text
            cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # Display the second camera stream
            cv2.imshow("OCR Bot Camera Stream", frame_1)
            cv2.imshow('OCR', frame)

            # Check for 'q' key to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                requests.get(f"http://{self.host_bot}/?cmd=s")
                break

        # Release the capture and close all windows
        self.terminate_cam()
        self.terminate_botcam()
#-----------------------------------------------------------------------------------------------------------------------------
    
    def terminate_cam(self):

        self.stop_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.run_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.left_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.right_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance

        self.stop_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.run_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.left_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.right_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance


        self.start_cam.setEnabled(True)

        self.close_cam.setEnabled(False)
        self.close_botcam.setEnabled(False)

        self.cam_label.setEnabled(False)
        self.botcam_label.setEnabled(False)

        self.stop_label.setEnabled(False)
        self.run_label.setEnabled(False)
        self.left_label.setEnabled(False)
        self.right_label.setEnabled(False)

        self.stop_label_icon.setEnabled(False)
        self.run_label_icon.setEnabled(False)
        self.left_label_icon.setEnabled(False)
        self.right_label_icon.setEnabled(False)
        self.close_cam_2.setEnabled(False)
        self.close_botcam_2.setEnabled(False)

        self.cam_label_2.setEnabled(False)
        self.botcam_label_2.setEnabled(False)


        self.stop_label_icon_2.setEnabled(False)
        self.go_label_icon.setEnabled(False)
        self.left_label_icon_2.setEnabled(False)
        self.right_label_icon_2.setEnabled(False)

        self.magic_hand_button.setEnabled(True)
        self.traffic_signs_button.setEnabled(True)
        self.commander_button.setEnabled(True)
        self.windows_button.setEnabled(True)

        self.tabWidget.setTabEnabled(4, True)

        if self.text_cap is not None:
            self.text_cap.release()
        cv2.destroyAllWindows()
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()
    
    def terminate_botcam(self):

        self.stop_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.run_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.left_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.right_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance

        self.stop_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.run_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.left_led_label.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance
        self.right_led_label_1.setStyleSheet("QLabel { background-color: #ffffff; border-radius: 10px; border: 2px solid black; }")  # Set LED appearance


        self.start_cam.setEnabled(True)

        self.close_cam.setEnabled(False)
        self.close_botcam.setEnabled(False)

        self.cam_label.setEnabled(False)
        self.botcam_label.setEnabled(False)

        self.stop_label.setEnabled(False)
        self.run_label.setEnabled(False)
        self.left_label.setEnabled(False)
        self.right_label.setEnabled(False)

        self.stop_label_icon.setEnabled(False)
        self.run_label_icon.setEnabled(False)
        self.left_label_icon.setEnabled(False)
        self.right_label_icon.setEnabled(False)
        self.close_cam_2.setEnabled(False)
        self.close_botcam_2.setEnabled(False)

        self.cam_label_2.setEnabled(False)
        self.botcam_label_2.setEnabled(False)


        self.stop_label_icon_2.setEnabled(False)
        self.go_label_icon.setEnabled(False)
        self.left_label_icon_2.setEnabled(False)
        self.right_label_icon_2.setEnabled(False)

        self.magic_hand_button.setEnabled(True)
        self.traffic_signs_button.setEnabled(True)
        self.commander_button.setEnabled(True)
        self.windows_button.setEnabled(True)

        if self.text_cap_1 is not None:
            self.text_cap_1.release()
        cv2.destroyAllWindows()
        if self.cap_1 is not None:
            self.cap_1.release()
        cv2.destroyAllWindows()

    
    def closeEvent(self, event):
        
        self.terminate_cam()
        self.terminate_botcam()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
