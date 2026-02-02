# **YTIG (YouTube & Instagram Controller)**

## **1. Overview**

**YTIG** is a computer vision–based automation application that allows users to control YouTube and Instagram using **hand gestures**, combined with a **smart time-limit system**.

The system uses a webcam to detect hand movements in real time and translates specific gestures into keyboard actions such as scrolling or closing a tab. A built-in timer restricts usage of YouTube and Instagram by automatically closing the active tab when the allotted time expires.

The application is built using:

* **FastAPI** — Web interface & video streaming
* **OpenCV** — Real-time camera processing
* **MediaPipe Hands** — Hand landmark detection
* **PyAutoGUI** — Automated keyboard control
* **OS Window Detection** — Identifies active browser and tab

---

## **2. Purpose of the Application**

YTIG is designed for:

* Reducing excessive screen time on social media
* Helping users stay focused
* Hands-free browsing control
* Parental control or self-discipline tool
* Accessibility aid for users who prefer gesture-based control

---

## **3. Key Features**

### **Gesture-Based Controls**

When YouTube or Instagram is active in a supported browser, the following gestures are recognized:

| Hand Gesture        | Action            |
| ------------------- | ----------------- |
| Index finger up     | Scroll Down       |
| Middle finger up    | Scroll Up         |
| All five fingers up | Close current tab |

The system detects the closest hand to the center of the camera frame and tracks it for gesture recognition.

---

### **Smart Timer (App-Limited Time Control)**

The timer has a special behavior:

* Starts when the user sets a time limit
* **Counts down ONLY when YouTube or Instagram is active**
* **Pauses automatically** when the user switches to another app
* Resumes when the user returns to YouTube/Instagram
* When time reaches zero → the active tab is automatically closed

This ensures time is spent only while actually using the platforms.

---

## **4. System Architecture**

The application follows this structure:

```
Web Browser (User Interface)
        |
        v
FastAPI Server (Python Backend)
        |
        v
OpenCV + MediaPipe (Hand Detection)
        |
        v
PyAutoGUI (Keyboard Automation)
        |
        v
Operating System (Active Window Detection)
```

---

## **5. How It Works**

### Step 1 — Camera Input

The webcam continuously captures frames using OpenCV.

### Step 2 — Hand Detection

MediaPipe detects hand landmarks in each frame.

### Step 3 — Gesture Recognition

Specific landmark positions determine which fingers are raised.

### Step 4 — Window Detection

The app checks whether the user is currently on YouTube or Instagram.

### Step 5 — Action Execution

If a valid gesture is detected while on IG/YT, a keyboard command is triggered.

### Step 6 — Timer Control

The smart timer updates in the background and closes the tab when time expires.

---

## **6. Web Interface**

The user interacts with the system via a simple web page that provides:

* Input field to set minutes
* Start button
* Live camera feed
* Gesture instructions

---

## **7. Technical Components Used**

| Component       | Role                      |
| --------------- | ------------------------- |
| FastAPI         | Backend server            |
| OpenCV          | Video capture & display   |
| MediaPipe       | Hand tracking             |
| PyAutoGUI       | Simulating keyboard input |
| Jinja2          | HTML template rendering   |
| OS Window Utils | Detect active tab         |

---

## **8. Limitations**

* Requires a webcam
* Works only with supported browsers in `BROWSERS` list
* Needs sufficient lighting for hand detection
* Gesture accuracy depends on camera quality
* Cannot run inside a browser alone (needs local Python server)

---

## **9. Future Improvements**

Possible enhancements include:

* Adding voice control
* Mobile app version
* Browser extension interface
* Progress bar for timer
* Audio alert when time is nearly up
* Customizable gestures
* Support for TikTok and Facebook

---

## **10. Conclusion**

YTIG is an innovative hands-free browsing controller that combines computer vision with productivity management. By integrating gesture control with a smart time limiter, it provides a modern solution for mindful social media usage.