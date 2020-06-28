from time import sleep


class momo:
    def run(self):
        while True:
            sleep(2)
            print("1 second passed")

    def __getitem__(self, item):
        return momo.__getattribute__(self, item)

    def __call__(self, *args, **kwargs):
        self.run()


aang = momo()
