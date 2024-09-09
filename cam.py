import cv2

def cam():
    cap = cv2.VideoCapture('Modern irrigation system.mp4')  # Adjust the video file path as per your system
    
    while True:
        ret, frame = cap.read()

        # Check if the frame is empty (end of the video)
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        cv2.imshow("Camera Feed", frame)

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

cam()
