#!/bin/python3.8
#-*- coding:utf-8 -*-

class chiropractic(Exception):
    def __init__(self):
        import cv2
        import mediapipe
        import numpy
        self.thread = []
        self.ext = False

        # Get Preset

        self.opencv = cv2
        mp_drawing = mediapipe.solutions.drawing_utils
        mp_drawing_styles = mediapipe.solutions.drawing_styles
        mp_pose = mediapipe.solutions.pose
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing_style_dot = mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2)
        self.mp_drawing_style_line = mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2)
        self.mp_drawing_style_dot_Wrong = mp_drawing.DrawingSpec(color=(100,100,100), thickness=2, circle_radius=2)
        self.mp_drawing_style_line_Wrong = mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
        self.mp_drawing_style_dot_Right = mp_drawing.DrawingSpec(color=(100,100,0), thickness=2, circle_radius=2)
        self.mp_drawing_style_line_Right = mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2)
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def start(self): # Open Thread
        from threading import Thread
        cap = Thread(target=self.capture)
        cap.start()
        self.thread.append(cap)
        assistant = Thread(target=self.assistant)
        assistant.start()
        self.thread.append(cap)

        while True: # Check exit key
            if self.cv2.waitKey(5) & 0xFF == 27: 
                self.ext = True
                for i in self.thread:
                    i.join()
                break
            
        

    def capture(self):
        while True:
            if self.ext == True: break
            cap = self.cv2.VideoCapture(0)
            self.success, self.image = cap.read()
    
    def assistant(self):
        while True:
            if self.ext == True: break
            image = self.image
            image, results = self.getpose(image) # Get pose result
            landmarks = results.pose_landmarks.landmark # Get landmark
            try:
                image = self.posecheck(landmarks=landmarks) # Check the Pose (Caculate)
            except:
                print("Something Went Wrong!! (ON POSECHECK)")
                self.cv2.putText(image, "Something went wrong", (50, 100), self.font, 1, (0,0,255),2)
            self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS, self.mp_drawing_style_dot, self.mp_drawing_style_line)
            self.cv2.imshow('Chiropractic assistant', image)

            if self.cv2.waitKey(5) & 0xFF == 27: 
                self.ext = True
                break
        

    def posecheck(self, landmarks, image):
            # Calculate inclination of shoulder and that of hip
            Inclination_SHOULDER = (landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y - landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y) / (landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x - landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x)
            # Caculate HIP
            Inclination_HIP = (landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y - landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y) / (landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x - landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x)

            # Consider if it is correct pose or not
            if Inclination_SHOULDER <= 0.06 and Inclination_SHOULDER >= -0.06 and Inclination_HIP <= 0.06 and Inclination_HIP >= -0.06:
                mp_drawing_style_dot = self.mp_drawing_style_dot_Right
                mp_drawing_style_line = self.mp_drawing_style_line_Right
                self.cv2.putText(image, "GOOD Pose! :)", (50, 100), self.font, 1, (0,255,0),2)
                print("GOOD Pose! :)")
            else:
                mp_drawing_style_dot = self.mp_drawing_style_dot_Wrong
                mp_drawing_style_line = self.mp_drawing_style_line_Wrong
                self.cv2.putText(image, "Bad Pose!!! :(", (50, 100), self.font, 1, (0,0,255),2)
                print("Bad Pose!!! :(")

            return image
            pass
        

    def getpose(self, image):
        image.flags.writeable = False
        image = self.cv2.cvtColor(image, self.cv2.COLOR_BGR2RGB)
        results = self.pose.process(image) # pose process
        image.flags.writeable = True
        image = self.cv2.cvtColor(image, self.cv2.COLOR_RGB2BGR)
        return image, results


if __name__ == "__MAIN__":
    chiropractic = chiropractic()
    chiropractic.start()