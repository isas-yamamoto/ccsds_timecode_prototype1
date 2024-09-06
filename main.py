import argparse
from ccsds_timecode.cuc import CCSDS_TimeCode_CUC


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
        "--epoch",
        type=str,
        default="1958-01-01T00:00:00Z",
        help="The epoch time string in ISO 8601 format.",
    )
    parser.add_argument(
        "--utc",
        type=str,
        default="2024-01-01T00:00:00Z",
        help="The UTC time string in ISO 8601 format.",
    )
    parser.add_argument(
        "--library",
        type=str,
        choices=["astropy", "spice", "skyfield", "spacepy"],
        default="spice",
        help="The library to use for time conversion ('astropy', 'spice', 'skyfield', or 'spacepy').",
    )

    # Parse arguments
    args = parser.parse_args()

    # Initialize CCSDS_TimeCode_CUC with the parsed library
    ccsds_time_code = CCSDS_TimeCode_CUC(
        epoch=args.epoch,
        basic_time_unit=1,
        num_basic_octets=4,
        num_fractional_octets=2,
        library=args.library,
    )

    # Output results
    print(f"P-Field: {hexdump(ccsds_time_code.get_p_field(), ' ')}")
    print(f"T-Field: {hexdump(ccsds_time_code.get_t_field(args.utc), ' ')}")
    print(f"Total Seconds: {ccsds_time_code.get_total_seconds(args.utc)}")


if __name__ == "__main__":
    main()
