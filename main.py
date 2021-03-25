import sys
from analysis import BrainAnalysis
from view.MainWindow import MainWindow

if __name__ == "__main__":
    if "-analysis" in sys.argv:
        BrainAnalysis.main()
    else:
        initial_app = MainWindow()
        initial_app.mainloop()
        print("Application Closed")
