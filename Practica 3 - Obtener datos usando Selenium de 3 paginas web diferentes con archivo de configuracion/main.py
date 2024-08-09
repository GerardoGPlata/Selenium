import curses
import subprocess

def print_menu(stdscr, selected_option):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    menu = ["1. Ejecutar script de Cyber",
            "2. Ejecutar script de Amazon",
            "3. Ejecutar script de Pagos UTT",
            "4. Ejecutar todos los scripts",
            "5. Salir"]
    
    for idx, option in enumerate(menu):
        x = w//2 - len(option)//2
        y = h//2 - len(menu)//2 + idx
        if idx == selected_option:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, option)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, option)
    
    stdscr.refresh()

def run_script(script_name):
    """Ejecuta un script dado su nombre."""
    subprocess.run(["python", script_name])

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    current_option = 0
    while True:
        print_menu(stdscr, current_option)
        key = stdscr.getch()

        if key == curses.KEY_DOWN:
            current_option = (current_option + 1) % 5
        elif key == curses.KEY_UP:
            current_option = (current_option - 1) % 5
        elif key == ord('\n'):
            if current_option == 0:
                run_script("Cyberpuerta.py")
            elif current_option == 1:
                run_script("Amazon.py")
            elif current_option == 2:
                run_script("Pagos UTT.py")
            elif current_option == 3:
                # Ejecutar todos los scripts en secuencia
                run_script("Cyberpuerta.py")
                run_script("Amazon.py")
                run_script("Pagos UTT.py")
            elif current_option == 4:
                break

if __name__ == "__main__":
    curses.wrapper(main)
