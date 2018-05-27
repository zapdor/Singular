import sys

import pandas as pd


def fix_pandas_bug(report_data):
    need_converting = [(x.month < 13 and x.day < 13) for x in report_data['Date']]
    if False in need_converting[:-1]:
        report_data['Date'] = report_data['Date'].dt.strftime('%Y-%m-%d')
    else:
        report_data['Date'] = report_data['Date'].dt.strftime('%Y-%d-%m')


def report_parser(file_path):
    report_data = pd.read_excel(file_path, sheet_name=None, header=3)['Sheet1']

    # prepare tables
    report_data['Date'] = pd.to_datetime(report_data['Date'][:-1])  # -1 always to ignore "Totals"
    # so apparently there is a bug with pandas and european machines (and with Excel!) - this will fix if needed
    fix_pandas_bug(report_data)
    report_data['Platform'] = report_data['Campaign'].apply(lambda x: str(x).split(' ', 1)[0])

    # get requested info
    total_costs = report_data['Cost'].iat[-1]
    total_installs = report_data['Installs'].iat[-1]

    per_date = report_data.groupby('Date')['Date', 'Cost', 'Installs'].sum()[:-1]
    per_app_and_platform = report_data.groupby(['App', 'Platform'])['Date', 'Cost', 'Installs'].sum()[:-1]

    # print all
    print("*Total installs:* {}\n".format(total_installs))
    print("*Total cost:* {}\n".format(total_costs))
    print("*Total per date:*\n")
    print(per_date)
    print("\n")
    print("*Total per App & Platform:*\n")
    print(per_app_and_platform)


def main():
    if len(sys.argv) != 2:
        print("Command should be: 'python Singular1.py <file_path>'")
        sys.exit(1)
    report_parser(sys.argv[1])


if __name__ == "__main__":
    main()
