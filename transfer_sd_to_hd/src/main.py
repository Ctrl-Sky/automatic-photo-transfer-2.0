import argparse
import os

TABLE_PATH = "tables/sd_migration_table.csv"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sd_card_path", default="/Volumes/SD_CARD_1")
    parser.add_argument("--external_hd_path", default="/Volumes/kl")
    parser.add_argument("--migration_name", required=False, default="")
    parser.add_argument("--end_on", required=False, default="")
    parser.add_argument("--include_day", required=False, default=True)
    args = parser.parse_args()

    sd_card_path = args.sd_card_path
    external_hd_path = args.external_hd_path
    migration_name = args.migration_name
    end_on = args.end_on
    include_day = args.include_day