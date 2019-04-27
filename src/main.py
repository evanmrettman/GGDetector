#import antigravity
import utility.logging as log
import json
import files.parse as parse


VERSION = 0
F_IN = "data"
F_ADD = "%s/additional_files" % F_IN
F_OUT = "output/version_%02d" % VERSION

def main():
    log.info("Hello from Steam Sensor")


    parse.parseApps("%s/list_4_26_19.json" % (F_IN))
    #parse.parseApps("%s/list_short.json" % (F_IN))


if __name__ == "__main__":
    log.starting()
    main()
    log.ending()