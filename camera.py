import cv2
import time
from threading import Thread

class Camera:
    def __init__(self, name:str = "output", width:int = 640, height:int = 480, fps:int = 20.0):
        """Constructor for the camera class

        Args:
            name (str, optional): Name given to the camera. Defaults to "output".
            width (int, optional): Width of the video capture. Defaults to 1280.
            height (int, optional): Height of the video capture. Defaults to 720.
            fps (float, optional): Framerate of the video capture. Defaults to 20.0.
        
        Other Attributes:
            cap (VideoCapture): To be used later to hold an instance of the VideoCapture object
            out (VideoWriter): To be used later to hold an instance of the VideoWriter object         
            fileIndex (int): Indicates file number of video capture. Initialized to 0. 
            recordStatus (bool): Indicates whether camera is on or off. Initialized to False          
        """
        self.name = name
        self.width = width
        self.height = height
        self.fps = fps
        self.cap = None
        self.out = None
        self.fileIndex = 0
        self.recordStatus = False

        self._initialize_camera()

    def _set_file(self) -> str:
        """Sets file name; increases every time function is called (i.e. a new video is recorded)
        
        Returns:
            filename (str): Name of the video capture file
        """
        filename = f"{self.name}_{self.fileIndex}.mp4"
        self.fileIndex += 1
        return filename

    def _initialize_camera(self) -> cv2.VideoCapture:
        """Creates the VideoCapture object

        Returns:
            VideoCapture: OpenCV object that captures videos
        """
        self.cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        return self.cap

    def _get_video_writer(self, filename: str) -> cv2.VideoWriter:
        """Creates and returns the VideoWriter object

        Args:
            filename (str): File that the video will be stored in

        Returns:
            VideoWriter: OpenCV object that writes the captured frames to a 
                         video file.
        """
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(filename, fourcc, self.fps, (self.width, self.height))
        return self.out

    def record(self, filename: str):
        """Starts video capture; user presses 'q' to stop recording
        
        Args:
            filename (str): File that the video will be stored in
        """

        #TODO: figure out how to open camera faster
        # self._initialize_camera()
        if not self.cap or not self.cap.isOpened():
            print("Error: Could not open webcam.")
            return

        self._get_video_writer(filename)

        self.recordStatus = True

        print("Recording for 15 seconds...")
        start_time = time.time()
        while time.time() - start_time < 15:  # Record for 15 seconds
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            self.out.write(frame)

        self.stop_recording()
    
    def create_record_thread(self):
        """Creates thread which handles recording"""

        fileName = self._set_file()

        cameraThread = Thread(
            target = self.record,
            args = (fileName, )
        )

        cameraThread.start()

    def stop_recording(self):
        """Closes the video file and capturing device"""

        if self.cap:
            self.cap.release()
        if self.out:
            self.out.release()
        cv2.destroyAllWindows()

        print("Recording stopped...")
        time.sleep(1)

    def __eq__(self, other) -> bool:
        """Checks to see if Camera objects have the same name.
        Meant to prevent files being overwritten if using more than one camera

        Args:
            other (Camera): Camera that is being compared to

        Returns:
            bool: Returns True if Camera objects have the same name, False otherwise
        """
        if not isinstance(other, Camera):
            raise TypeError
        return self.name == other.name

quitApp = False
recording = False

def getUserInput():
    global quitApp, recording

    while(1):
        userInput = input("Enter 'stop' to stop program, 'camera' to start recording: ").strip().lower()
        if userInput == 'stop':
            quitApp = True
        elif userInput == 'camera':
            recording = not recording

# if __name__ == "__main__":
#     cam = Camera()

#     inputTask = Thread(
#         target = getUserInput
#         )
#     inputTask.start()

#     while not quitApp:
#         if recording and not cam.recordStatus:
#             cam.create_record_thread()
#         elif not recording and cam.recordStatus:
#             cam.stop_recording()
#         time.sleep(0.1)

#     if cam.recordStatus:
#         cam.stop_recording()

#     inputTask.join()
#     print("Program terminated.")

if __name__ == "__main__":
    print("Initializing hardware...")
    cam = Camera("test")

    cam.record(cam._set_file())




# # Actual Controls Now. Functionality
# rocket: Camera = Camera("rocket")
# #rocket.set_file(7)
# rocket.start_recording()
# #rocket.set_file(7)
# #rocket.run(30)
# rocket.stop_recording()
