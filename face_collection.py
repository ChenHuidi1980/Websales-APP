import cv2
import os

def create_user_folder():
    dirnum = 0
    os.chdir("faceIDs")

    file_list = os.listdir()
    dir_list = []
    for eachfile in file_list:
        if '.' not in eachfile:
            dir_list.append(eachfile)

    while not dirnum:
        username = input('Please input your user name: ')
        if username != '':
            if len(dir_list) == 0:
                break

            for eachdir in dir_list:
                if username in eachdir:
                    print('User name exists, please use another name.\n')
                    dirnum = 0
                    break
                else:
                    dirnum += 1

    dirnum += 1
    userfolder = username + '_' + str(dirnum)
    os.mkdir(userfolder)
    os.chdir(userfolder)
    userpath = os.getcwd()
    os.chdir("..")
    os.chdir("..")
    return userpath, username, dirnum
    #print('Total', dirnum, 'sub directories.')

def face_collection():
    face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    camera = cv2.VideoCapture(0)
    face_id = input('Please enter the face ID: ')
    sample_number = 0

    storagedir = os.path.dirname('faceIDs/')
    if not os.path.exists(storagedir):
        os.mkdir(storagedir)

    while camera.isOpened():
        _, video = camera.read()
        grey_video = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(grey_video, scaleFactor=1.05, minNeighbors=5, minSize=(100, 100))

        for (x, y, w, h) in faces:
            cv2.rectangle(video, (x, y), (x+w, y+h), (0, 255, 0), 5)

        cv2.imshow('video', video)
        k = cv2.waitKey(200)
        sample_number = sample_number + 1

        if k & 0xFF == ord('q'):
            break

        if sample_number > 50:
            print("Saving Completed.")
            break
        else:
            print("Saving face " + str(sample_number) + "...")
            cv2.imwrite("faceIDs/User_" + face_id + '_face' + str(sample_number) + ".jpg",
                        grey_video[y:y + h, x:x + w])

    camera.release()
    cv2.destroyAllWindows()
