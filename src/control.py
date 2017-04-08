import robot
import curses

ROBOT = robot.Robot()

MOVES = {
    32: ROBOT.stop_motors,
    258: ROBOT.backwards,
    259: ROBOT.forwards,
    260: ROBOT.right,
    261: ROBOT.left
}


def run(std_scr):
    control = 0
    while control != 120:
        control = std_scr.getch()
        std_scr.addstr(0, 0, "Control: " + str(control) + "  ")
        if control in MOVES:
            MOVES[control]()


curses.wrapper(run)

ROBOT.cleanup()
