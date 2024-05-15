import threading
import multiprocessing
from camera_system import start_capture
from chassis_movement import chassis_forward_backward
import time

if __name__ == '__main__':
    print("Starting the system...")
    base_directory = input("Enter the directory name for saving the datasets: ")
    duration = int(input("Enter the duration (seconds): "))
    motor_speed = int(input("Enter the motor speed (-100 to 100): "))
    # Run motor operations in a thread
    motor_thread = threading.Thread(target=chassis_forward_backward,args = (duration,motor_speed))
    motor_thread.start()

    # Run camera processes (multiprocessing is internal)
    # time.sleep(duration*0.2)
    start_capture(base_directory)

    motor_thread.join()  # Ensure motor operations complete
    print("System shutdown. All operations completed.")
