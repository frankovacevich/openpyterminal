import openpyterminal as pt
import time
import os
import git


class Sample4(pt.ListSimple):

    def __init__(self):
        super().__init__("LOADING SCREEN TESTS")
        self.options = [
            ["Test 1 (time.sleep)", self.test1],
            ["Test 2 (time.sleep with longer min_wait)", self.test2],
            ["Test 3 (time.sleep with progress bar)", self.test3],
            ["Test 4 (os sleep)", self.test4],
            ["Test 5 (git clone)", self.test5],
            ["Test 6 (git clone with result)", self.test6],
            ["Exit", self.close]
        ]

        self.update()

    def test1(self):
        print("Starting")
        t = time.time()
        pt.LoadingScreen.show_dialog("Loading test 1", lambda: time.sleep(3))
        print("Done in", time.time() - t, "seconds")

    def test2(self):
        print("Starting. This should take longer")
        t = time.time()
        pt.LoadingScreen.show_dialog("Loading test 2", lambda: time.sleep(3), min_wait=6000)
        print("Done in", time.time() - t, "seconds")

    def test3(self):
        class MyLoadingScreen(pt.LoadingScreen):
            def __init__(self):
                super().__init__("Loading test 3")
                self.update_progress(0)

            def do(self):
                for i in range(0, 100):
                    time.sleep(0.1)
                    self.update_progress(i / 100)

        print("Starting")
        MyLoadingScreen().run()
        print("Done!")

    def test4(self):
        print("Starting subprocess")
        t = time.time()
        pt.LoadingScreen.show_dialog("Loading test 4", lambda: os.system("sleep 4"))
        print("Done in", time.time() - t, "seconds")

    def test5(self):
        print("Starting subprocess")
        t = time.time()
        pt.LoadingScreen.show_dialog(
            "Loading test 5",
            lambda: os.system("git clone https://github.com/frankovacevich/openpyterminal ~/test5")
        )
        print("Done in", time.time() - t, "seconds")

    def test6(self):
        print("Starting subprocess")

        class MyLoadingScreen(pt.LoadingScreen):
            def __init__(self):
                super().__init__("Loading test 6")
                self.result = None

            def do(self):
                repo = "https://github.com/frankovacevich/openpyterminal"
                try:
                    git.Repo.clone_from(repo)
                    self.result = True
                except:
                    self.result = False

        print("Starting")
        t = time.time()
        M = MyLoadingScreen()
        M.run()
        if M.result: pt.MessageDialog.show_dialog("Test Result", "Repository cloned", {"hide_btn_d": True})
        else: pt.MessageDialog.show_dialog("Test Result", "Failed to clone repository", {"hide_btn_d": True})
        print("Done in", time.time() - t, "seconds")


app = pt.TerminalApp(Sample4)
app.fullscreen = False
app.touchscreen = False
app.run()

