from moulitek.mt_print import *
import subprocess
import glob
import json

moulitek_script_trace = {
    "build": False,
    "coverage": None,
    "branches": None,
    "tests": []
}

moulitek_crash_reasons = dict(
    [(SEGFAULT, "SEGFAULT"), (BADOUTPUT, "BADOUTPUT"), (RETVALUE, "RETVALUE"), (TIMEOUT, "TIMEOUT")])


def check_makefile():
    makefile_test = Category(
        "Preriquires Tests", "Looking for mandatory preriquires of the project.", info=True)
    make_rules = makefile_test.add_sequence(
        "Make rules", "Check all makefile's mandatory rules.")
    mandatory = ["all", "re", "clean", "fclean"]
    for phony in mandatory:
        make_rules.add_test("Make %s." % phony)
        ret = subprocess.call(
            "timeout 15s make -q %s 1> /dev/null 2> /dev/null" % phony, shell=True)
        if ret == 2:
            make_rules.set_status("Make %s." % phony, False, BADOUTPUT,
                                  "Rule make %s" % phony, "No rule in Makefile")
        else:
            make_rules.set_status("Make %s." % phony, True)


def init_moulitek():
    """Initialize moulitek for testing
    """
    global moulitek_script_trace
    if not "Makefile" in glob.glob("*"):
        moulitek_script_trace["build"] = True
        return
    ret = subprocess.call(
        "timeout 15s make -q tests_run 1> /dev/null 2> /dev/null", shell=True)
    if ret != 2:
        subprocess.call(
            "timeout 15s make tests_run 1> /dev/null 2> /dev/null", shell=True)
        proc = subprocess.Popen("timeout 15s gcovr --exclude=tests", shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        coverage, _ = proc.communicate()
        moulitek_script_trace["coverage"] = coverage.decode()
        proc = subprocess.Popen("timeout 15s gcovr --exclude=tests -b",
                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        branches, _ = proc.communicate()
        moulitek_script_trace["branches"] = branches.decode()
    check_makefile()
    ret = subprocess.call(
        "timeout 15s make fclean && make 1> /dev/null 2> /dev/null", shell=True)
    if (ret == 0):
        moulitek_script_trace["build"] = True
    else:
        exit(0)

def gen_trace():
    global moulitek_script_trace
    for cat in moulitek_all_categories:
        category = {"name": cat.name, "description": cat.desc,
                    "info": cat.info, "sequences": []}
        for seq in cat.sequences:
            sequence = {"name": seq.name, "description": seq.desc, "passed": True, "tests": []}
            for test in seq.tests:
                if test["passed"]:
                    sequence["tests"].append(
                        {"name": test["name"], "passed": True})
                else:
                    if test["reason"] == NEVER_RUN:
                        continue
                    sequence["passed"] = False
                    sequence["tests"].append(
                        {"name": test["name"], "description": test["desc"], "passed": False, "reason": moulitek_crash_reasons[test["reason"]], "expected": test["expected"], "got": test["got"]})
            category["sequences"].append(sequence)
        moulitek_script_trace["tests"].append(category)
    open("trace.txt", "w+").write(json.dumps(moulitek_script_trace))
