import os
import time

class Utils:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')


    @staticmethod
    def delay(ms):
        time.sleep(ms / 1000)
        
        
    @staticmethod
    def showBox(title: str, subtitle: str | None = None, *, width: int | None = None, use_ascii: bool = False, color: bool = True) -> None:
        """Print a centered, width-aware CLI box; optional subtitle; no return."""
        import shutil, re
        
        term_w = shutil.get_terminal_size(fallback=(80, 24)).columns
        w = max(60, min(width if isinstance(width, int) and width >= 20 else term_w, 120))
        
        if use_ascii:
            tl, tr, bl, br, h, v = "+", "+", "+", "+", "-", "|"
        else:
            tl, tr, bl, br, h, v = "╔", "╗", "╚", "╝", "═", "║"
            
            
        # Colors
        if color and not use_ascii:
            C_BORDER = "\033[36m"     # cyan
            C_TITLE  = "\033[97;1m"   # bright white bold
            C_SUB    = "\033[90m"     # dim gray
            C_RESET  = "\033[0m"
        else:
            C_BORDER = C_TITLE = C_SUB = C_RESET = ""
            
        # Lines to render
        lines = [f"{C_TITLE}{title}{C_RESET}"]
        if subtitle:
            lines.append(f"{C_SUB}{subtitle}{C_RESET}")
            
        # Helpers
        ansi_re = re.compile(r"\x1b\[[0-9;]*m")
        def border() -> str:
            return f"{C_BORDER}{tl}{h * (w - 2)}{tr}{C_RESET}"
        
        def empty() -> str:
            return f"{C_BORDER}{v}{' ' * (w - 2)}{v}{C_RESET}"
        
        def center_line(s: str) -> str:
            visible = ansi_re.sub("", s)
            pad = max(0, (w - 2) - len(visible))
            left = pad // 2
            right = pad - left
            return f"{C_BORDER}{v}{' ' * left}{s}{' ' * right}{v}{C_RESET}"
        
        # Render
        print()
        print(border())
        print(empty())
        for s in lines:
            print(center_line(s))
        print(empty())
        print(f"{C_BORDER}{bl}{h * (w - 2)}{br}{C_RESET}")
