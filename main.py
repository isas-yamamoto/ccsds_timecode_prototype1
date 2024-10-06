import argparse
from datetime import datetime
from ccsds_timecode.cuc import CCSDS_TimeCode_CUC
from ccsds_timecode.cds import CCSDS_TimeCode_CDS
from ccsds_timecode.ccs import CCSDS_TimeCode_CCS
from ccsds_timecode.ascii import CCSDS_TimeCode_ASCII


def hexdump(data, sep=""):
    """Convert a byte sequence to a hex dump."""
    return sep.join([f"{x:02x}" for x in data])


def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description="Generate CCSDS Time Code with specified library."
    )

    # Add arguments for epoch, UTC time, and library
    parser.add_argument(
        "--code",
        type=str,
        choices=["CUC", "CDS", "CCS", "ASCII"],
        default="CUC",
        help="The time code to use for time conversion ('CUC', 'CDS', 'CCS', or 'ASCII').",
    )
    parser.add_argument(
        "--epoch",
        type=str,
        default="1958-01-01T00:00:00Z",
        help="The epoch time string in ISO 8601 format.",
    )
    parser.add_argument(
        "--utc",
        type=str,
        default=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f"),
        help="The UTC time string in ISO 8601 format.",
    )
    parser.add_argument(
        "--library",
        type=str,
        choices=["my", "astropy", "spice", "skyfield", "spacepy"],
        default="my",
        help="The library to use for time conversion ('my', 'astropy', 'spice', 'skyfield', or 'spacepy').",
    )

    # Parse arguments
    args = parser.parse_args()

    if args.code == "CUC":
        time_code = CCSDS_TimeCode_CUC(
            epoch=args.epoch,
            basic_time_unit=1,
            num_basic_octets=4,
            num_fractional_octets=2,
            library=args.library,
        )
    elif args.code == "CDS":
        time_code = CCSDS_TimeCode_CDS(
            epoch=args.epoch,
            epoch_id=0b0,
            length_of_day_segment=0b0,
            length_of_subms_segment=0b01,
            library=args.library,
        )
    elif args.code == "CCS":
        time_code = CCSDS_TimeCode_CCS(
            calendar_variation_flag=0b0,
            resolution=0b110,
            library=args.library,
        )
    elif args.code == "ASCII":
        time_code = CCSDS_TimeCode_ASCII()

    print(time_code)
    if args.code in ["CUC", "CDS"]:
        total_seconds = time_code.get_total_seconds(args.utc)
        print(f"Total Seconds: {total_seconds:.16f}")
        contents = time_code.get_contents(total_seconds)
        for key, val in contents.items():
            print(f"{key}: {val}")
    print("---")
    print(f"UTC: {args.utc}")
    p_field = time_code.get_p_field()
    if p_field is not None:
        print(f"P-Field(hex): {hexdump(p_field, ' ')}")
    print(f"T-Field(hex): {hexdump(time_code.get_t_field(args.utc), ' ')}")


if __name__ == "__main__":
    main()
