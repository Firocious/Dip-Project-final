import cv2
import face_recognition
import tkinter as tk
import threading

# Load sample images and learn how to recognize them
rahul_image = face_recognition.load_image_file("rahul.jpg")
harshal_image = face_recognition.load_image_file("harshal.jpg")
venki_image = face_recognition.load_image_file("venki.jpg")

rahul_face_encoding = face_recognition.face_encodings(rahul_image)[0]
harshal_face_encoding = face_recognition.face_encodings(harshal_image)[0]
venki_face_encoding = face_recognition.face_encodings(venki_image)[0]

# Create arrays of known face encodings and their corresponding names
known_face_encodings = [rahul_face_encoding, harshal_face_encoding, venki_face_encoding]
known_face_names = ["Rahul", "Harshal", "Venki"]

# Define voting options
voting_options = ["Candidate A", "Candidate B", "Candidate C"]

# Function to handle button click
def vote(candidate):
    print("Voted for:", candidate)

# Function to create Tkinter window for voting options
def create_voting_window():
    root = tk.Tk()
    root.geometry("300x200")
    root.title("Voting Options")

    # Create buttons for each voting option
    for i, option in enumerate(voting_options):
        button = tk.Button(root, text=option, command=lambda opt=option: vote(opt))
        button.pack(pady=5)

    # Start Tkinter main loop
    root.mainloop()

# Function to handle video streaming
def video_stream():
    # Initialize the video capture
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Find all face locations and encodings in the current frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Loop through each face found in the frame
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face matches any known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match is found, use the name of the matched face
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

                # Draw a box around the face and label it
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

                # Create voting options window
                create_voting_window()

            else:
                # If face doesn't match, display "Voter Not Listed" in red
                cv2.putText(frame, "Voter Not Listed", (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    cap.release()
    cv2.destroyAllWindows()

# Start video streaming thread
video_thread = threading.Thread(target=video_stream)
video_thread.start()
