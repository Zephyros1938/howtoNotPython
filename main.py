class Main:
    __contents__: dict = {"__import__": {}, "assets": {}}
    __toImport = ["pygame", "zipfile", "os", "shutil", "math"]

    def __init__(self, *flags):
        for x in self.__toImport:
            self["__import__"][x] = __import__(x)
        self["__import__"]["pygame"].init()
        self["windowing"] = {
            "WIN": self["__import__"]["pygame"].display.set_mode((1920, 1080)),
            "DT": -1.0,
            "MAX_FPS": -1,
        }
        self["common"] = {
            "CLOCK": self["__import__"]["pygame"].time.Clock(),
            "RUNNING": True,
        }
        self["AssetManager"] = AssetManager(self)
        self["AssetManager"].registerFontZipped(
            "fonts/Roboto_Mono.zip", "static/RobotoMono-Bold.ttf", "cool", 24
        )
        self["AssetManager"].registerImage(
            "images/home_25dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.png", "home"
        )

    def run(self, *flags):
        if "debug" in flags:
            self["DEBUG"] = {}
        TOTAL_TIME = 0
        WIN = self["windowing"]["WIN"]
        CLOCK = self["common"]["CLOCK"]
        AM = self["AssetManager"]
        coolFont = AM.getFont("cool", 24)
        while self["common"]["RUNNING"]:
            for ev in self["__import__"]["pygame"].event.get():
                if ev.type == self["__import__"]["pygame"].QUIT:
                    self["common"]["RUNNING"] = False

            WIN.fill("blue")
            fps = CLOCK.get_fps()
            coolFont.render_to(
                WIN,
                (
                    (self["__import__"]["math"].sin(TOTAL_TIME) + 1)
                    / 2
                    * WIN.get_width(),
                    (self["__import__"]["math"].cos(TOTAL_TIME) + 1)
                    / 2
                    * WIN.get_height(),
                ),
                f"{fps:.2f}",
            )
            WIN.blit(AM.getImage("home"), (100, 100))


            self["__import__"]["pygame"].display.flip()

            self["windowing"]["DT"] = (
                CLOCK.tick(self["windowing"]["MAX_FPS"]) / 1000.0
            )
            TOTAL_TIME += self["windowing"]["DT"]
        if "DEBUG" in self.__contents__:
            self["__import__"]["pygame"].quit()
            print(self.__contents__)

        return self

    def cleanup(self, *flags):
        self["AssetManager"].cleanup()

    def initializeAttributesS1(self, codeToDo: list[str] = [], *flags):
        """Uses `exec()` to set attributes"""
        for x in codeToDo:
            exec(x, globals(), locals())
        return self

    def initializeAttributesS2(self, **classes):
        for name, cls in classes.items():
            setattr(Main, name, cls)
        return self

    def __setitem__(self, key, item):
        self.__contents__[key] = item

    def __getitem__(self, key):
        return self.__contents__[key]


class AssetManager:
    from typing import Any
    from os import name as osname

    _CACHE: dict = {"FONTS": {}, "IMAGES": {}}

    def __init__(self, main: Main):
        self.main = main
        try:
            self.main["__import__"]["os"].mkdir(self._OUTPUT_DIR)
        except:
            pass

    _UNZIPPED_PATHS: dict[str, str] = {}
    _SEARCH_DIR = "./assets/"
    _OUTPUT_DIR = "./unzipped/" if osname != "posix" else "/tmp/zephyros1938/unzipped/"

    def unzipFile(self, path: str):
        zipfile = self.main["__import__"]["zipfile"]

        with zipfile.ZipFile(self._SEARCH_DIR + path, "r") as zip_ref:
            zip_ref.extractall(self._OUTPUT_DIR + path)
        print(f"Unzipped {path} to {self._SEARCH_DIR}")
        return self._OUTPUT_DIR + path

    def registerFontZipped(
        self, fontZipPath: str, fontFullPath: str, fontName: str, fontSize: int
    ):
        """preferably use google fonts for this"""
        if not fontZipPath in self._UNZIPPED_PATHS:
            self._UNZIPPED_PATHS[fontZipPath] = self.unzipFile(fontZipPath)
        try:
            fp = self._UNZIPPED_PATHS[fontZipPath] + "/" + fontFullPath
            fn = (fontName,fontSize)
            if fn not in self._CACHE["FONTS"]:
                self._CACHE["FONTS"][fn] = self.main["__import__"][
                    "pygame"
                ].freetype.Font(fp, fontSize)
            else:
                print(f"[INFO] Font [{fn}] ({fontName}) Already Registered in cache.")
        except Exception as e:
            raise Exception(e)

    def registerFontDirect(self, fontPath: str, fontName: str, fontSize: int):
        fn = (fontName,fontSize)
        if fn not in self._CACHE["FONTS"]:
            self._CACHE["FONTS"][fn] = self.main["__import__"]["pygame"].freetype.Font(
                fontPath, fontSize
            )
        else:
            print(f"[INFO] Font [{fn}] ({fontName}) Already Registered in Cache.")

    def getFont(self, fontName: str, fontSize: int):
        fn = (fontName,fontSize)
        if fn not in self._CACHE["FONTS"]:
            raise Exception(
                f"Please register font {fontName} with AssetManager.registerFont()"
            )
        return self._CACHE["FONTS"][fn]

    def registerImage(self, imagePath, imageName):
        if imageName not in self._CACHE["IMAGES"]:
            self._CACHE["IMAGES"][imageName] = self.main["__import__"]["pygame"].image.load(self.main["__import__"]["os"].path.join('assets', imagePath))
        else:
            print(f"[INFO] Image [{imageName}] ({imagePath}) Already Registered in Cache.")
    
    def getImage(self, imageName):
        if imageName not in self._CACHE["IMAGES"]:
            raise Exception(
                f"Please register image {imageName} with AssetManager.registerImage()"
            )
        return self._CACHE["IMAGES"][imageName]
        

    def cleanup(self):
        (
            self.main["__import__"]["shutil"].rmtree(self._OUTPUT_DIR)
            if self.osname != "posix"
            else ()
        )


if __name__ == "__main__":
    Main().initializeAttributesS1(
        [
            """
Main.Vector2 = type(
    "Vector2",
    (object,),
    {
        "x": 0,
        "y": 0,
        "__init__": lambda self, x=0, y=0: setattr(self, "x", x) or setattr(self, "y", y)
    }
)
""",
        ]
    ).initializeAttributesS2().run().cleanup()
