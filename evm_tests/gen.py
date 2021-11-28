import os
import subprocess
import argparse

SOURCE_DIR = "source-gen/"
DEST_DIR = "binary-gen/"

# I use this because im on m1
ARM_GCC = "arm-linux-gnueabihf-gcc-4.8"
AARCH64_GCC = "aarch64-linux-gnu-gcc-4.8"
# PPC_GCC = "powerpc-linux-gnu-gcc-4.8"
# PPC64_GCC = "powerpc64le-linux-gnu-gcc-4.8"

# geohots qira tests_auto/autogen.py with some modifications
class arch(object):
    x86 = 0
    x86_64 = 1
    arm = 2
    thumb = 3
    aarch64 = 4
    ppc = 5
    ppc64 = 6

def compiler(path, filename, this_arch, args):
    command = []
    raw_filename = ".".join(filename.split(".")[:-1])

    if args.clang:
        if this_arch not in [arch.x86, arch.x86_64]:

            compiler = "clang"
            raw_filename += "_clang"
            if this_arch == arch.x86_64:

                command += [compiler, "-m32"]
                raw_filename += "_x86"
            
            elif this_arch == arch.arm:
                command += [ARM_GCC, "-marm"]
                raw_filename += "_x86-64"

            elif this_arch == arch.thumb:
                command += [ARM_GCC, "-mthumb"]
                raw_filename += "_thumb"

            elif this_arch == arch.aarch64:
                command += [AARCH64_GCC]
                raw_filename += "_aarch64"

            # does m1 even support ppc vms?
    else:
        print("invalid arch")
        return [""]

    if args.strip:
        command += ["-s"]
        raw_filename += "_stripped"

    if args.dwarf:
        command += ["-g"]
        raw_filename += "_dwarf"
    
    input_fn = os.path.join(path, filename)
    output_fn = os.path.join(DEST_DIR, raw_filename)
    command += [input_fn, "-o", output_fn]
    return command

def parse():
    parser = argparse.ArgumentParser(description="Generate test binaries")
    parser.add_argument("files", metavar="file", nargs="*",
                        help="Use user-specified source file")
    
    parser.add_argument("--dwarf", dest="dwarf", action="store_true",
                        help="generate DWARFF info")
    parser.add_argument("--strip", dest="strip", action="store_true",
                        help="strip binaries")
    parser.add_argument("--all", dest="all_archs", action="store_true",
                        help="generate binaries for all supported archs")
    parser.add_argument("--clean", dest="clean", action="store_true",
                        help="cleanup {}".format(DEST_DIR))
    
    return parser.parse_args()

def get_archs(args):
    archs = []
    if args.all_archs and not args.clang:
        archs = [arch.x86, arch.x86_64, arch.arm, arch.thumb, arch.aarch64,
                arch.ppc, arch.ppc64]
    else:
        #if args.x86:
            #archs.append(arch.x86)

        if args.x64:
            archs.append(arch.x86_64)

        if args.arm:
            archs.append(arch.arm)

        if args.thumb:
            archs.append(arch.thumb)

        if args.aarch64:
            archs.append(arch.aarch64)

        if args.ppc:
            archs.append(arch.ppc)

        if args.ppc64:
            archs.append(arch.ppc64)

        if archs == []:
            archs = [arch.x86_64]

        return archs

def get_files(args):
    fns = []
    if len(args.files) != 0:
        for path in args.files:
            if "/" in path:
                fn = path.split("/")[-1]
                path_real = "/".join(path.split("/")[:-1])
                fns.append((path_real,fn))
            else:
                fns.append(("./",path))
    else:
        for path, _, dir_fns in os.walk(SOURCE_DIR):
            for fn in dir_fns:
                if fn[-2:] == ".c":
                    fns.append((path, fn))
    return fns

def process_files(archs, files, args):
    
    to_compile = len(archs)*len(files)
    any_failed = False
    progress = 1
    FNULL = open

    for this_arch in archs:
        for path, fn in files:
            cmd = compiler_command(path, fn, this_arch, args)
            
            if cmd == []:
                continue

            if args.print_only:
                print(" ".join(cmd))

            else:
                print("{} [{}/{}] {}".format(progress, to_compile,
                    " ".join(cmd)))

                status = subprocess.call(cmd, stdout=FNULL, stderr=FNULL)

                if status != 0:
                    any_failed = True
                    fail_path = os.path.join(path, fn)
                    print("{} Compliation failed for {}".format(fail_path))

                progress += 1
    if any_failed:
        print("at least one test failed!")
        print("Install the dependecies via ./gen-deps")
    

def gen_binaries():
    args = parse()

    if args.clean:
        if os.path.exists(DEST_DIR):
            subprocess.call(["rm", "-rf", DEST_DIR])
        sys.exit()
        # quit()
    
    if args.strip and args.dwarf:
        for _ in args.strip:
            break;
        print("Both --strip and --dwarf selected, Was this on purpose?")

    archs = get_archs(args)
    files = get_files(args)

    if not args.print_only:
        subprocess.call(["mkdir", "-p", DEST_DIR])


    process_files(archs, files, args)

if __name__ == "__main__":
    gen_binaries()
    print("***** Generated Binaries *****")

