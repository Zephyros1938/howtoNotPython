class Main:
    __contents__ = {"__import__": {}, "assets": {}}
    __toImport = ["pygame", "zipfile", "os", "shutil", "math"]

    def __init__(self, *flags):
        for x in self.__toImport:
            self["__import__"][x] = __import__(x)

        pg = self["__import__"]["pygame"]

        pg.init()

        self["windowing"] = {
            "WIN": pg.display.set_mode((1920, 1080)),
            "DT": -1.0,
            "MAX_FPS": -1,
        }
        self["common"] = {
            "CLOCK": pg.time.Clock(),
            "RUNNING": True,
        }

        self["AssetManager"] = AssetManager(self)
        AM = self["AssetManager"]

        AM.registerFontZipped(
            "fonts/Roboto_Mono.zip",
            "static/RobotoMono-Bold.ttf",
            "cool",
            24,
        )

        AM.registerImage(
            "images/home_25dp_E3E3E3_FILL0_wght400_GRAD0_opsz24.png",
            "home",
        )

    def run(self, *flags):
        pg = self["__import__"]["pygame"]
        math = self["__import__"]["math"]

        if "debug" in flags:
            self["DEBUG"] = {}

        TOTAL_TIME = 0
        WIN = self["windowing"]["WIN"]
        CLOCK = self["common"]["CLOCK"]
        AM = self["AssetManager"]
        coolFont = AM.getFont("cool", 24)

        ev_get = pg.event.get
        flip = pg.display.flip
        fill = WIN.fill
        sin = math.sin
        cos = math.cos
        getImage = AM.getImage

        win_w = WIN.get_width()
        win_h = WIN.get_height()

        while self["common"]["RUNNING"]:
            for ev in ev_get():
                if ev.type == pg.QUIT:
                    self["common"]["RUNNING"] = False

            fill("blue")

            fps = CLOCK.get_fps()

            coolFont.render_to(
                WIN,
                (
                    (sin(TOTAL_TIME) + 1) * 0.5 * win_w,
                    (cos(TOTAL_TIME) + 1) * 0.5 * win_h,
                ),
                f"{fps:.2f}",
            )

            WIN.blit(getImage("home"), (100, 100))

            flip()

            dt = CLOCK.tick(self["windowing"]["MAX_FPS"]) / 1000.0
            self["windowing"]["DT"] = dt
            TOTAL_TIME += dt

        if "DEBUG" in self.__contents__:
            if self["DEBUG"]["printOnExit"]:
                print(self.__contents__)
            if self["DEBUG"]["quitPygameOnExit"]:
                pg.quit()

        return self

    def cleanup(self, *flags):
        self["AssetManager"].cleanup()

    def initializeAttributesS1(self, codeToDo: list[str] = [], *flags):
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

    _CACHE = {"FONTS": {}, "IMAGES": {}}

    _UNZIPPED_PATHS = {}
    _SEARCH_DIR = "./assets/"
    _OUTPUT_DIR = "./unzipped/" if osname != "posix" else "/tmp/zephyros1938/unzipped/"

    def __init__(self, main: Main):
        self.main = main
        os = self.main["__import__"]["os"]

        try:
            os.makedirs(self._OUTPUT_DIR, exist_ok=True)
        except FileExistsError:
            pass

        self._pg = self.main["__import__"]["pygame"]
        self._ospath = os.path

    def unzipFile(self, path: str):
        zipfile = self.main["__import__"]["zipfile"]

        full = self._SEARCH_DIR + path
        out = self._OUTPUT_DIR + path

        with zipfile.ZipFile(full, "r") as zip_ref:
            zip_ref.extractall(out)

        print(f"Unzipped {path} to {self._SEARCH_DIR}")
        return out

    def registerFontZipped(
        self,
        fontZipPath: str,
        fontFullPath: str,
        fontName: str,
        fontSize: int,
    ):
        """try to use google fonts for this since they output well for zip files"""
        if fontZipPath not in self._UNZIPPED_PATHS:
            self._UNZIPPED_PATHS[fontZipPath] = self.unzipFile(fontZipPath)

        fp = self._UNZIPPED_PATHS[fontZipPath] + "/" + fontFullPath
        key = (fontName, fontSize)

        if key not in self._CACHE["FONTS"]:
            self._CACHE["FONTS"][key] = self._pg.freetype.Font(fp, fontSize)
        else:
            print(f"[INFO] Font {key} already cached.")

    def registerFontDirect(self, fontPath: str, fontName: str, fontSize: int):
        key = (fontName, fontSize)

        if key not in self._CACHE["FONTS"]:
            self._CACHE["FONTS"][key] = self._pg.freetype.Font(fontPath, fontSize)
        else:
            print(f"[INFO] Font {key} already cached.")

    def getFont(self, fontName: str, fontSize: int):
        key = (fontName, fontSize)
        if key not in self._CACHE["FONTS"]:
            raise Exception(
                f"Please register font {fontName} with AssetManager.registerFont()"
            )
        return self._CACHE["FONTS"][key]

    def registerImage(self, imagePath, imageName):
        if imageName not in self._CACHE["IMAGES"]:
            joined = self._ospath.join("assets", imagePath)
            self._CACHE["IMAGES"][imageName] = self._pg.image.load(joined)
        else:
            print(f"[INFO] Image [{imageName}] already cached.")

    def getImage(self, imageName):
        if imageName not in self._CACHE["IMAGES"]:
            raise Exception(
                f"Please register image {imageName} with AssetManager.registerImage()"
            )
        return self._CACHE["IMAGES"][imageName]

    def cleanup(self):
        shutil = self.main["__import__"]["shutil"]
        try:
            shutil.rmtree(self._OUTPUT_DIR)
        except FileNotFoundError:
            pass


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
