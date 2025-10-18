from screeninfo import get_monitors
import hand

if __name__ == "__main__":
    # --- Display monitor info ---
    for monitor in get_monitors():
        print(f"Monitor: {monitor.name}")
        print(f" Width: {monitor.width}")
        print(f" Height: {monitor.height}")
        print(f" X: {monitor.x}")
        print(f" Y: {monitor.y}")
        print("------")

    # --- Start hand & finger tracking ---
    my_hand = hand.HandTracker(monitor.width, monitor.height)
    
    my_hand.get_hand_and_finger_positions()
