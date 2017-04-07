import robot
import curses


MOVES = {
    32: robot.stop_motors,
    258: robot.backwards,
    259: robot.forwards,
    260: robot.right,
    261: robot.left
}


def run(std_scr):
    control = 0
    while control != 120:
        control = std_scr.getch()
        std_scr.addstr(0, 0, "Control: " + str(control) + "  ")
        if control in MOVES:
            MOVES[control]()


curses.wrapper(run)

robot.cleanup()
