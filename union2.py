# import the necessary packages

def file_scan():
    from imutils.video import VideoStream
    from pyzbar import pyzbar
    import argparse
    import datetime
    import imutils
    import time
    import cv2
    import csv
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
        help="path to output CSV file containing barcodes")
    args = vars(ap.parse_args())

    # initialize the video stream and allow the camera sensor to warm up
    print("[BILGI] Video kamera calisiyor...")
    vs = VideoStream(src=0).start()
    #vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)
    
    # open the output CSV file for writing and initialize the set of
    # barcodes found thus far
    csv = open(args["output"], "w")
    found = set()
    count = 0
    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it to
        # have a maximum width of 400 pixels
        frame = vs.read()
        #frame = imutils.resize(frame, width=400)
        #find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)
        # loop over the detected barcodes
        for barcode in barcodes:
                # extract the bounding box location of the barcode and draw
                # the bounding box surrounding the barcode on the image
                (x, y, w, h)=barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
       
                # the barcode data is a bytes object so if we want to draw it
                # on our output image we need to convert it to a string first
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type

                # draw the barcode data and barcode type on the image
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(frame, text, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                # if the barcode text is currently not in our CSV file, write
                # the timestamp + barcode to disk and update the set
                if barcodeData not in found:
                    if 5012345678900 == int(barcodeData):
                        csv.write("{},{}\n".format(barcodeData, "Bin1"))
                        csv.flush()
                        found.add(barcodeData)
                    elif 811204012344 == int(barcodeData):
                        csv.write("{},{}\n".format(barcodeData, "Bin2"))
                        csv.flush()
                        found.add(barcodeData)
                    elif 8691014000012 == int(barcodeData):
                        csv.write("{},{}\n".format(barcodeData, "Bin3"))
                        csv.flush()
                        found.add(barcodeData)
                    elif 3245456345344 == int(barcodeData):
                        print("I found the second")
                        csv.write("{},{}\n".format(barcodeData, "Bin2"))
                        csv.flush()
                        found.add(barcodeData)
                    
                
             # show the output frame
        cv2.imshow("Barcode Scanner", frame)
        key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
        #count = count + 1
        if key == ord("q"):
            break

    # close the output CSV file do a bit of cleanup
    print("[BILGI] Islem sonlandi...")
    cv2.destroyAllWindows()
    vs.stop()
    csv.close()
   
def file_sender():
    import csv
    import serial
    import time
    ##Initialise the serial connection
    ser = serial.Serial('COM5', 9600)
    time.sleep(2)
    print("In file sender")
    ##open csv file and read it in one line at a time
    with open('barcodes.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader: ##for each line do the following
            print("In fileeeeeeeee")
            myseq = row[0] ##read in the sequence number
            mystate = row[1] ##read in the bin number
            print(myseq) ## print sequence number for tracking
            print(mystate)##print bin number for visual checking
            ser.write(mystate.encode('utf-8')) ## write bin to arduino encoding to unicode
            print("In write")
            fromuno  = ser.readline().decode('UTF-8') ##confirmation from Arduino decoding back to characters
            print("In ser")
            print(fromuno) ##print picked message from Arduino
    

def main():
    file_scan()
    file_sender()
    

    
if __name__ == '__main__':
    main()
