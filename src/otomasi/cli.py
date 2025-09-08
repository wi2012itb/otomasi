from abc import ABC, abstractmethod
from argparse import ArgumentParser, FileType, Namespace

from otomasi.attendance import zoom_attendance
from otomasi.calendar import holiday_summary
from otomasi.grading import adjust_final, compile, dpk
from otomasi.mentoring import assign_groups, journal_screener, journeys_compile
from otomasi.utilities.files import DfOutFormat


class Subcommand(ABC):
    def __init__(self, name: str, help: str):
        self.name = name
        self.help = help

    @abstractmethod
    def load_parser(self, parser: ArgumentParser):
        raise NotImplementedError

    @abstractmethod
    def main(self, args: Namespace):
        raise NotImplementedError


class Compile(Subcommand):
    def load_parser(self, parser):
        parser.add_argument("master", type=str, help="master reference file to compile")
        parser.add_argument(
            "inputs",
            type=str,
            nargs="+",
            help="input files to be compiled together, MUST share a common column with the master file",
        )
        parser.add_argument(
            "--out", type=str, help="output file name", default="compiled"
        )
        parser.add_argument(
            "--column",
            type=str,
            help="column used to join the tables together",
            default="NIM",
        )
        parser.add_argument(
            "--method",
            type=compile.JoinMethod,
            choices=list(compile.JoinMethod),
            default=compile.JoinMethod.LEFT,
            help="join method",
        )
        parser.add_argument(
            "--concat",
            action="store_true",
            help="concatenates the inputs first instead of just joining them",
        )

    def main(self, args):
        compile.main(
            args.master, args.inputs, args.out, args.column, args.method, args.concat
        )


class DPK(Subcommand):
    def load_parser(self, parser):
        parser.add_argument(
            "inputs",
            type=str,
            nargs="+",
            help="input files to be compiled together, MUST share a common column with the master file",
        )
        parser.add_argument(
            "--out", type=str, help="output file name", default="master_dpk"
        )

    def main(self, args):
        dpk.main(args.inputs, args.out)


class CompileJourneys(Subcommand):
    def load_parser(self, parser):
        parser.add_argument(
            "input_file",
            type=str,
            nargs="+",
            help="mentor grades to be compiled",
        )
        parser.add_argument(
            "--anchor",
            type=str,
            help="anchor header to be used for extraction",
            default="NIM",
        )
        parser.add_argument("--out", type=str, default="journeys")

    def main(self, args):
        return journeys_compile.main(args.input_file, args.anchor, args.out)


class MentorGroup(Subcommand):
    def load_parser(self, parser):
        parser.add_argument(
            "input_file",
            type=str,
            nargs="+",
            help="students informations to be compiled into groups",
        )
        parser.add_argument(
            "--group_size", type=int, default=10, help="Maximum group members count"
        )
        parser.add_argument(
            "--min_size", type=int, default=7, help="Minimum group members count"
        )
        parser.add_argument("--out", type=str, default="mentoring")

    def main(self, args):
        assign_groups.main(args.input_file, args.out, args.group_size, args.min_size)


class JournalScreener(Subcommand):
    def load_parser(self, parser):
        parser.add_argument("input_dir", type=str, help="input directory")
        parser.add_argument(
            "-o", "--out", type=str, help="output file name", default="result.xlsx"
        )

    def main(self, args):
        journal_screener.main(args.input_dir, args.out)


class HolidaySummary(Subcommand):
    def load_parser(self, parser):
        parser.add_argument(
            "seed_file",
            type=FileType("r"),
            metavar="seed-file",
            help="JSON file containing information about the class schedule",
        )
        parser.add_argument(
            "holiday_file",
            type=FileType("r"),
            metavar="holiday-file",
            help="CSV file containing list of holidays",
        )
        parser.add_argument(
            "-o",
            "--output",
            type=str,
            nargs="?",
            default="holidays_compiled",
            help="output file location",
        )
        parser.add_argument(
            "--out-format",
            type=DfOutFormat,
            default=DfOutFormat.CSV,
            choices=list(DfOutFormat),
            help="output format of the file",
        )
        parser.add_argument(
            "--drop-dates",
            action="store_true",
            help="drop the date columns for classes",
        )

    def main(self, args):
        holiday_summary.main(
            args.seed_file,
            args.holiday_file,
            args.output,
            args.out_format,
            args.drop_dates,
        )


class ZoomAttendance(Subcommand):
    def load_parser(self, parser):
        parser.add_argument("filename", type=str)
        parser.add_argument(
            "--threshold",
            type=int,
            help="minimum threshold (in minutes) for attendance to count (default 80 minutes), set to -1 for average duration as threshold",
            default=80,
        )
        parser.add_argument(
            "-O", "--out", type=str, help="output filename", default="result.csv"
        )

    def main(self, args):
        zoom_attendance.main(args.filename, args.out, args.threshold)


class AdjustScore(Subcommand):
    def load_parser(self, parser):
        parser.add_argument(
            "input_file",
            type=str,
            help="Final score file",
        )
        parser.add_argument(
            "grade_config",
            type=FileType("r"),
            metavar="grade_config",
            help="JSON file containing upper grade threshold",
        )
        parser.add_argument(
            "--score",
            type=str,
            nargs="?",
            default="NA",
            help="Score column to be checked and adjusted",
        )
        parser.add_argument(
            "--index",
            type=str,
            nargs="?",
            default="Indeks",
            help="Final index column to be checked against",
        )
        parser.add_argument(
            "-o",
            "--output",
            type=str,
            nargs="?",
            default="adjusted.xlsx",
            help="output file location",
        )

    def main(self, args):
        adjust_final.main(
            args.input_file, args.grade_config, args.score, args.index, args.output
        )


def get_subcommands() -> list[Subcommand]:
    return [
        HolidaySummary(
            "holiday", "Compile given schedule and holidays into a calendar"
        ),
        ZoomAttendance(
            "zoom-attendance",
            "Generate attendance based on Zoom meeting report's duration",
        ),
        MentorGroup("groups", "Generate mentoring groups from student list"),
        CompileJourneys(
            "journeys-compile", "Compile mentors' grading sheets for journeys"
        ),
        JournalScreener(
            "journal", "Perform sanity checks from submitted devotion journals"
        ),
        Compile(
            "compile",
            "Compiles several files into one based on a master (reference) file",
        ),
        DPK(
            "dpk",
            "Compiles several DPK files into one file, must share same columns",
        ),
        AdjustScore("adjust-score", "Adjust final score based on modified final grade"),
    ]


def main():
    parser = ArgumentParser(prog="otomasi")
    subparsers = parser.add_subparsers(
        dest="command", help="The command to run which module", required=True
    )
    subcommands = get_subcommands()
    for subcommand in subcommands:
        # uses subparsers for subcommands, see https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.add_subparsers
        subcommand_parser = subparsers.add_parser(subcommand.name, help=subcommand.help)
        subcommand.load_parser(subcommand_parser)
        # Set the function to run the subcommand
        subcommand_parser.set_defaults(func=subcommand.main)
    args = parser.parse_args()
    # Run the function set with set_defaults(), passing the arguments as parameters
    args.func(args)
